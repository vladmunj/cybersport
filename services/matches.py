from services.minio_client import MinioClient
from datetime import datetime
from app.config import (MINIO_MATCHES_BUCKET_NAME)

def matches_load(minio_client: MinioClient):
    object_date = datetime.now().strftime('%Y-%m-%d')
    return minio_client.objects_list(MINIO_MATCHES_BUCKET_NAME, object_date + "/")