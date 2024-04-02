import os

import backoff
from dotenv import load_dotenv
from clickhouse_driver import Client
from clickhouse_driver import  errors


load_dotenv()


@backoff.on_exception(backoff.expo, (errors.NetworkError, errors.UnexpectedPacketFromServerError))
def connect_clickhouse(client: Client):
    print('Ожидание clickhouse...')
    client.execute('SHOW DATABASES')


if __name__ == "__main__":
    host = os.getenv("CLICKHOUSE_MAIN_HOST")
    port = os.getenv("CLICKHOUSE_PORT")

    client = Client(host=host, port=port)
    
    connect_clickhouse(client)
