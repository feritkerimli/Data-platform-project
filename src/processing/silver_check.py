#%%
import sys
sys.path.append(r'C:\users\hp\desktop\farid\projects\praktika\data-platform-zip')
from src.processing.bronze_read import bronze_read
import pandas as pd
import numpy as np

def silver_check():
    all_data = bronze_read()
    customers = all_data['bronze/customers_dataset.csv']
    order_items = all_data['bronze/order_items_dataset.csv']
    order_payments = all_data['bronze/order_payments_dataset.csv']

    orders = all_data['bronze/orders_dataset.csv']
    sellers = all_data['bronze/sellers_dataset.csv']
    products = all_data['bronze/products_dataset.csv']

    # # --- Customers
    # print(customers.head())
    # print(display(customers.head()))  # this is for gui
    # print(customers.info())
    # # Checking for nulls
    # print(customers[customers['customer_id'].isnull()])
    # print(customers[customers['customer_unique_id'].isnull()])
    # print(customers[customers['customer_zip_code_prefix'].isnull()])
    # print(customers[customers['customer_city'].isnull()])
    # print(customers[customers['customer_state'].isnull()])
    # # Checking for duplicates
    # print(customers[customers.duplicated(subset= 'customer_id')].sort_values(by="customer_id"))
    # print(customers[customers.duplicated()].sort_values(by="customer_id"))
    # # Checking for standartization
    # print(customers['customer_zip_code_prefix'].unique())
    # print(customers['customer_city'].unique())
    # print(customers['customer_state'].unique()) 
    # print(customers[customers['customer_id'] != customers['customer_id'].str.strip()])
    # print(customers[customers['customer_unique_id'] != customers['customer_unique_id'].str.strip()])
    # print(customers[customers['customer_city'] != customers['customer_city'].str.strip()])
    # print(customers[customers['customer_state'] != customers['customer_state'].str.strip()])
    # customers['customer_id'] = customers['customer_id'].str.strip()

    # *************************
    customers['customer_city'] = customers['customer_city'].str.capitalize()
    # ********************
    # print(display(customers.head()))

    # --- Order items
    # print(display(order_items.head()))
    # print(order_items.info())
    # **********************
    order_items['price'] = np.where(order_items['price']<0,-1*order_items['price'],order_items['price'])
    order_items['freight_value'] = np.where(order_items['freight_value']<0,-1*order_items['freight_value'],order_items['freight_value'])
    # *******************
    # print(display(order_items.head()))
    # Checking for duplicates
    # print(order_items[order_items.duplicated()].sort_values('order_id'))
    
    # Checking for nulls
    # print(order_items[order_items['order_id'].isnull()])
    # print(order_items[order_items['order_item_id'].isnull()])
    # print(order_items[order_items['product_id'].isnull()])
    # print(order_items[order_items['seller_id'].isnull()])
    # print(order_items[order_items['shipping_limit_date'].isnull()])
    # print(order_items[order_items['price'].isnull()])
    # print(order_items[order_items['freight_value'].isnull()])
    
    # Checking for abnormal data
    # print(order_items[pd.to_datetime(order_items['shipping_limit_date'])<pd.to_datetime('1900-01-01 00:00:00')])
    # print(order_items[order_items['price']<=0])
    # print(order_items[order_items['freight_value']<0])
    


    # Order payments --------
    # print(display(order_payments.head()))
    # ******************
    order_payments['payment_type'] = np.where(order_payments['payment_type']=='not_defined','cancelled',order_payments['payment_type'])
    order_payments['payment_installments'] = np.where(order_payments['payment_installments']==0,1,order_payments['payment_installments'])

    # fixing non-sequential data
    order_payments = order_payments.sort_values(
        ['payment_sequential']
    )
    order_payments['payment_sequential'] = order_payments.groupby('order_id').cumcount() + 1
    # ********************
    

    # print(display(order_payments.head()))

    # checking for duplicates
    # print(order_payments[order_payments.duplicated()].sort_values('order_id'))

    # Checking for nulls
    # print(order_payments[order_payments['order_id'].isnull()])
    # print(order_payments[order_payments['payment_sequential'].isnull()])
    # print(order_payments[order_payments['payment_type'].isnull()])
    # print(order_payments[order_payments['payment_installments'].isnull()])
    # print(order_payments[order_payments['payment_value'].isnull()])
    
    # Checking for abnormal data
    # print(order_payments['payment_sequential'].unique())
    # print(order_payments['payment_type'].unique())
    # print(order_payments['payment_installments'].unique())
    # print(display(order_payments[order_payments['payment_value']<=0]))
    # print(order_payments[order_payments['payment_type']=='not_defined'])
    # print(order_payments[order_payments['payment_sequential']<=0])
    # print(display(order_payments[order_payments['payment_installments']<=0]))
    # print(order_payments[order_payments['order_id']=='744bade1fcf9ff3f31d860ace076d422'])
    # print(order_items[order_items['order_id']=='744bade1fcf9ff3f31d860ace076d422'])

    # non_sequential_check = order_payments.groupby('order_id')['payment_sequential'].apply(
    #     lambda x: sorted(x.tolist()) == list(range(1, len(x) + 1))
    # )

    # print(display(non_sequential_check[non_sequential_check == False]))

    # Orders -----------
    # print(display(orders.head()))

    # ********************
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
    # *******************
    # print(display(orders.head()))
    # print(display(orders[orders['order_id']=='dcb36b511fcac050b97cd5c05de84dc3']))

    # Checking for duplicates
    # print(orders[orders.duplicated(subset='order_id')].sort_values(by='order_id'))
    # print(orders[orders.duplicated()].sort_values(by='order_id'))

    # Checking for nulls
    # print(orders[orders['order_id'].isnull()])
    # print(orders[orders['customer_id'].isnull()])
    # print(orders[orders['order_status'].isnull()])
    # print(orders[orders['order_purchase_timestamp'].isnull()])
    # print(orders[orders['order_approved_at'].isnull()].to_string())
    # print(orders[orders['order_delivered_carrier_date'].isnull()])
    # print(orders[orders['order_delivered_customer_date'].isnull()])
    # print(orders[orders['order_estimated_delivery_date'].isnull()])

    # Checking for standartization
    # print(orders['order_status'].unique())
    # print(display(orders[orders['order_status'] == 'unavailable'].head()))

    # Checking for abnormal data
    # print(orders[pd.to_datetime(orders['order_purchase_timestamp'])>pd.Timestamp.now()])
    # print(orders[pd.to_datetime(orders['order_purchase_timestamp'])>pd.to_datetime(orders['order_approved_at'])])  
    # print(display(orders[pd.to_datetime(orders['order_approved_at'])>pd.to_datetime(orders['order_delivered_carrier_date'])].head()))
    # print(display(orders[pd.to_datetime(orders['order_delivered_carrier_date'])>pd.to_datetime(orders['order_delivered_customer_date'])].head()))
    # print(display(orders[pd.to_datetime(orders['order_delivered_customer_date'])>pd.to_datetime(orders['order_estimated_delivery_date'])].head()))

    # print(orders[pd.to_datetime(orders['order_purchase_timestamp'])>pd.to_datetime(orders['order_estimated_delivery_date'])].head().to_string())

    # Products
    # print(display(products.head()))
    # **************
    products['product_category_name'] = products['product_category_name'].str.capitalize()
    # ***************
    # print(display(products.head()))

    # Checking for nulls  
    # print(products[products['product_id'].isnull()])
    # print(products[products['product_category_name'].isnull()])
    # print(products[products['product_name_lenght'].isnull()])
    # print(products[products['product_description_lenght'].isnull()])
    # print(products[products['product_photos_qty'].isnull()])
    # print(products[products['product_weight_g'].isnull()])
    # print(products[products['product_length_cm'].isnull()])
    # print(products[products['product_height_cm'].isnull()])
    # print(products[products['product_width_cm'].isnull()])

    # Checking for duplicates
    # print(products[products.duplicated(subset='product_id')].sort_values(by='product_id'))

    # Checking for standartization
    # print(products['product_category_name'].unique())

    # Checking for abnormal data
    # print(products[products['product_name_lenght']<=0])
    # print(products[products['product_description_lenght']<=0])
    # print(products[products['product_photos_qty']<=0])
    # print(products[products['product_weight_g']<=0].to_string())
    # print(products[products['product_length_cm']<=0])
    # print(products[products['product_height_cm']<=0])
    # print(products[products['product_width_cm']<=0])

    # Sellers
    # print(display(sellers.head()))
    # ************
    sellers['seller_city'] = sellers['seller_city'].str.capitalize()
    # ***********
    # print(display(sellers.head()))
    # Checking for nulls
    # print(sellers[sellers['seller_id'].isnull()])
    # print(sellers[sellers['seller_zip_code_prefix'].isnull()])
    # print(sellers[sellers['seller_city'].isnull()])
    # print(sellers[sellers['seller_state'].isnull()])

    # Checking for duplicates
    # print(sellers[sellers.duplicated(subset='seller_id')].sort_values(by='seller_id'))
    return customers,order_items,order_payments,orders,products,sellers
    



    
    

    
    
if __name__ == "__main__":
    silver_check()