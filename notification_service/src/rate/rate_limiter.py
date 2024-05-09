from aiohttp import ClientConnectorError
from aiohttp.web_exceptions import HTTPError


def is_rate_limited(thrown_type, thrown_value):
    return issubclass(thrown_type, HTTPError) and thrown_value.status_code == 429


def is_circuit_processable(thrown_type, thrown_value):
    return is_rate_limited(thrown_type, thrown_value) or issubclass(
        thrown_type, ClientConnectorError
    )
