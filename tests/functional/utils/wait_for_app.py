import os

import backoff
from dotenv import load_dotenv
import requests


load_dotenv()


@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
def connect_server(host: str, port: int):
    print('Ожидание сервера...')
    r = requests.get(f'http://{host}:{port}', stream=True)


if __name__ == "__main__":

    host = os.getenv("FASTAPI_UGC_HOST") or 'localhost'
    port = os.getenv("FASTAPI_UGC_PORT") or 8000

    connect_server(host, int(port))
