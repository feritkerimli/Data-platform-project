import pandas as pd
import random
import string
from datetime import datetime,timedelta
from src.processing.silver_read import silver_read


def fake_order():
    all_data = silver_read()
    customers = all_data['silver/customers.csv']
    order_items = all_data['silver/order_items.csv']
    order_payments = all_data['silver/order_payments.csv']
    orders = all_data['silver/orders.csv']
    sellers = all_data['silver/sellers.csv']
    products = all_data['silver/products.csv']

    fake_order_df = pd.DataFrame({
        "order_id":[],
        "customer_id":[],
        "order_status":[],
        "order_purchase_timestamp":[],
        "order_approved_at":[],
        "order_delivered_carrier_date":[],
        "order_delivered_customer_date":[],
        "order_estimated_delivery_date":[]
    })
    fake_order_items_df = pd.DataFrame({
        "order_id":[],
        "order_item_id":[],
        "product_id":[],
        "seller_id":[],
        "shipping_limit_date":[],
        "price":[],
        "freight_value":[]
    })
    fake_order_payments_df= pd.DataFrame({
        "order_id":[],
        "payment_sequential":[],
        "payment_type":[],
        "payment_installments":[],
        "payment_value":[]
    })
    fake_order_id = ''.join(random.choices(string.ascii_lowercase, k=5))
    for i in range(50):
        fake_order_df.loc[len(fake_order_df)] = [fake_order_id+str(i),customers['customer_id'].sample().iloc[0],'invoiced',datetime.now().strftime("%Y-%m-%d %H:%M:%S"),None,None,None,(datetime.now()+timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S")]
        order_item_random_row = order_items.sample().iloc[0]
        fake_order_items_df.loc[len(fake_order_items_df)] = [fake_order_df['order_id'].iloc[-1],1,order_item_random_row['product_id'],order_item_random_row['seller_id'],None,order_item_random_row['price'],order_item_random_row['freight_value']]
        fake_order_payments_df.loc[len(fake_order_payments_df)] = [fake_order_df['order_id'].iloc[-1],1,'debit_card',1,order_item_random_row['price']+order_item_random_row['freight_value']]

    orders = pd.concat([orders, fake_order_df], ignore_index=True)
    order_items = pd.concat([order_items, fake_order_items_df], ignore_index=True)
    order_payments = pd.concat([order_payments, fake_order_payments_df], ignore_index=True)
    return customers,order_items,order_payments,orders,products,sellers

    

