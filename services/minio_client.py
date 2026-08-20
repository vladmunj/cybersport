from services.json_transform import json_prepare, json_load
from io import BytesIO
from minio import Minio
from app.config import MINIO_HOST, MINIO_USER, MINIO_PASSWORD
from exceptions.minio import MinioException

class MinioClient:
    def __init__(self):
        try:
            self.client = Minio(
                MINIO_HOST,
                access_key=MINIO_USER,
                secret_key=MINIO_PASSWORD,
                secure=False
            )
        except Exception as e:
            raise MinioException(e) from e

    def __set_bucket(self, bucket_name):
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
        except Exception as e:
            raise MinioException(e) from e

    def upload_json(self, bucket_name, data, object_name):
        self.__set_bucket(bucket_name)
        json_data = json_prepare(data)
        try:
            self.client.put_object(
                bucket_name,
                object_name,
                BytesIO(json_data),
                length=len(json_data),
                content_type="application/json"
            )
        except Exception as e:
            raise MinioException(e) from e

    def get_json(self, bucket_name, object_name):
        try:
            response = self.client.get_object(bucket_name, object_name)
        except Exception as e:
            raise MinioException(e) from e
        return json_load(response)

    def objects_list(self, bucket_name, prefix = ""):
        try:
            return self.client.list_objects(
                bucket_name,
                prefix=prefix,
                recursive=True
            )
        except Exception as e:
            raise MinioException(e) from e