from sqlalchemy import create_engine
from src.config.config import POSTGRES_CONFIG

def get_postgres_engine():
    user = POSTGRES_CONFIG["user"]
    password = POSTGRES_CONFIG["password"]
    host = POSTGRES_CONFIG["host"]
    port = POSTGRES_CONFIG["port"]
    db = POSTGRES_CONFIG["database"]
    
    # SQLAlchemy connection string
    conn_str = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(conn_str)
    return engine