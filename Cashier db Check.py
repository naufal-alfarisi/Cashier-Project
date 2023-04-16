"""
This module can used to check wether the checked out
orders is successfully inserted to the database or not
by creating a query to extract the data from the database
"""

# Import necessary library
import sqlite3
from tabulate import tabulate

# Creating connection to the 'Cashier.db' file
conn = sqlite3.connect('Cashier.db')
cursor = conn.cursor()

# Execute SQL query to select all columns from a table

# Choose this to select everything from user_info table
query1 = "SELECT * FROM user_info" 

# Choose this to select everything from orders_detail table
query2 = "SELECT * FROM orders_detail"

# Execute the query
cursor.execute(query2)

# Fetch the column names
column_names = [description[0] for description in cursor.description]

# Fetch the results
results = cursor.fetchall()

# Print the fetched results and column names as headers
print(tabulate(results, headers= column_names))

# Close the cursor and connection
cursor.close()
conn.close()