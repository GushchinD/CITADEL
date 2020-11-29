from apiclient import endpoint
from typing import List
from app.data.financial.models import Individual, Entity, EntityStatus

from app.settings import get_settings

from .base_client import BaseDaMIAClient


@endpoint(base_url=get_settings().damia_fns_url)
class FNS:
    search = 'search'
    company_data = 'egr'
    companies_data = 'multiinfo'


def extract_entity(raw_record):
    if 'ИП' in raw_record:
        return Individual(name=raw_record['ИП']['ФИОПолн'], itn=raw_record['ИП']['ИНН'])
    else:  # elif 'ЮЛ' in raw_record:
        return Entity(
            name=raw_record['ЮЛ']['НаимПолнЮЛ'],
            itn=raw_record['ЮЛ']['ИНН'],
            status=EntityStatus.active if raw_record['ЮЛ']['Статус'] == 'Действующее' else EntityStatus.liquidated
        )


class FNSClient(BaseDaMIAClient):
    def __init__(self) -> None:
        super(FNSClient, self).__init__(get_settings().damia_fns_api_key)

    def search(self, query: str):
        return list(
            map(
                extract_entity,
                self.get(FNS.search, params={'q': query})['items']
            )
        )

    def company_data(self, inn: str):
        result = self.get(FNS.company_data, params={'req': inn})

        return result

    def companies_data(self, inns: List[str]):
        return self.get(FNS.companies_data, params={'req': ','.join(inns)})
