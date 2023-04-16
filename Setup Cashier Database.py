"""
This module will create the "Cashier.db" 
as a local database saved on a file.

Run this module before using the "Cashier.py"
You only need to run this module once to create the needed table

If you run this module more than once it will return error 
saying that the mentioned table is already exist. If that happen 
you can just leave it and go ahead use the "Cashier.py"
"""
# Import sqlite3 library to setup a SQL based database 
import sqlite3

""" Creating local file "Cashier.db", 
    if the file already exist it will connect this module to it """
conn = sqlite3.connect('Cashier.db')

# Check if the connection successfully established
print ("Opened database successfully")

# Creating the user_info table, will return as error if table already exist
conn.execute('''CREATE TABLE user_info (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         user TEXT NOT NULL,
         date DATE NOT NULL)''')

# Check if the table successfully created
print ("user_info table created successfully")

# Creating the orders_detail table, will return as error if table already exist
conn.execute('''CREATE TABLE orders_detail (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         user TEXT NOT NULL,
         item TEXT NOT NULL,
         qty INTEGER NOT NULL,
         price REAL NOT NULL,
         total_price REAL NOT NULL,
         discount REAL NOT NULL,
         price_after_discount REAL NOT NULL)''')

# Check if the table successfully created
print ("orders_detail table created successfully")

# Disconnect from database
conn.close()
