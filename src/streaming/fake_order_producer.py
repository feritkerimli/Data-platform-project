from kafka import KafkaProducer
import json
import time
import random
import string
from datetime import datetime, timedelta
from src.processing.silver_read import silver_read
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
def fake_order_stream():
    all_data = silver_read()
    customers = all_data['silver/customers.csv']
    order_items = all_data['silver/order_items.csv']
    fake_order_id = ''.join(random.choices(string.ascii_lowercase, k=5))
    while True:
        for i in range(5):
            order_id = fake_order_id + str(i)
            order_item_random_row = order_items.sample().iloc[0]
            message = {
                "order": {
                    "order_id": order_id,
                    "customer_id": customers['customer_id'].sample().iloc[0],
                    "order_status": "invoiced",
                    "order_purchase_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "order_estimated_delivery_date": (
                        datetime.now() + timedelta(days=20)
                    ).strftime("%Y-%m-%d %H:%M:%S")
                },
                "item": {
                    "order_id": order_id,
                    "product_id": order_item_random_row['product_id'],
                    "seller_id": order_item_random_row['seller_id'],
                    "price": float(order_item_random_row['price']),
                    "freight_value": float(order_item_random_row['freight_value'])
                },
                "payment": {
                    "order_id": order_id,
                    "payment_type": "debit_card",
                    "payment_value": float(
                        order_item_random_row['price'] +
                        order_item_random_row['freight_value']
                    )
                }
            }
            producer.send('orders-topic', message)
            print("Produced:", order_id)
        producer.flush()
        time.sleep(5)

if __name__ == "__main__":
    fake_order_stream()
    