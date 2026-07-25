from src.processing.bronze_read import bronze_read
import pandas as pd
import numpy as np

def silver_transform():
    all_data = bronze_read()
    customers = all_data['bronze/customers_dataset.csv']
    order_items = all_data['bronze/order_items_dataset.csv']
    order_payments = all_data['bronze/order_payments_dataset.csv']

    orders = all_data['bronze/orders_dataset.csv']
    sellers = all_data['bronze/sellers_dataset.csv']
    products = all_data['bronze/products_dataset.csv']

    # # --- Customers
    customers['customer_city'] = customers['customer_city'].str.capitalize()
    
    # Orders (because we need merge to fix customer_unique_id problem)
    orders = pd.merge(orders,customers,how='left',on='customer_id')    
    orders = orders[['order_id','customer_unique_id',"order_status","order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]] 
    orders.rename(columns={'customer_unique_id': 'customer_id'}, inplace=True)
    # Then fix the customers
    customers.drop('customer_id', axis=1, inplace=True)
    customers.drop_duplicates(inplace=True)
    customers.rename(columns={'customer_unique_id': 'customer_id'}, inplace=True)
    

    # --- Order items
    order_items['price'] = np.where(order_items['price']<0,-1*order_items['price'],order_items['price'])
    order_items['freight_value'] = np.where(order_items['freight_value']<0,-1*order_items['freight_value'],order_items['freight_value'])
   
    


    # Order payments --------
    order_payments['payment_type'] = np.where(order_payments['payment_type']=='not_defined','cancelled',order_payments['payment_type'])
    order_payments['payment_installments'] = np.where(order_payments['payment_installments']==0,1,order_payments['payment_installments'])

    # fixing non-sequential data
    order_payments = order_payments.sort_values(
        ['payment_sequential']
    )
    order_payments['payment_sequential'] = order_payments.groupby('order_id').cumcount() + 1
    

    # Orders -----------
    orders['order_approved_at'],orders['order_delivered_carrier_date'] = np.where(
        pd.to_datetime(orders['order_approved_at'])>pd.to_datetime(orders['order_delivered_carrier_date']),
        [orders['order_delivered_carrier_date'],orders['order_approved_at']],
        [orders['order_approved_at'],orders['order_delivered_carrier_date']]
    )
    orders['order_delivered_carrier_date'],orders['order_delivered_customer_date'] = np.where(
        pd.to_datetime(orders['order_delivered_carrier_date'])>pd.to_datetime(orders['order_delivered_customer_date']),
        [orders['order_delivered_customer_date'],orders['order_delivered_carrier_date']],
        [orders['order_delivered_carrier_date'],orders['order_delivered_customer_date'] ]
    )

    orders['order_delivered_customer_date'],orders['order_estimated_delivery_date'] = np.where(
        pd.to_datetime(orders['order_delivered_customer_date'])>pd.to_datetime(orders['order_estimated_delivery_date']),
        [orders['order_estimated_delivery_date'],orders['order_delivered_customer_date']],
        [orders['order_delivered_customer_date'],orders['order_estimated_delivery_date']]
    )
    

    # Products
    products['product_category_name'] = products['product_category_name'].str.capitalize()
    

    # Sellers
    sellers['seller_city'] = sellers['seller_city'].str.capitalize()
    
    return customers,order_items,order_payments,orders,products,sellers