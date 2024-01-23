import random
import uuid

from functional.settings import fake, test_settings

random.seed(42)


def generate_movie_sample() -> dict:
    genres = (
        fake.words(
            ext_word_list=[
                "Sci-Fi",
                "Thriller",
                "Horror",
                "Mistery",
                "History",
                "Science",
            ],
            nb=2,
            unique=True,
        ),
    )
    director = [fake.name() for _ in range(2)]
    writers_name = [fake.name() for _ in range(2)]
    actors_name = [fake.name() for _ in range(2)]
    return {
        "id": str(uuid.uuid4()),
        "imdb_rating": fake.random.randint(0, 10),
        "genre": genres,
        "title": fake.sentence(nb_words=2),
        "description": fake.sentence(),
        "director": director,
        "actors_names": actors_name,
        "writers_names": writers_name,
        "actors": [{"id": fake.uuid4(), "name": name} for name in actors_name],
        "writers": [{"id": fake.uuid4(), "name": name} for name in writers_name],
        "genres": [
            {"id": fake.uuid4(), "name": name} for genre in genres for name in genre
        ],
    }


def generate_movies_data(size: int = 60) -> list[dict]:
    es_data = [generate_movie_sample() for _ in range(size)]
    bulk_query = []
    for row in es_data:
        data = {"_index": test_settings.es_movie_index, "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)
    return bulk_query


def generate_search_queries(data: list[dict], counts: int = 10):
    queries = []
    names = [item["_source"]["title"] for item in data]
    for _ in range(counts):
        choice = random.choice(names)
        body = [
            item["_source"]["id"]
            for item in data
            if choice.lower() in item["_source"]["title"].lower()
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
    data_sorted_by_title_asc = sorted(data, key=lambda item: item["_source"]["title"])
    film_ids_asc_title = [item["_source"]["id"] for item in data_sorted_by_title_asc]
    data_sorted_by_title_desc = sorted(
        data, key=lambda item: item["_source"]["title"], reverse=True
    )
    film_ids_desc_title = [item["_source"]["id"] for item in data_sorted_by_title_desc]
    data_sorted_by_imdb_rating_asc = sorted(
        data, key=lambda item: item["_source"]["imdb_rating"]
    )
    film_ids_asc_imdb = [
        item["_source"]["id"] for item in data_sorted_by_imdb_rating_asc
    ]
    data_sorted_by_imdb_rating_desc = sorted(
        data, key=lambda item: item["_source"]["imdb_rating"], reverse=True
    )
    film_ids_desc_imdb = [
        item["_source"]["id"] for item in data_sorted_by_imdb_rating_desc
    ]
    queries = [
        (
            {"sort": "title"},
            {"status": 200, "body": film_ids_asc_title[min_index:max_index]},
        ),
        (
            {"sort": "-title"},
            {"status": 200, "body": film_ids_desc_title[min_index:max_index]},
        ),
        (
            {"sort": "imdb_rating"},
            {
                "status": 200,
                "body": film_ids_asc_imdb[min_index:max_index],
            },
        ),
        (
            {"sort": "-imdb_rating"},
            {
                "status": 200,
                "body": film_ids_desc_imdb[min_index:max_index],
            },
        ),
    ]
    return queries


def generate_filter_queries(data: list[dict]):
    queries = []
    actor_id = random.choice(
        [item["id"] for row in data for item in row["_source"]["actors"]]
    )
    writer_id = random.choice(
        [item["id"] for row in data for item in row["_source"]["writers"]]
    )
    genre = random.choice(
        [item["id"] for row in data for item in row["_source"]["genres"]]
    )
    actor_films = [
        row["_source"]["id"]
        for row in data
        for item in row["_source"]["actors"]
        if item["id"] == actor_id
    ]
    writer_films = [
        row["_source"]["id"]
        for row in data
        for item in row["_source"]["writers"]
        if item["id"] == writer_id
    ]
    genre_films = [
        row["_source"]["id"]
        for row in data
        for item in row["_source"]["genres"]
        if item["id"] == genre
    ]

    print(len(actor_films))
    print(len(writer_films))
    print(len(genre_films))

    queries.append(
        (
            {"actor_id": actor_id},
            {"status": 200, "length": min(len(actor_films), 40), "body": actor_films},
        )
    )
    queries.append(
        (
            {"writer_id": writer_id},
            {"status": 200, "length": min(len(writer_films), 40), "body": writer_films},
        )
    )
    queries.append(
        (
            {"genre": genre},
            {"status": 200, "length": min(len(genre_films), 40), "body": genre_films},
        )
    )

    return queries


MOVIE_MOCK_DATA = generate_movies_data(125)
MOVIE_SORT_TEST_QUERY = generate_sort_queries(MOVIE_MOCK_DATA)
MOVIE_SEARCH_TEST_QUERY = generate_search_queries(MOVIE_MOCK_DATA, 10)
MOVIE_PAGINATION_TEST_QUERY = generate_pagination_queries(MOVIE_MOCK_DATA)
MOVIE_FILTER_TEST_QUERY = generate_filter_queries(MOVIE_MOCK_DATA)
