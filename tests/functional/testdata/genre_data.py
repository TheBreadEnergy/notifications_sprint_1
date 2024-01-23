import random
import uuid

from functional.settings import fake, test_settings

random.seed(42)


def generate_genre_sample() -> dict:
    genres = ["Sci-Fi", "Thriller", "Horror", "Mystery", "History", "Science"]
    return {
        "id": str(uuid.uuid4()),
        "name": random.choice(genres),
        "description": fake.sentence(),
    }


def generate_genres_data(size: int = 60) -> list[dict]:
    es_data = [generate_genre_sample() for _ in range(size)]
    bulk_query = []
    for row in es_data:
        data = {"_index": test_settings.es_genre_index, "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)
    return bulk_query


def generate_search_queries(data: list[dict], counts: int = 10):
    queries = []
    names = [item["_source"]["name"] for item in data]
    for _ in range(counts):
        choice = random.choice(names)
        body = [
            item["_source"]["id"]
            for item in data
            if choice.lower() in item["_source"]["name"].lower()
        ]
        queries.append(
            ({"query": choice}, {"status": 200, "length": len(body), "body": body})
        )
    queries.append(({"query": "!dfdf"}, {"status": 200, "length": 0, "body": []}))
    return queries


def generate_pagination_queries(data: list[dict], size: int = 40):
    queries = []
    last_page = len(data) // size + 1
    queries.append(
        (
            {"page": 1, "size": size},
            {"status": 200, "body": data[:size], "length": min(size, len(data))},
        )
    )
    last_start, last_end = (last_page - 1) * size, min(last_page * size, len(data))
    queries.append(
        (
            {"page": last_page, "size": size},
            {
                "status": 200,
                "body": data[last_start:last_end],
                "length": last_end - last_start,
            },
        )
    )
    random_page = random.randint(0, last_page)
    random_start, random_end = max(0, random_page - 1) * size, min(
        len(data), random_page * size
    )
    queries.append(
        (
            {"page": random_page, "size": size},
            {
                "status": 200,
                "body": data[random_start:random_end],
                "length": random_end - random_start,
            },
        ),
    )
    return queries


def generate_sort_queries(data: list[dict], page: int = 1, size: int = 40):
    min_index = (page - 1) * size
    max_index = page * size
    data_sorted_by_name_asc = sorted(data, key=lambda item: item["_source"]["name"])
    genre_ids_asc_name = [item["_source"]["id"] for item in data_sorted_by_name_asc]
    data_sorted_by_name_desc = sorted(
        data, key=lambda item: item["_source"]["name"], reverse=True
    )
    genre_ids_desc_name = [item["_source"]["id"] for item in data_sorted_by_name_desc]
    queries = [
        (
            {"sort": "asc"},
            {"status": 200, "body": genre_ids_asc_name[min_index:max_index]},
        ),
        (
            {"sort": "desc"},
            {"status": 200, "body": genre_ids_desc_name[min_index:max_index]},
        ),
    ]
    return queries


GENRE_MOCK_DATA = generate_genres_data(125)
GENRE_SORT_TEST_QUERY = generate_sort_queries(GENRE_MOCK_DATA)
GENRE_SEARCH_TEST_QUERY = generate_search_queries(GENRE_MOCK_DATA, 10)
GENRE_PAGINATION_TEST_QUERY = generate_pagination_queries(GENRE_MOCK_DATA)
