import sys

from loguru import logger
from src.core.config import settings

REQUEST_LOG_FORMAT = (
    '{{"request_id": "{extra[request_id]}", "asctime": "{time:YYYY-MM-DD HH:mm:ss}", '
    '"levelname": "{level.name}", "name": "{name}", "message": "{message}", '
    '"host": "{extra[host]}", "user-agent": "{extra[user-agent]}", '
    '"method": "{extra[method]}", "path": "{extra[path]}", '
    '"query_params": "{extra[query_params]}", "status_code": "{extra[status_code]}"}}'
)


def setup_root_logger():
    logger.remove()
    logger.add(
        settings.logger_filename,
        format=REQUEST_LOG_FORMAT,
        level=settings.log_level,
        rotation=settings.logger_rotation,
    )
    logger.add(
        sys.stdout,
        format=REQUEST_LOG_FORMAT,
        level=settings.log_level,
        colorize=True,
    )
