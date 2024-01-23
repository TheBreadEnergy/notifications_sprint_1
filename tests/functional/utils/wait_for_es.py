import time

from elasticsearch import Elasticsearch
from functional.settings import test_settings


def wait_for_es(es_client: Elasticsearch):
    while True:
        if es_client.ping():
            break
        time.sleep(1)


def main():
    es_client = Elasticsearch(hosts=test_settings.es_host)
    wait_for_es(es_client)


if __name__ == "__main__":
    main()
