from uvicorn import run
from .main import app
from .settings import get_settings

if __name__ == '__main__':
    run(app, host=get_settings().listen_host, port=get_settings().listen_port)
