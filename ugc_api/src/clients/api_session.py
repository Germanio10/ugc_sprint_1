from aiohttp import client


session: client.ClientSession | None = None


def get_api_session() -> client.ClientSession:
    return session