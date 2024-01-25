import pytest
from functional.settings import test_settings
from functional.testdata.movie_data import (
    MOVIE_FILTER_TEST_QUERY,
    MOVIE_MOCK_DATA,
    MOVIE_PAGINATION_TEST_QUERY,
    MOVIE_SEARCH_TEST_QUERY,
    MOVIE_SORT_TEST_QUERY,
)
from functional.testdata.movie_template import MOVIE_TEMPLATE

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("query_data, expected_answer", MOVIE_PAGINATION_TEST_QUERY)
async def test_pagination(
    es_write_data, make_get_request, query_data: dict, expected_answer: dict
):
    await es_write_data(test_settings.es_movie_index, MOVIE_TEMPLATE, MOVIE_MOCK_DATA)
    response = await make_get_request("/api/v1/films/", query_data)
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]


@pytest.mark.parametrize("query_data, expected_answer", MOVIE_SORT_TEST_QUERY)
@pytest.mark.asyncio
async def test_sort(
    es_write_data, make_get_request, query_data: dict, expected_answer: dict
):
    await es_write_data(test_settings.es_movie_index, MOVIE_TEMPLATE, MOVIE_MOCK_DATA)
    response = await make_get_request("/api/v1/films/", query_data)
    assert response["status"] == expected_answer["status"]
    assert [item["id"] for item in response["body"]] == expected_answer["body"]


@pytest.mark.parametrize("query_data, expected_answer", MOVIE_FILTER_TEST_QUERY)
async def test_filter(
    es_write_data, make_get_request, query_data: dict, expected_answer: dict
):
    await es_write_data(test_settings.es_movie_index, MOVIE_TEMPLATE, MOVIE_MOCK_DATA)
    response = await make_get_request("/api/v1/films/", query_data)
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]
    assert [item["id"] for item in response["body"]] == expected_answer["body"]


@pytest.mark.parametrize("query_data, expected_answer", MOVIE_SEARCH_TEST_QUERY)
async def test_search(
    es_write_data, make_get_request, query_data: dict, expected_answer: dict
):
    await es_write_data(test_settings.es_movie_index, MOVIE_TEMPLATE, MOVIE_MOCK_DATA)
    response = await make_get_request("/api/v1/films/search/", query_data)
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]
    assert [item["id"] for item in response["body"]] == expected_answer["body"]
