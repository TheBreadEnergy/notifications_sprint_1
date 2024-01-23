import pytest
from functional.settings import test_settings
from functional.testdata.genre_data import (
    GENRE_MOCK_DATA,
    GENRE_PAGINATION_TEST_QUERY,
    GENRE_SEARCH_TEST_QUERY,
    GENRE_SORT_TEST_QUERY,
)
from functional.testdata.genre_template import GENRE_TEMPLATE

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("query_data, expected_answer", GENRE_PAGINATION_TEST_QUERY)
async def test_pagination(
    es_write_data, make_get_request, query_data: dict, expected_answer: dict
):
    await es_write_data(test_settings.es_genre_index, GENRE_TEMPLATE, GENRE_MOCK_DATA)
    response = await make_get_request("/api/v1/genres/", query_data)
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]


@pytest.mark.parametrize("query_data, expected_answer", GENRE_SORT_TEST_QUERY)
async def test_sort(
    es_write_data, make_get_request, query_data: dict, expected_answer: dict
):
    await es_write_data(test_settings.es_genre_index, GENRE_TEMPLATE, GENRE_MOCK_DATA)
    response = await make_get_request("/api/v1/genres/", query_data)
    assert response["status"] == expected_answer["status"]

    assert [item["id"] for item in response["body"]] == expected_answer["body"]


@pytest.mark.parametrize("query_data, expected_answer", GENRE_SEARCH_TEST_QUERY)
async def test_search(
    es_write_data, make_get_request, query_data: dict, expected_answer: dict
):
    await es_write_data(test_settings.es_genre_index, GENRE_TEMPLATE, GENRE_MOCK_DATA)
    response = await make_get_request("/api/v1/genres/search/", query_data)
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]
    assert [item["id"] for item in response["body"]] == expected_answer["body"]
