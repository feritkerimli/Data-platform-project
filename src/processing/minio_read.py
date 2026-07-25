import pandas as pd
from io import BytesIO
from src.storage.minio_client import get_minio_client
from src.config.config import BUCKET

def minio_read(file_name):
    client = get_minio_client()
    response = client.get_object(BUCKET, f"{file_name}")
    df= pd.read_csv(BytesIO(response.read()))
    response.close()
    response.release_conn()
    return df