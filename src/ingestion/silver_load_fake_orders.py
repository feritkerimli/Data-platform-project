from src.storage.minio_client import get_minio_client
from src.config.config import BUCKET
from src.streaming.fake_order import fake_order
import io

def silver_load_fake_orders():
    client = get_minio_client()
    bucket = BUCKET

    customers,order_items,order_payments,orders,products,sellers= fake_order()

    def upload_df(df, name):
        data = df.to_csv(index=False).encode("utf-8")
        buffer = io.BytesIO(data)

        object_name = f"silver/{name}.csv"

        client.put_object(
            bucket_name=bucket,
            object_name=object_name,
            data=buffer,
            length=len(data),
            content_type="text/csv"
        )

        print(f"{name}.csv uploaded to MinIO as {object_name}")

    upload_df(customers, "customers")
    upload_df(order_items, "order_items")
    upload_df(order_payments, "order_payments")
    upload_df(orders, "orders")
    upload_df(products, "products")
    upload_df(sellers, "sellers")
    