from src.storage.minio_client import get_minio_client
from src.config.config import BUCKET
from src.models.star_frame import gold_model
import io

def gold_load():
    client = get_minio_client()
    bucket = BUCKET

    dim_customers,dim_products,dim_sellers,dim_date,fact_orders = gold_model()

    def upload_df(df, name):
        data = df.to_csv(index=False).encode("utf-8")
        buffer = io.BytesIO(data)

        object_name = f"gold/{name}.csv"

        client.put_object(
            bucket_name=bucket,
            object_name=object_name,
            data=buffer,
            length=len(data),
            content_type="text/csv"
        )

        print(f"{name}.csv uploaded to MinIO as {object_name}")

    upload_df(dim_customers, "dim_customers")
    upload_df(fact_orders, "fact_orders")
    upload_df(dim_products, "dim_products")
    upload_df(dim_sellers, "dim_sellers")
    upload_df(dim_date, "dim_date")
    