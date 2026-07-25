from minio import Minio
from src.config.config import MINIO_CONFIG

def get_minio_client():
    return Minio(
        MINIO_CONFIG["endpoint"],
        access_key=MINIO_CONFIG["access_key"],
        secret_key=MINIO_CONFIG["secret_key"],
        secure=MINIO_CONFIG["secure"]
    )
