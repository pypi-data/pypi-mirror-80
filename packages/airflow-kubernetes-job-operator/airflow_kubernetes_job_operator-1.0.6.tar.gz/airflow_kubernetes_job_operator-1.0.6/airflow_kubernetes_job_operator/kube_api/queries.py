from logging import Logger
import logging
from datetime import datetime
import os
import json
from typing import Union
import dateutil.parser
from zthreading.events import Event

from airflow_kubernetes_job_operator.kube_api.exceptions import KubeApiClientException, KubeApiException
from airflow_kubernetes_job_operator.kube_api.utils import kube_logger, not_empty_string
from airflow_kubernetes_job_operator.kube_api.collections import KubeObjectKind, KubeObjectState, KubeObjectDescriptor
from airflow_kubernetes_job_operator.kube_api.client import KubeApiRestQuery, KubeApiRestClient


KUBE_API_SHOW_SERVER_LOG_TIMESTAMPS = os.environ.get("KUBE_API_SHOW_SERVER_LOG_TIMESTAMPS", "false").lower() == "true"
KUBE_API_SHOW_SERVER_DETECT_LOG_LEVEL = (
    os.environ.get("KUBE_API_SHOW_SERVER_DETECT_LOG_LEVEL", "true").lower() == "true"
)


def do_detect_log_level(line: "LogLine", msg: str):
    if "CRITICAL" in msg:
        return logging.CRITICAL
    if "ERROR" in msg:
        return logging.ERROR
    elif "WARN" in msg or "WARNING" in msg:
        return logging.WARNING
    elif "DEBUG" in msg:
        return logging.DEBUG
    else:
        return logging.INFO


KUBE_API_SHOW_SERVER_DETECT_LOG_LEVEL_METHOD = do_detect_log_level


class LogLine:
    def __init__(self, pod_name: str, namespace: str, message: str, timestamp: datetime):
        super().__init__()
        self.pod_name = pod_name
        self.namespace = namespace
        self.message = message
        self.timestamp = timestamp

    def log(self, logger: Logger = kube_logger):
        msg = self.__repr__()
        if not KUBE_API_SHOW_SERVER_DETECT_LOG_LEVEL:
            logger.info(msg)
        elif KUBE_API_SHOW_SERVER_DETECT_LOG_LEVEL_METHOD is not None:
            logger.log(
                KUBE_API_SHOW_SERVER_DETECT_LOG_LEVEL_METHOD(self, msg) or logging.INFO,
                msg,
            )
        else:
            logger.info(msg)

    def __str__(self):
        return self.message

    def __repr__(self):
        timestamp = f"[{self.timestamp}]" if KUBE_API_SHOW_SERVER_LOG_TIMESTAMPS else ""
        return timestamp + f"[{self.namespace}/pods/{self.pod_name}]: {self.message}"


class GetPodLogs(KubeApiRestQuery):
    def __init__(
        self,
        name: str,
        namespace: str = None,
        since: datetime = None,
        follow: bool = False,
        timeout: int = None,
    ):
        assert not_empty_string(name), ValueError("name must be a non empty string")
        assert not_empty_string(namespace), ValueError("namespace must be a non empty string")

        kind: KubeObjectKind = KubeObjectKind.get_kind("Pod")
        super().__init__(
            resource_path=kind.compose_resource_path(namespace=namespace, name=name, suffix="log"),
            method="GET",
            timeout=timeout,
            auto_reconnect=follow,
        )

        self.kind = kind
        self.name: str = name
        self.namespace: str = namespace
        self.since: datetime = since
        self.query_params = {
            "follow": follow,
            "pretty": False,
            "timestamps": True,
        }

        self.since = since
        self._last_timestamp = None
        self._active_namespace = None

    def pre_request(self, client: "KubeApiRestClient"):
        super().pre_request(client)

        # Updating the since argument.
        last_ts = self.since if self.since is not None and self.since > self._last_timestamp else self._last_timestamp

        since_seconds = None
        if last_ts is not None:
            since_seconds = (datetime.now() - last_ts).total_seconds()
            if since_seconds < 0:
                since_seconds = 0

        self.query_params["sinceSeconds"] = since_seconds

    def on_reconnect(self, client: KubeApiRestClient):
        # updating the since property.
        if not self.query_running or not self.auto_reconnect:
            # if the query is not running then we have reached the pods log end.
            # we should disconnect, otherwise we should have had an error.
            self.auto_reconnect = False
            return

        try:
            pod = client.query(
                GetNamespaceObjects(
                    kind=self.kind,
                    namespace=self.namespace,
                    name=self.name,
                )
            )
            self.auto_reconnect = pod is not None and KubeObjectDescriptor(pod).state == KubeObjectState.Running
            if self.auto_reconnect:
                super().on_reconnect(client)
        except Exception as ex:
            self.auto_reconnect = False
            raise ex

    def parse_data(self, message_line: str):
        self._last_timestamp = datetime.now()
        timestamp = dateutil.parser.isoparse(message_line[: message_line.index(" ")])

        message = message_line[message_line.index(" ") + 1 :]  # noqa: E203
        message = message.replace("\r", "")
        lines = []
        for message_line in message.split("\n"):
            lines.append(LogLine(self.name, self.namespace, message_line, timestamp))
        return lines

    def emit_data(self, data):
        for line in data:
            super().emit_data(line)

    def log_event(self, logger: Logger, ev: Event):
        if ev.name == self.data_event_name and isinstance(ev.args[0], LogLine):
            ev.args[0].log(logger)
        super().log_event(logger, ev)


class GetNamespaceObjects(KubeApiRestQuery):
    def __init__(
        self,
        kind: Union[str, KubeObjectState],  # type:ignore
        namespace: str,
        name: str = None,
        api_version: str = None,
        watch: bool = False,
        label_selector: str = None,
        field_selector: str = None,
    ):
        kind: KubeObjectKind = (
            kind if isinstance(kind, KubeObjectKind) else KubeObjectKind.get_kind(kind)  # type:ignore
        )
        super().__init__(
            resource_path=kind.compose_resource_path(namespace=namespace, name=name, api_version=api_version),
            method="GET",
            query_params={
                "pretty": False,
                "fieldSelector": field_selector or "",
                "labelSelector": label_selector or "",
                "watch": watch,
            },
            auto_reconnect=watch,
            throw_on_if_first_api_call_fails=name is None,
        )
        self.kind = kind
        self.namespace = namespace

    def parse_data(self, line):
        rsp = json.loads(line)
        return rsp

    def emit_data(self, data: dict):
        if "kind" in data:
            data_kind: str = data["kind"]
            if data_kind.endswith("List"):
                item_kind = data_kind[:-4]
                for item in data["items"]:
                    item["kind"] = item_kind
                    super().emit_data(item)
            else:
                super().emit_data(data)
        elif "type" in data:
            # as event.
            event_object = data["object"]
            event_object["event_type"] = data["type"]
            super().emit_data(event_object)

    def query_loop(self, client):
        try:
            return super().query_loop(client)
        except KubeApiClientException as ex:
            if ex.rest_api_exception.status == 404:
                raise KubeApiException(
                    f"Resource {self.resource_path} of kind '{self.kind.api_version}/{self.kind.name}' not found"
                )
        except Exception as ex:
            raise ex


class GetAPIResources(KubeApiRestQuery):
    def __init__(
        self,
        api="apps/v1",
    ):
        super().__init__(
            f"/apis/{api}",
        )

    def parse_data(self, data):
        return json.loads(data)


class GetAPIVersions(KubeApiRestQuery):
    def __init__(
        self,
    ):
        super().__init__(
            "/apis",
            method="GET",
        )

    def parse_data(self, data):
        rslt = json.loads(data)
        prased = {}
        for grp in rslt.get("groups", []):
            group_name = grp.get("name")
            preferred = grp.get("preferredVersion", {}).get("version")
            for ver_info in grp.get("versions", []):
                group_version = ver_info.get("groupVersion")
                version = ver_info.get("version")
                assert group_version is not None, KubeApiException("Invalid group version returned from the api")
                prased[group_version] = {
                    "group_name": group_name,
                    "is_preferred": preferred == version,
                    "version": version,
                    "group": grp,
                }
        return prased
