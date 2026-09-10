from datetime import datetime
from app.config import (MINIO_MATCHES_BUCKET_NAME)

def matches_load(minio_client):
    object_date = datetime.now().strftime('%Y-%m-%d')
    return minio_client.objects_list(MINIO_MATCHES_BUCKET_NAME, object_date + "/")