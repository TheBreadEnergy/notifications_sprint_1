import logging

logger = logging.getLogger("etl_application")
logger.setLevel(logging.INFO)
file_handler = logging.StreamHandler()


formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s"
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
