from apiclient import APIClient
from apiclient.authentication_methods import QueryParameterAuthentication
from apiclient.response_handlers import JsonResponseHandler
from apiclient.request_formatters import NoOpRequestFormatter

class BaseDaMIAClient(APIClient):
    def __init__(self, api_key: str) -> None:
        super(BaseDaMIAClient, self).__init__(
            authentication_method=QueryParameterAuthentication('key', api_key),
            request_formatter=NoOpRequestFormatter,
            response_handler=JsonResponseHandler
        )
