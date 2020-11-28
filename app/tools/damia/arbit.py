from apiclient import endpoint, unmarshal_response
from dataclasses import dataclass

from .base_client import BaseDaMIAClient

from app.settings import get_settings

@endpoint(base_url=get_settings().damia_arbit_url)
class Arbit:
    ...

class ArbitClient(BaseDaMIAClient):
    def __init__(self) -> None:
        super(ArbitClient, self).__init__(get_settings().damia_arbit_api_key)
