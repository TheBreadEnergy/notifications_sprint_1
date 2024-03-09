from datetime import datetime, timedelta


def serialize_datetime(obj):
    print(obj, type(obj).__name__)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return obj.total_seconds()
