from apiclient import APIClient, endpoint, unmarshal_response

from apiclient.authentication_methods import NoAuthentication
from apiclient.request_formatters import NoOpRequestFormatter
from apiclient.response_handlers import JsonResponseHandler

from dataclasses import dataclass
from typing import Optional

from app.settings import get_settings

settings = get_settings()


@dataclass
class EgrulRecord:
    o: str
    i: Optional[str]
    n: str


class NalogRuClient(APIClient):
    @endpoint(base_url=settings.egrul_url)
    class NalogRu:
        base = ''
        result = 'search-result/{query_id}'

    def __init__(self) -> None:
        super(NalogRuClient, self).__init__(response_handler=JsonResponseHandler,
                                            authentication_method=NoAuthentication(),
                                            request_formatter=NoOpRequestFormatter)

    def get_query_data(self, query: str, region_code: str):
        return self.post(NalogRuClient.NalogRu.base, data={'query': query, 'region': region_code})

    # @unmarshal_response(list[EgrulRecord])
    def search(self, query: str, region_code: str):
        t = self.get_query_data(query, region_code)['t']
        res = self.get(NalogRuClient.NalogRu.result.format(query_id=t))['rows']
        return list(
            filter(lambda rec: all(map(rec.__contains__, 'oin')), res)
        )
