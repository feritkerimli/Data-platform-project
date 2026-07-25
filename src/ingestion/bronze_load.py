from src.storage.minio_client import get_minio_client
from src.config.config import DATA_PATH ,BUCKET
import os

def bronze_load():
    client = get_minio_client()
    bucket = BUCKET
    data_path = DATA_PATH

    for file in os.listdir(data_path):
        file_path = os.path.join(data_path, file)
        object_name = f"bronze/{file}"

        client.fput_object(
            bucket_name=bucket,   # bucket name
            object_name=object_name,  # file name in minio
            file_path=file_path   # local file path
        )
        print(f"{file} uploaded to MinIO as {object_name}")
