import mysql.connector as my
from customer_data import customers_df
from product_data import products_df
import pandas as pd
import numpy as np
import random
from dotenv import load_dotenv
import os




# Load environment variables from .env file
load_dotenv()

# Fetch database credentials from environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Number of orders
num_orders = 200

# Generate order data
np.random.seed(42)
order_ids = np.arange(1, num_orders + 1)
customer_ids = np.random.choice(customers_df['customer_id'], size=num_orders)
product_ids = np.random.choice(products_df['product_id'], size=num_orders)
quantities = np.random.randint(1, 10, size=num_orders)
total_prices = quantities * np.random.choice(products_df['selling_price'], size=num_orders)
payment_modes = np.random.choice(['Credit Card', 'PayPal', 'Cash on Delivery'], size=num_orders)
order_dates = pd.date_range(start='2022-01-01', periods=num_orders, freq='D')
order_statuses = np.random.choice(['Pending', 'Delivered', 'Shipped', 'Cancelled'], size=num_orders)

# Create a DataFrame
orders_df = pd.DataFrame({
    'order_id': order_ids,
    'customer_id': customer_ids,
    'product_id': product_ids,
    'quantity': quantities,
    'total_price': total_prices,
    'payment_mode': payment_modes,
    'order_date': order_dates,
    'order_status': order_statuses
})

# Display the first few rows
print(orders_df.head())

# Establish connection
con = my.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
# Create a cursor object
cursor = con.cursor()

# Create the orders table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id VARCHAR(10),
    product_id VARCHAR(10),
    quantity INT,
    total_price DECIMAL(10, 2),
    payment_mode VARCHAR(50),
    order_date DATE,
    order_status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
"""
cursor.execute(create_table_query)

# Insert data into the orders table
for index, row in orders_df.iterrows():
    insert_query = """
    INSERT INTO orders (order_id, customer_id, product_id, quantity, total_price, payment_mode, order_date, order_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, tuple(row))

# Commit the changes
con.commit()

# Close the cursor and connection
cursor.close()
con.close()

print("Data inserted successfully into 'orders' table.")
