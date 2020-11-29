from apiclient import endpoint, unmarshal_response
from dataclasses import dataclass

from app.settings import get_settings

from .base_client import BaseDaMIAClient


@endpoint(base_url=get_settings().damia_fns_url)
class FNS:
    search = 'search'
    company_data = 'egr'
    companies_data = 'multiinfo'


class FNSClient(BaseDaMIAClient):
    def __init__(self) -> None:
        super(FNSClient, self).__init__(get_settings().damia_fns_api_key)

    def search(self, query: str):
        return self.get(FNS.search, params={'q': query})['items']

    def company_data(self, inn: str):
        return self.get(FNS.company_data, params={'req': inn})

    def companies_data(self, inns: list[str]):
        return self.get(FNS.companies_data, params={'req': ','.join(inns)})
