from pydantic import BaseSettings
from pydantic.fields import Field
from pydantic.networks import HttpUrl
from functools import lru_cache


class Settings(BaseSettings):
    listen_host: str = Field('0.0.0.0')
    listen_port: int = Field(8000)

    egrul_url: HttpUrl = Field('https://egrul.nalog.ru')

    damia_fns_api_key: str
    damia_fns_url: HttpUrl = Field('https://api-fns.ru/api')

    damia_arbit_api_key: str
    damia_arbit_url: HttpUrl = Field('https://damia.ru/api-arb')

    damia_scoring_api_key: str
    damia_scoring_url: HttpUrl = Field('https://damia.ru/api-scoring')

    terrorists_search_url: str = Field('http://www.fedsfm.ru/TerroristSearch')

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()
