import time

from functional.settings import test_settings
from redis.client import Redis


def wait_for_redis(redis: Redis):
    while True:
        if redis.ping():
            break
        time.sleep(1)


def main():
    redis_client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    wait_for_redis(redis_client)


if __name__ == "__main__":
    main()
