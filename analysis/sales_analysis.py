import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def sales_summary():

    conn = sqlite3.connect("medical_shop.db")

    query = """
    SELECT s.sale_id, m.name, s.quantity, s.total_price, s.sale_Date
    FROM sales s
    JOIN medicines m ON s.medicine_id = m.id
    """

    df = pd.read_sql_query(query,conn)

    print("\n📊 Sales Data:")
    print(df)

    print("\n💰 Total Revenue:")
    print(df["total_price"].sum())

    print("\n🔥 Top Selling Medicines:")
    top_meds = df.groupby("name")["quantity"].sum().sort_values(ascending = False)
    print(top_meds)
    
    # 📊 BAR CHART — Top Medicines
    top_meds.plot(kind = "bar")
    plt.title("Top selling medicines")
    plt.xlabel("Medicines")
    plt.ylabel("Quantity Sold")
    plt.show()
    
    # 📅 Sales per Da
    daily_sales = df.groupby("sale_date")["total_price"].sum()
    daily_sales.plot(kind = "line")
    plt.title("Daily Sales")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.show()

    conn.close()
    
def category_sales():
    conn = sqlite3.connect("medical_shop.db")
    
    query = """
    SELECT c.category_name, SUM(s.total_price) AS total_sales
    FROM sales s
    JOIN medicines m ON s.medicine_id = m.id
    JOIN categories c ON m.category_id = c.category_id
    """
    df = pd.read_sql_query(query,conn)
    
    print("\n📊 Category-wise Sales:\n")
    print(df)
    
    df.set_index("category_name")["total_sales"].plot(kind = "bar")
    plt.title("Category wise sales")
    plt.xlabel("Category name")
    plt.ylabel("total sales")
    plt.show()
    
    conn.close()
    
def profit_analysis():
    conn = sqlite3.connect("medical_shop.db")
    
    query = """
    SELECT m.name,
    s.quantity,
    m.cost_price,
    m.selling_price,
    (m.selling_price - m.cost_price) * s.quantity AS profit
    FROM sales s
    JOIN medicines m ON s.medicine_id = m.id
    """
    df = pd.read_sql_query(query, conn)
    
    print("\n💰 Profit Data:\n")
    print(df)

    total_profit = df["profit"].sum()
    print("\n🔥 Total Profit:", total_profit)
    
    profit_by_medicine = df.groupby('name')["profit"].sum()
    
    profit_by_medicine.plot(kind = "bar")
    plt.title("Profit by each medicine")
    plt.xlabel("Medicine")
    plt.ylabel("Profit")
    plt.xticks(rotation=30)
    plt.show()
    
    conn.close()
    
    
def monthly_sales_trend():
    conn = sqlite3.connect("medical_shop.db")
    
    
    query = """
    SELECT sale_date,
    total_price
    FROM sales
    """
    
    df = pd.read_sql_query(query, conn)
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    # ✅ Extract month
    df["month"] = df["sale_date"].dt.to_period("M")

    # ✅ Group by month
    monthly_sales = df.groupby("month")["total_price"].sum()
    
    print("\n📅 Monthly Sales:\n")
    print(monthly_sales)
    
    monthly_sales.plot(kind="line", marker = "o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("month")
    plt.ylabel("total sales")
    plt.xticks(rotation = 30)
    plt.grid()
    plt.show()
    
    conn.close()