MINIO_CONFIG = {
    "endpoint": "localhost:9000",
    "access_key": "minio",
    "secret_key": "minio12345",
    "secure": False,
    "bucket_name": "data-lake"
}


POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "user": "admin",
    "password": "admin",
    "database": "warehouse"
}

DATA_PATH = "data"
BUCKET = "data-lake"
