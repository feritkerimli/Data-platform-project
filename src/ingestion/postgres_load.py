import pandas as pd
from sqlalchemy import text
from src.storage.postgre_client import get_postgres_engine
from src.processing.gold_read import gold_read

def postgres_load():
    engine = get_postgres_engine()

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE fact_orders;"))
        conn.execute(text("TRUNCATE TABLE dim_customer;"))
        conn.execute(text("TRUNCATE TABLE dim_product;"))
        conn.execute(text("TRUNCATE TABLE dim_seller;"))
        conn.execute(text("TRUNCATE TABLE dim_date;"))
    

    all_data = gold_read()
    dim_customer = all_data['gold/dim_customers.csv']
    dim_date = all_data["gold/dim_date.csv"]
    dim_product = all_data["gold/dim_products.csv"]
    dim_seller = all_data["gold/dim_sellers.csv"]
    fact_orders = all_data["gold/fact_orders.csv"]

    
    dim_customer.to_sql(
        name="dim_customer",
        con=engine,
        if_exists="append",   
        index=False
    )

    dim_date.to_sql(
        name="dim_date",
        con=engine,
        if_exists="append",
        index=False
    )

    dim_product.to_sql(
        name="dim_product",
        con=engine,
        if_exists="append",
        index=False
    )

    dim_seller.to_sql(
        name="dim_seller",
        con=engine,
        if_exists="append",
        index=False
    )

    fact_orders.to_sql(
        name="fact_orders",
        con=engine,
        if_exists="append",
        index=False
    )


    print("Loaded to postgres successfully")