from aiohttp import ClientSession

client_session: ClientSession | None = None


def get_client_session() -> ClientSession:
    return client_session or ClientSession()
