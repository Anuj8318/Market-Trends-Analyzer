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

# Define the number of customers to generate
num_customers = 100

# Generate random customer data
customer_ids = [f"CUST{str(i).zfill(4)}" for i in range(1, num_customers + 1)]
names = [f"Customer {i}" for i in range(1, num_customers + 1)]
cities = np.random.choice(['Phoenix', 'Houston', 'Chicago'], num_customers)
emails = [f"customer{i}@example.com" for i in range(1, num_customers + 1)]
phone_numbers = [f"{random.randint(1000000000, 9999999999)}" for i in range(num_customers)]
addresses = [f"{random.randint(100, 999)} Main St" for i in range(num_customers)]
pin_codes = [random.randint(10000, 99999) for i in range(num_customers)]

# Create a DataFrame
customers_df = pd.DataFrame({
    'customer_id': customer_ids,
    'name': names,
    'city': cities,
    'email': emails,
    'phone_no': phone_numbers,
    'address': addresses,
    'pin_code': pin_codes
})

# print(customers_df)

# Establish connection
con = my.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

# Create a cursor object
cursor = con.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS customer (
 `customer_id` varchar(10) NOT NULL,
 `name` varchar(100) NOT NULL,
 `city` varchar(65) NOT NULL,
 `email` varchar(45) NOT NULL,
 `phone_no` varchar(15) NOT NULL,
 `address` varchar(100) NOT NULL,
 `pin_code` int NOT NULL,
 PRIMARY KEY(`customer_id`)
 ) ;
"""
cursor.execute(create_table_query)

# Insert data into the table
for index, row in customers_df.iterrows():
    insert_query = """
    INSERT INTO customer (customer_id, name, city, email, phone_no, address, pin_code)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    city = VALUES(city),
    email = VALUES(email),
    phone_no = VALUES(phone_no),
    address = VALUES(address),
    pin_code = VALUES(pin_code)
    """
    cursor.execute(insert_query, tuple(row))

# Commit the changes
con.commit()

# Close the cursor and connection
cursor.close()
con.close()

print("Data inserted successfully into 'customer' table.")










# check this code after project completion 


# # Create the connection string
# connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"

# # Create an SQLAlchemy engine
# try:
#     engine = create_engine(connection_string)
    
#     # Test connection
#     with engine.connect() as connection:
#         print("Connected to MySQL successfully!")

#     # Insert the DataFrame into the database
#     customers_df.to_sql('customer', con=engine, if_exists='replace', index=False)
#     print("Data inserted successfully into 'customer' table.")

# except pymysql.err.OperationalError as e:
#     print(f"OperationalError: {e}")
#     print("Failed to connect to the MySQL database. Please check your credentials, MySQL server status, or connection details.")
# except Exception as e:
#     print(f"An error occurred: {e}")




# import mysql.connector as my 

# # Connect to MySQL server
# con = my.connect(
#     host="localhost",
#     user="root",
#     password="8318AnujSingh@",
#     database='ecommerce'  # Connect to the existing 'xyz' database
# )

# cr = con.cursor()
# cr.execute("INSERT INTO customer VALUES (1, 'aniket', 'xyc','aniket@gmail.com','123456433','lotus pride','123')")
# con.commit()