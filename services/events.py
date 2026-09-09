from services.minio_client import MinioClient
from services.objects import get_events_object_name
from app.config import (MINIO_EVENTS_BUCKET_NAME)

def events_load(minio_client: MinioClient):
    events_object_name = get_events_object_name()
    return minio_client.get_json(
        MINIO_EVENTS_BUCKET_NAME,
        events_object_name
    )