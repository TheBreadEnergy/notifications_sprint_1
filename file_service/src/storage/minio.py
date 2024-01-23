from miniopy_async import Minio

minio_client: Minio | None = None


def get_minio() -> Minio | None:
    return minio_client
