import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd


def open_reports_window():

    win = tk.Toplevel()
    win.title("Reports Dashboard")
    win.geometry("700x500")

    # ---------------- TABLE ----------------
    tree = ttk.Treeview(win)
    tree.pack(fill="both", expand=True)

    # ---------------- FUNCTIONS ----------------

    def clear_table():
        tree.delete(*tree.get_children())

    def load_table(df):
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        for col in df.columns:
            tree.heading(col, text=col)

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    # ---------------- REPORT FUNCTIONS ----------------

    def show_total_revenue():
        clear_table()

        conn = sqlite3.connect("medical_shop.db")
        df = pd.read_sql_query(
            "SELECT SUM(total_price) as revenue FROM sales", conn)
        conn.close()

        load_table(df)

    def show_top_selling():
        clear_table()

        conn = sqlite3.connect("medical_shop.db")
        df = pd.read_sql_query("""
        SELECT m.name, SUM(s.quantity) as total_qty
        FROM sales s
        JOIN medicines m ON s.medicine_id = m.id
        GROUP BY m.name
        ORDER BY total_qty DESC
        """, conn)
        conn.close()

        load_table(df)

    def show_category_sales():
        clear_table()

        conn = sqlite3.connect("medical_shop.db")
        df = pd.read_sql_query("""
        SELECT c.category_name, SUM(s.total_price) as total_sales
        FROM sales s
        JOIN medicines m ON s.medicine_id = m.id
        JOIN categories c ON m.category_id = c.category_id
        GROUP BY c.category_name
        """, conn)
        conn.close()

        load_table(df)

    def show_monthly_sales():
        clear_table()

        conn = sqlite3.connect("medical_shop.db")
        df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', sale_date) as month,
               SUM(total_price) as total_sales
        FROM sales
        GROUP BY month
        """, conn)
        conn.close()

        load_table(df)

    def show_expiry_alert():
        clear_table()

        conn = sqlite3.connect("medical_shop.db")
        df = pd.read_sql_query("""
        SELECT name, stock_quantity, expiry_date
        FROM medicines
        WHERE expiry_date <= date('now', '+30 days')
        ORDER BY expiry_date ASC
        """, conn)
        conn.close()

        if df.empty:
            tree["columns"] = ["Message"]
            tree["show"] = "headings"
            tree.heading("Message", text="Message")
            tree.insert("", "end",
                        values=["No medicines nearing expiry"])
            return

        load_table(df)

    # ---------------- BUTTONS ----------------

    tk.Button(win, text="Total Revenue",
              command=show_total_revenue).pack(pady=5)

    tk.Button(win, text="Top Selling",
              command=show_top_selling).pack(pady=5)

    tk.Button(win, text="Category Sales",
              command=show_category_sales).pack(pady=5)

    tk.Button(win, text="Monthly Sales",
              command=show_monthly_sales).pack(pady=5)

    tk.Button(win, text="Expiry Alert",
              command=show_expiry_alert).pack(pady=5)