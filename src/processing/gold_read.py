from src.storage.minio_client import get_minio_client
from src.processing.minio_read import minio_read
from src.config.config import BUCKET
import pandas as pd

def gold_read():
    client = get_minio_client()
    folder = "gold/"
    objects = client.list_objects(BUCKET, prefix=folder, recursive=True)
    all_df = {}
    for obj in objects:
        df = minio_read(obj.object_name)
        print(f"Processing: {obj.object_name}")
        all_df[obj.object_name] = df
    return all_df

