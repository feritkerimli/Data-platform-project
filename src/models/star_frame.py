from src.processing.silver_read import silver_read
import pandas as pd
import numpy as np

def gold_model():
    all_data = silver_read()
    dim_customers = all_data['silver/customers.csv']
    order_items = all_data['silver/order_items.csv']
    order_payments = all_data['silver/order_payments.csv']

    orders = all_data['silver/orders.csv']
    dim_sellers = all_data['silver/sellers.csv']
    dim_products = all_data['silver/products.csv']

    # Dim Customer
    dim_customers.rename(columns=
        {
        'customer_zip_code_prefix': 'zip_code',
        'customer_city':'city',
        'customer_state':'state'
        }, inplace=True)

    dim_customers = dim_customers[['customer_id','city','state','zip_code']]

    # Dim Product
    dim_products.rename(columns=
        {
        'product_category_name': 'category',
        'product_weight_g':'weight_g',
        }, inplace=True)
    dim_products = dim_products[['product_id','category','weight_g']]
    # Dim Seller
    dim_sellers.rename(columns=
        {
        'seller_city': 'city',
        'seller_zip_code_prefix':'zip_code',
        'seller_state':'state'
        }, inplace=True)
    dim_sellers = dim_sellers[['seller_id','city','state','zip_code']]

    # Fact table
    fact_orders = pd.merge(order_items,orders,how='left',on='order_id')
    fact_orders = fact_orders[['order_id','order_item_id','customer_id','product_id','seller_id','order_purchase_timestamp','order_estimated_delivery_date','price','freight_value']]
    fact_orders['revenue'] = fact_orders['price'] + fact_orders['freight_value']
    fact_orders.rename(columns={
        'order_purchase_timestamp': 'order_ts',
        'order_estimated_delivery_date':'delivered_ts'
        }, inplace=True)
    # Dim Date
    dates = pd.concat([
        pd.to_datetime(fact_orders['order_ts'],format='mixed'),
        pd.to_datetime(fact_orders['delivered_ts'],format='mixed')
    ])

    dates = dates.dropna()
    dates = dates.dt.date.drop_duplicates()

    dim_date = pd.DataFrame({
        'date': dates
    })

    dim_date['year'] = pd.to_datetime(dim_date['date']).dt.year
    dim_date['month'] = pd.to_datetime(dim_date['date']).dt.month
    dim_date['day'] = pd.to_datetime(dim_date['date']).dt.day
    dim_date['week'] = pd.to_datetime(dim_date['date']).dt.isocalendar().week

    

    return dim_customers,dim_products,dim_sellers,dim_date,fact_orders
