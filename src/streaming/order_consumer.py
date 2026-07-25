from kafka import KafkaConsumer
import json
import pandas as pd
from src.processing.silver_read import silver_read
from src.ingestion.silver_load_fake_consumers import silver_load_fake_consumers
from src.ingestion.gold_load import gold_load
from src.ingestion.postgres_load import postgres_load


consumer = KafkaConsumer(
    'orders-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='orders-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:

    data = message.value

    fake_order_df = pd.DataFrame([data["order"]])
    fake_order_items_df = pd.DataFrame([data["item"]])
    fake_order_payments_df = pd.DataFrame([data["payment"]])

    all_data = silver_read()
    customers = all_data['silver/customers.csv']
    order_items = all_data['silver/order_items.csv']
    order_payments = all_data['silver/order_payments.csv']
    orders = all_data['silver/orders.csv']
    sellers = all_data['silver/sellers.csv']
    products = all_data['silver/products.csv']

    orders = pd.concat([orders, fake_order_df], ignore_index=True)
    order_items = pd.concat([order_items, fake_order_items_df], ignore_index=True)
    order_payments = pd.concat([order_payments, fake_order_payments_df], ignore_index=True)
    silver_load_fake_consumers(customers,order_items,order_payments,orders,products,sellers)
    gold_load()
    postgres_load()

    print(fake_order_df)
    print(fake_order_items_df)
    print(fake_order_payments_df)
