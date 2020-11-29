from apiclient import endpoint

from .base_client import BaseClient
from app.settings import get_settings
from app.data.financial.models import Individual, Entity

settings = get_settings()


@endpoint(base_url=settings.egrul_url)
class NalogRu:
    base = ''
    result = 'search-result/{query_id}'


def extract_entity(raw_record):
    name = raw_record['n']
    itn = raw_record['i']
    if raw_record['k'] == 'ul':
        return Entity(name, itn)
    else:
        return Individual(name, itn)


class NalogRuClient(BaseClient):
    def get_query_data(self, query: str, region_code: str):
        return self.post(NalogRu.base, data={'query': query, 'region': region_code})

    def search(self, query: str, region_code: str):
        t = self.get_query_data(query, region_code)['t']
        res = self.get(NalogRu.result.format(query_id=t))['rows']
        return list(
            map(
                extract_entity,
                filter(
                    lambda rec: all(map(rec.__contains__, 'ink')),
                    res
                )
            )
        )
