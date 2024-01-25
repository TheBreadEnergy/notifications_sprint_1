import asyncio

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from functional.settings import test_settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="es_client", scope="session")
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name="client_session", scope="session")
async def client_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name="es_write_data")
def es_write_data(es_client):
    async def inner(index_name: str, template: dict, data: list[dict]):
        if await es_client.indices.exists(index=index_name):
            await es_client.indices.delete(index=index_name)
        await es_client.indices.create(index=index_name, body=template)
        updated, errors = await async_bulk(
            client=es_client, actions=data, refresh="wait_for"
        )
        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest_asyncio.fixture(name="make_get_request")
def make_get_request(client_session):
    async def inner(path: str, query_data):
        url = test_settings.service_url + path
        async with client_session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        return {"body": body, "headers": headers, "status": status}

    return inner
