from apiclient import endpoint, unmarshal_response
from dataclasses import dataclass

from app.settings import get_settings

from .base_client import BaseDaMIAClient


@endpoint(base_url=get_settings().damia_arbit_url)
class Arbit:
    search = 'dela'
    details = 'delo'

class ArbitClient(BaseDaMIAClient):
    def __init__(self) -> None:
        super(ArbitClient, self).__init__(get_settings().damia_arbit_api_key)

    def search(self, query: str):
        return self.get(Arbit.search, params={'q': query, 'exact': 0})

    def details(self, id: str):
        return self.get(Arbit.details, params={'regn': id})
