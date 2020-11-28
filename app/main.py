from app.tools.damia.fns import FNSClient
from fastapi import FastAPI
from .settings import get_settings


app = FastAPI()

@app.get('/data')
def get_data():
    return FNSClient().search('Варламов Илья')
