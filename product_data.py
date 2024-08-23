import pandas as pd
import numpy as np
import random
import mysql.connector as my
from dotenv import load_dotenv
import os



# Load environment variables from .env file
load_dotenv()

# Fetch database credentials from environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")




# Number of products
num_products = 50

# Generate product data
np.random.seed(42)
product_ids = [f"PROD{str(i).zfill(4)}" for i in range(1, num_products + 1)]
product_names = [f"Product {i}" for i in range(1, num_products + 1)]
categories = np.random.choice(['Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Sports'], size=num_products)
sub_categories = np.random.choice(['Gadgets', 'Apparel', 'Fiction', 'Appliances', 'Equipment'], size=num_products)
original_prices = np.round(np.random.uniform(10, 1000, size=num_products), 2)
selling_prices = np.round(original_prices - np.random.uniform(1, 50, size=num_products), 2)
stocks = np.random.randint(0, 100, size=num_products)

# Create a DataFrame
products_df = pd.DataFrame({
    'product_id': product_ids,
    'product_name': product_names,
    'category': categories,
    'sub_category': sub_categories,
    'original_price': original_prices,
    'selling_price': selling_prices,
    'stock': stocks
})

# Display the first few rows
print(products_df.head())

# Establish connection
con = my.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

# Create a cursor object
cursor = con.cursor()

# Create the product table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS product (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    original_price DECIMAL(10, 2),
    selling_price DECIMAL(10, 2),
    stock INT
);
"""
cursor.execute(create_table_query)

# Insert data into the table
# Insert data into the product table with update option for duplicates
for index, row in products_df.iterrows():
    insert_query = """
    INSERT INTO product (product_id, product_name, category, sub_category, original_price, selling_price, stock)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    product_name = VALUES(product_name),
    category = VALUES(category),
    sub_category = VALUES(sub_category),
    original_price = VALUES(original_price),
    selling_price = VALUES(selling_price),
    stock = VALUES(stock)
    """
    cursor.execute(insert_query, tuple(row))


# Commit the changes
con.commit()

# Close the cursor and connection
cursor.close()
con.close()

print("Data inserted successfully into 'product' table.")
