import sqlite3

#creating connection with database
conn = sqlite3.connect("medical_shop.db")

cursor = conn.cursor()

#creating Category table
cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT
)""")

#creating medicines table
cursor.execute("""
               CREATE TABLE IF NOT EXISTS medicines(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   category_id INTEGER,
                   batch_number TEXT ,
                   expiry_date TEXT,
                   cost_price REAL,
                   selling_price REAL,
                   units_per_strip INTEGER,
                   stock_quantity INTEGER)""")

#creating sales table
cursor.execute("""
               CREATE TABLE IF NOT EXISTS sale_items(
                   item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   sale_id INTEGER,
                   medicine_id INTEGER,
                   quantity INTEGER,
                   total_price REAL)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    sale_date TEXT
)
""")

conn.commit()
conn.close()

print("tables and database created sucessfully!!")