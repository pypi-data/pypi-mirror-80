import json
import logging
import re
import traceback
from concurrent.futures import ThreadPoolExecutor
from os import environ
from pprint import pformat
from typing import Dict
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from httmock import HTTMock, urlmatch
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from wrapt import ObjectProxy


class NominodeClient:
    """
    Interact with the Nominode API
    """

    def __init__(self):
        self.logger = logging.getLogger("nomigen.nominode_api")
        self._session = None

    @property
    def nominode_url(self):
        api_url = nominode_ctx.nomnom_api
        # ensure we always have a trailing / on the api url, otherwise we mess up urljoin
        return api_url if api_url.endswith("/") else api_url + "/"

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
            self._session.headers.update({"token": nominode_ctx.token})
            # max value for each backoff is 2 minutes, 20 retries gets us about 30 minutes of retrying
            retries = Retry(
                total=20, backoff_factor=1, status_forcelist=[502, 503, 504, 404]
            )
            self._session.mount(self.nominode_url, HTTPAdapter(max_retries=retries))
        return self._session

    def request(
        self,
        method: str,
        url_prefix: str = None,
        data: dict = None,
        params: Dict[str, str] = None,
        reg_data: str = None,
        headers: Dict[str, str] = None,
        path_override: str = None,
    ):
        """
        Authenticated request to nominode.

        Makes an authenticated request to the nominode and returns a JSON blob.

        Generally should not be used.

        :param method: HTTP Method to use (GET,POST,PUT,ect)
        :param url_prefix: Endpoint to hit e.g. execution/log
        :param data: Payload for request, must be JSON serializable
        :type data: optional
        :param params: URL Parameters, must be url encodable
        :type params: optional
        :param reg_data: Non JSON data to append to request. Cannot be used with data parameter
        :type reg_data: optional
        :param headers: Header dictionary
        :type headers: optional
        :param path_override: Override string for the start of the nominode url (usually /api/v1)
        :type path_override: optional
        :return: JSON Response data
        :rtype: dict
        """
        response_data = self._get_response_data(
            method=method,
            endpoint_url=url_prefix,
            data=reg_data,
            headers=headers,
            json_data=data,
            params=params,
            path_override=path_override,
        )
        return response_data

    def _get_response_data(
        self,
        method,
        endpoint_url,
        json_data=None,
        params=None,
        data=None,
        headers=None,
        path_override=None,
    ):
        headers = headers or {}
        if json_data:
            headers.update({"Content-Type": "application/json"})
        # endpoint urls should not start with a /
        endpoint_url = (
            endpoint_url if not endpoint_url.startswith("/") else endpoint_url.lstrip("/")
        )
        # this is to support overriding /api/1/ to /api/v2 if needed
        if path_override:
            split_url = list(urlsplit(self.nominode_url))
            split_url[2] = path_override
            base_url = urlunsplit(split_url)
            url = urljoin(base_url, endpoint_url)
        else:
            url = urljoin(self.nominode_url, endpoint_url)

        response = self.session.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data if data else json.dumps(json_data, default=str),
        )
        try:
            response.raise_for_status()
            data = response.json()
            return data
        except Exception:
            self.logger.exception(
                f"Error during {method}:{url} - {response.status_code} - response payload:\n{response.text}"
            )
            raise

    def update_progress(
        self, message: str = None, progress: int = None
    ) -> Dict[str, str]:
        """
        Update nominode with current task progress

        :param message: Message for to attach to current task progress
        :param progress: Number representing the percentage complete of the task (0-100)
        :return: Response data
        """
        # Called to periodically update the completion status of a given execution
        # Always sets to - '05': 'Executing: Running in docker container'
        if message is None and progress is None:
            raise Exception(
                "Message or Progress needs to be provided when updating execution status..."
            )
        data = {"status_code": "05", "progress": progress, "message": message}
        return self.request(
            "put", "execution/update/%s" % nominode_ctx.execution_uuid, data=data
        )

    def update_connection(self, connection: str, connection_uuid: str) -> Dict[str, str]:
        """
        Update a connection on the nominode

        :param connection: Dictionary representing the updated connection object
        :param connection_uuid: UUID of the connection to be updated
        :return: Response data
        """
        data = {"alias": connection["alias"], "parameters": json.dumps(connection)}
        return self.request("post", "connection/%s/update" % connection_uuid, data=data)

    def checkout_execution(self) -> Dict:
        """
        Fetch the task parameters. Should only be called once.

        :return: task parameters dictionary
        """
        return self.request("put", "execution/checkout/%s" % nominode_ctx.execution_uuid)

    def update_task_parameters(self, parameters: dict, task_uuid: str = None) -> None:
        """
        Patch the task parameters on the nominode.

        :param parameters:
            Dictionary representing the updated parameters. Partial updates are possible and will be merged in with existing parameters.
        :param task_uuid:
            UUID of the task to update, will default to the current task
        :type task_uuid: optional

        """
        task_uuid = task_uuid if task_uuid else nominode_ctx.task_uuid
        result = self.request(
            "put", "/task/{}/parameters".format(task_uuid), data=parameters
        )
        if "error" in result:
            raise Exception(result["error"])

    def update_result(self, result: Dict[str, any]) -> Dict[str, str]:
        """
        Update the task parameters on the nominode

        :param result: JSON data representing the result of this task. Currently only a json encoded Bokeh plot is supported.
        :return: Response data
        """
        assert "result_type" in result
        assert "result" in result
        result = self.request(
            "put",
            f"projects/{nominode_ctx.project_uuid}/task_execution/{nominode_ctx.execution_uuid}/result",
            data=result,
            path_override="api/v2/",
        )
        if "error" in result:
            raise Exception(result["error"])
        else:
            return result

    def get_secrets(self):
        """
        Fetch the encoded connections associated with this task
        Returns:
            dict: decoded connections
        """
        x = self.request("get", "execution/decode/%s" % nominode_ctx.execution_uuid)
        if "error" in x:
            raise Exception(x["error"])
        else:
            return x

    def get_metadata_table(self, metadata_uuid: str, data_table_uuid: str):
        """
        Fetch a specific metadata table and data table from the nominode

        Parameters:
            metadata_uuid (string): UUID String of the metadata table.
            data_table_uuid (string): UUID String of the data table within the metadata.

        Returns:
            dict: success/response data
        """
        assert metadata_uuid, "metadata_uuid is required"
        assert data_table_uuid, "data_table_uuid is required"

        # Get the data_table details and column information
        url = "metadata/{metadata_uuid}/{data_table_uuid}"
        url = url.format(metadata_uuid=metadata_uuid, data_table_uuid=data_table_uuid)
        data_table = self.request("get", url)
        if "results" in data_table:
            # Grab first data table that matches.
            data_table = data_table["results"][0]
        else:
            raise Exception(
                "Error getting data table details for {}...".format(data_table_uuid)
            )

        return data_table


class NominodeLoggingContext:
    def __init__(self, sync=False):
        self.root_logger = logging.getLogger()
        self.nominode_handler = NominodeLogHandler(sync=sync)

    def __enter__(self):
        self.root_logger.setLevel(environ.get("NND_LOG_LEVEL", logging.INFO))
        self.root_logger.addHandler(self.nominode_handler)

    def __exit__(self, et, ev, tb):
        self.root_logger.removeHandler(self.nominode_handler)
        self.nominode_handler.shutdown()


class NominodeLogHandler(logging.Handler):
    # Send log lines in a separate thread, log lines are 'non critical' so if we get a timeout we don't care too much
    # Using a thread pool to limit the number of threads spawned

    def __init__(
        self,
        *args,
        sync=False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.sync = sync
        self.nominode = NominodeClient()
        self.threadPool = ThreadPoolExecutor(1)

    def shutdown(self):
        self.threadPool.shutdown()

    def emit(self, record):
        if self.sync:
            self._emit(record)
        else:
            self.threadPool.submit(self._emit, record)

    def _emit(self, record):
        to_send = record.__dict__.copy()
        to_send["execution_uuid"] = nominode_ctx.execution_uuid
        to_send["log_version"] = "0.1.0"
        if to_send["exc_info"]:
            to_send["exception_lines"] = traceback.format_exception(*to_send["exc_info"])
            del to_send["exc_info"]
        to_send["msg"] = str(to_send["msg"])

        r_logger = logging.getLogger("requests")
        url_logger = logging.getLogger("urllib3")
        r_logger.propagate = False
        url_logger.propagate = False
        self.nominode.request(
            "put", f"execution/log/{nominode_ctx.execution_uuid}", data=to_send
        )
        r_logger.disabled = True
        url_logger.disabled = True


class NominodeContextMock(HTTMock):
    def __init__(self, task_parameters=None):
        super().__init__(self.api_match)
        self.logger = logging.getLogger("nomigen.nominode-mock")
        task_parameters = task_parameters or {}
        self.secrets = {
            k: {**secret, "alias": f"Connection Alias {i}"}
            if secret
            else {"alias": f"Connection {i}"}
            for i, (k, secret) in enumerate(task_parameters.pop("config", {}).items())
        }
        self.params = {**task_parameters, "alias": "Task Alias"}
        self.calls = []
        self.environ = None

    def __enter__(self):
        self.environ = environ.copy()
        environ["execution_uuid"] = "TEST_UUID"
        environ["task_uuid"] = "TASK_UUID"
        environ["project_uuid"] = "TEST_PROJECT"
        environ["nomnom_api"] = "http://127.0.0.1:9090"
        environ["token"] = "token"
        environ["NND_LOG_LEVEL"] = logging.getLevelName(logging.getLogger().level)
        self.nnd_context = NominodeContext.from_env()
        self.nnd_context.__enter__()
        super().__enter__()
        return self

    def __exit__(self, *args):
        self.nnd_context.__exit__(*args)
        super().__exit__(*args)
        environ.pop("execution_uuid")
        environ.pop("task_uuid")
        environ.pop("project_uuid")
        environ.pop("nomnom_api")
        environ.pop("token")

    @urlmatch(netloc=r"(.*\.)?127.0.0.1:9090$")
    def api_match(self, url, request):
        self.calls.append((url.path, json.loads(request.body)))
        match = re.match(r"/connection/(?P<uuid>.+)/update", url.path)
        if match:
            json_data = request.body
            loaded = json.loads(json_data)
            uuid = match.groupdict()["uuid"]
            self.params["config"][uuid] = json.loads(loaded["parameters"])
            self.logger.debug("Caught connections update. Test creds updated")
        elif url.path == "/execution/log/TEST_UUID":
            json_data = request.body
            loaded = json.loads(json_data)
        elif url.path == "/task/TASK_UUID/update":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug("Caught task update {}".format(pformat(loaded)))
        elif url.path == "/execution/update/TEST_UUID":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug(
                "Caught execution progress update {}".format(pformat(loaded))
            )
        elif url.path == "/execution/decode/TEST_UUID":
            return json.dumps(self.secrets)
        elif url.path == "/task/TASK_UUID/parameters":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug("Caught task parameter update {}".format(pformat(loaded)))
            return json.dumps({"result": "success"})
        elif url.path == "/execution/checkout/TEST_UUID":
            return json.dumps({"parameters": self.params, "task_uuid": "TASK_UUID"})
        else:
            self.logger.info(
                f"Unknown api endpoint called {url.path}, \n Body {request.body}"
            )
        return '{"you_logged":"test"}'


class NominodeContext:
    def __init__(self, execution_uuid, task_uuid, project_uuid, nomnom_api, token):
        self.execution_uuid = execution_uuid
        self.task_uuid = task_uuid
        self.project_uuid = project_uuid
        self.nomnom_api = nomnom_api
        self.token = token
        self.api_mock = NoContext()
        self.logging_context = NominodeLoggingContext()

    def __enter__(self):
        nominode_ctx._set_nominode_context(self)
        self.logging_context.__enter__()
        return self

    def __exit__(self, *args):
        self.logging_context.__exit__(*args)
        nominode_ctx._set_nominode_context(NoContext())

    @classmethod
    def from_env(cls):
        try:
            instance = cls(
                execution_uuid=environ["execution_uuid"],
                task_uuid=environ["task_uuid"],
                project_uuid=environ["project_uuid"],
                nomnom_api=environ["nomnom_api"],
                token=environ["token"],
            )
        except KeyError as e:
            raise RuntimeError(
                f"Could not find expected environment variable '{e.args[0]}'"
            )
        return instance


class NoContext:
    def __getattr__(self, name):
        if name in ["execution_uuid", "task_uuid", "project_uuid", "nomnom_api", "token"]:
            raise RuntimeError(
                "Not in nominode context, wrap with ExecutionContextMock or only execute via a nominode"
            )
        else:
            return super().__getattribute__(name)


class NominodeContextProxy(ObjectProxy):
    def __init__(self):
        super().__init__(None)

    def _set_nominode_context(self, nominode_ctx):
        super().__init__(nominode_ctx)


nominode_ctx: NominodeContext = NominodeContextProxy()
