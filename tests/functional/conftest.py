import asyncio
import json

import pytest
import aiohttp

from kafka import KafkaConsumer

from functional.settings import settings


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def aiohttp_client():
    client = aiohttp.ClientSession()
    yield client
    await client.close()


@pytest.fixture(scope='session')
def create_user(aiohttp_client):

    async def inner(*args, **kwargs):
        user_data = {
            'username': 'testname',
            'login': 'testlogin',
            'password': 'Fcbate2002_$',
            'email': 'test@example.ru',
            'first_name': 'string',
            'last_name': 'string',
            'birth_day': '2024-02-29',
            'picture': 'string',
        }
        url = f'{settings.auth_service.url()}/signup/'
        headers = {}
        async with aiohttp_client.post(url, json=user_data, headers=headers) as response:
            status = response.status
            return status

    return inner


@pytest.fixture(scope='session')
def login_user(aiohttp_client):

    async def inner(*args, **kwargs):
        login_data = {
            'login': 'testlogin',
            'password': 'Fcbate2002_$'
        }
        url = f'{settings.auth_service.url()}/login/'
        headers = {}
        async with aiohttp_client.post(url, json=login_data, headers=headers) as response:
            return response.cookies

    return inner


@pytest.fixture(scope='session')
def make_post_request(aiohttp_client):

    async def inner(data: dict, method: str, access_token: str = None):
        url = f'{settings.ugc_service.url()}/{method}'
        cookies = {}
        if access_token:
            cookies = {'access_token_cookie': access_token}
        async with aiohttp_client.post(url, json=data, cookies=cookies) as response:
            body = None
            status = response.status
            if 'Content-Type' in response.headers and 'application/json' in response.headers['Content-Type']:
                body = await response.json()
            return {
                'body': body,
                'status': status
            }
    return inner


@pytest.fixture(scope='session')
def get_token(login_user):

    async def inner(*args, **kwargs):
        tokens = await login_user()
        access_token = tokens['access_token_cookie'].value
        return access_token

    return inner


@pytest.fixture(scope='session')
def consumer_client():
    consumer = KafkaConsumer(
        bootstrap_servers=['kafka-0:9092', 'kafka-1:9092', 'kafka-2:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=False,
    )
    consumer.subscribe(["messages"])
    yield consumer
    consumer.close()
