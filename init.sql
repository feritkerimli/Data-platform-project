CREATE TABLE IF NOT EXISTS fact_orders (
    order_id TEXT,
    order_item_id INT,
    customer_id TEXT,
    product_id TEXT,
    seller_id TEXT,
    order_ts TEXT,
    delivered_ts TEXT,
    price FLOAT,
    freight_value FLOAT,
    revenue FLOAT
);
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
);
CREATE TABLE IF NOT EXISTS dim_product (
    product_id TEXT,
    category TEXT,
    weight_g FLOAT
);
CREATE TABLE IF NOT EXISTS dim_seller (
    seller_id TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
);
CREATE TABLE IF NOT EXISTS dim_date (
    date TEXT,
    year INT,
    month INT,
    day INT,
    week INT
);
