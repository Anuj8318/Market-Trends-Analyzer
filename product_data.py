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

# Predefined product items with actual names
product_data = [
    {"product_name": "Smartphone", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Laptop", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "T-shirt", "category": "Clothing", "sub_category": "Apparel"},
    {"product_name": "Blender", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Running Shoes", "category": "Sports", "sub_category": "Equipment"},
    {"product_name": "Tablet", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Jeans", "category": "Clothing", "sub_category": "Apparel"},
    {"product_name": "Non-Fiction Book", "category": "Books", "sub_category": "Fiction"},
    {"product_name": "Smartwatch", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Headphones", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Gaming Console", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Blender", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Coffee Maker", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Fiction Book", "category": "Books", "sub_category": "Fiction"},
    {"product_name": "Action Camera", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Basketball", "category": "Sports", "sub_category": "Equipment"},
    {"product_name": "Sneakers", "category": "Clothing", "sub_category": "Apparel"},
    {"product_name": "Vacuum Cleaner", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Yoga Mat", "category": "Sports", "sub_category": "Equipment"},
    {"product_name": "Electric Kettle", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Microwave Oven", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Cookware Set", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Cycling Helmet", "category": "Sports", "sub_category": "Equipment"},
    {"product_name": "Ski Goggles", "category": "Sports", "sub_category": "Equipment"},
    {"product_name": "Bluetooth Speaker", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Wireless Mouse", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Fitness Tracker", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "LED TV", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Smart Light Bulb", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Cordless Drill", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Graphic T-Shirt", "category": "Clothing", "sub_category": "Apparel"},
    {"product_name": "Baseball Glove", "category": "Sports", "sub_category": "Equipment"},
    {"product_name": "Electric Scooter", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Electric Toothbrush", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "3D Printer", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Drone", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Air Purifier", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Tennis Racket", "category": "Sports", "sub_category": "Equipment"},
    {"product_name": "Camera Lens", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Instant Pot", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Electric Grill", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Treadmill", "category": "Sports", "sub_category": "Equipment"},
    {"product_name": "Air Fryer", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Sound Bar", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Robot Vacuum", "category": "Home & Kitchen", "sub_category": "Appliances"},
    {"product_name": "Virtual Reality Headset", "category": "Electronics", "sub_category": "Gadgets"},
    {"product_name": "Mountain Bike", "category": "Sports", "sub_category": "Equipment"},
    {"product_name": "Electric Shaver", "category": "Home & Kitchen", "sub_category": "Appliances"},
]

# Expand product data to 50 items
product_data_expanded = (product_data * (num_products // len(product_data) + 1))[:num_products]

# Generate product IDs
product_ids = [f"PROD{str(i).zfill(4)}" for i in range(1, num_products + 1)]

# Generate random prices and stock levels
np.random.seed(42)
original_prices = np.round(np.random.uniform(10, 1000, size=num_products), 2)
selling_prices = np.round(original_prices - np.random.uniform(1, 50, size=num_products), 2)
stocks = np.random.randint(0, 100, size=num_products)

# Create a DataFrame
products_df = pd.DataFrame({
    'product_id': product_ids,
    'product_name': [item['product_name'] for item in product_data_expanded],
    'category': [item['category'] for item in product_data_expanded],
    'sub_category': [item['sub_category'] for item in product_data_expanded],
    'original_price': original_prices,
    'selling_price': selling_prices,
    'stock': stocks
})

# Display the first few rows
print(products_df.head())

# Establish connection to MySQL
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

# Insert data into the product table
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
