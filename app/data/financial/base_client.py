from apiclient.client import APIClient

from apiclient.authentication_methods import NoAuthentication
from apiclient.request_formatters import NoOpRequestFormatter
from apiclient.response_handlers import JsonResponseHandler


class BaseClient(APIClient):
    def __init__(self) -> None:
        super(BaseClient, self).__init__(response_handler=JsonResponseHandler,
                                         authentication_method=NoAuthentication(),
                                         request_formatter=NoOpRequestFormatter)
