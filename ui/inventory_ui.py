import tkinter as tk
from tkinter import messagebox
import sqlite3


def open_add_medicine_window():

    win = tk.Toplevel()
    win.title("Add Medicine")
    win.geometry("400x500")

    # ---------------- FUNCTIONS ----------------

    def load_categories():
        conn = sqlite3.connect("medical_shop.db")
        cursor = conn.cursor()

        cursor.execute("SELECT category_id, category_name FROM categories")
        categories = cursor.fetchall()
        conn.close()

        category_listbox.delete(0, tk.END)

        for cat in categories:
            category_listbox.insert(tk.END, f"{cat[0]} | {cat[1]}")


    def search_medicine(event):

        text = entry_name.get().strip().lower()

        if len(text) < 2:
            suggestion_box.delete(0, tk.END)
            return

        conn = sqlite3.connect("medical_shop.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT name FROM medicines
        WHERE LOWER(name) LIKE ?
        """, (f"%{text}%",))

        results = cursor.fetchall()
        conn.close()

        suggestion_box.delete(0, tk.END)

        for r in results:
            suggestion_box.insert(tk.END, r[0])


    def select_medicine(event):
        try:
            selected = suggestion_box.get(suggestion_box.curselection())
            entry_name.delete(0, tk.END)
            entry_name.insert(0, selected)
            suggestion_box.delete(0, tk.END)
        except:
            pass


    def add_medicine():
        try:
            name = entry_name.get().strip()
            stock = entry_stock.get().strip()
            cost = entry_cost.get().strip()
            selling = entry_selling.get().strip()

            # ✅ Validation
            if not name or not stock or not cost or not selling:
                messagebox.showerror("Error", "All fields are required")
                return

            stock = int(stock)
            cost = float(cost)
            selling = float(selling)

            selected = category_listbox.get(category_listbox.curselection())
            category_id = int(selected.split("|")[0].strip())

            conn = sqlite3.connect("medical_shop.db")
            cursor = conn.cursor()

            # 🔍 Case-insensitive check (IMPORTANT FIX)
            cursor.execute("""
            SELECT id, stock_quantity FROM medicines 
            WHERE LOWER(name) = LOWER(?)
            """, (name,))
            result = cursor.fetchone()

            if result:
                new_stock = result[1] + stock

                cursor.execute("""
                UPDATE medicines
                SET stock_quantity = ?
                WHERE id = ?
                """, (new_stock, result[0]))

                messagebox.showinfo("Updated", "Stock updated for existing medicine")

            else:
                cursor.execute("""
                INSERT INTO medicines 
                (name, category_id, stock_quantity, cost_price, selling_price)
                VALUES (?, ?, ?, ?, ?)
                """, (name, category_id, stock, cost, selling))

                messagebox.showinfo("Success", "Medicine added successfully")

            conn.commit()
            conn.close()

            # 🧹 Clear fields
            entry_name.delete(0, tk.END)
            entry_stock.delete(0, tk.END)
            entry_cost.delete(0, tk.END)
            entry_selling.delete(0, tk.END)
            suggestion_box.delete(0, tk.END)

        except:
            messagebox.showerror("Error", "Enter valid data & select category")

    # ---------------- UI ----------------

    tk.Label(win, text="Add Medicine", font=("Arial", 14)).pack(pady=10)

    tk.Label(win, text="Medicine Name").pack()
    entry_name = tk.Entry(win)
    entry_name.pack()

    # 🔥 Suggestion box (NEW)
    suggestion_box = tk.Listbox(win, height=4)
    suggestion_box.pack(pady=5)

    entry_name.bind("<KeyRelease>", search_medicine)
    suggestion_box.bind("<<ListboxSelect>>", select_medicine)

    tk.Label(win, text="Stock Quantity").pack()
    entry_stock = tk.Entry(win)
    entry_stock.pack()

    tk.Label(win, text="Cost Price").pack()
    entry_cost = tk.Entry(win)
    entry_cost.pack()

    tk.Label(win, text="Selling Price").pack()
    entry_selling = tk.Entry(win)
    entry_selling.pack()

    tk.Label(win, text="Select Category").pack()

    category_listbox = tk.Listbox(win, height=5)
    category_listbox.pack(pady=5)

    tk.Button(win, text="Load Categories", command=load_categories).pack(pady=5)

    tk.Button(win, text="Add Medicine",
              command=add_medicine,
              bg="green", fg="white").pack(pady=10)
    

from tkinter import ttk


def open_inventory_window():

    import sqlite3

    win = tk.Toplevel()
    win.title("Inventory")
    win.geometry("700x400")

    # ---------------- TABLE ----------------
    columns = ("ID", "Name", "Category", "Stock", "Price")

    tree = ttk.Treeview(win, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # ---------------- LOAD DATA ----------------
    def load_inventory():

        conn = sqlite3.connect("medical_shop.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT m.id, m.name, c.category_name, m.stock_quantity, m.selling_price
        FROM medicines m
        JOIN categories c ON m.category_id = c.category_id
        """)

        rows = cursor.fetchall()
        conn.close()

        # Clear existing
        for item in tree.get_children():
            tree.delete(item)

        # Insert new data
        for row in rows:
            tree.insert("", tk.END, values=row)

    # Load button
    tk.Button(win, text="Load Inventory", command=load_inventory).pack(pady=10)