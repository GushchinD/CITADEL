from apiclient import endpoint

from .base_client import BaseClient
from app.settings import get_settings


settings = get_settings()


@endpoint(base_url=settings.terrorists_search_url)
class TerroristSearch:
    search = ''


class TerroristSearchClient(BaseClient):
    def search(self, query: str):
        return self.post(TerroristSearch.search, data={'rowIndex': 0, 'pageLength': 10000, 'searchText': query})
