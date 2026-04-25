import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date
import os


# ---------------- PDF GENERATION ----------------
def generate_pdf_bill(customer_name, bill_items, total_amount):

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from datetime import datetime

    # 📅 Current date & time
    now = datetime.now()
    formatted_date = now.strftime("%d-%m-%Y %I:%M %p")

    # 📁 Unique file name
    file_name = f"bill_{customer_name}_{now.strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    elements = []

    # 🏪 Title
    elements.append(Paragraph("Medical Shop Invoice", styles['Title']))
    elements.append(Spacer(1, 10))

    # 👤 Customer + Date
    elements.append(Paragraph(f"Customer: {customer_name}", styles['Normal']))
    elements.append(Paragraph(f"Date: {formatted_date}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # 💊 Items Header
    elements.append(Paragraph("Items:", styles['Heading3']))
    elements.append(Spacer(1, 10))

    # 📦 Items list
    for item in bill_items:
        line = f"{item['name']} x {item['quantity']} = ₹{item['total']}"
        elements.append(Paragraph(line, styles['Normal']))

    elements.append(Spacer(1, 10))

    # 💰 Total
    elements.append(Paragraph(f"Total Amount: ₹{total_amount}", styles['Heading2']))

    doc.build(elements)


# ---------------- CLEANUP OLD FILES ----------------
def cleanup_old_bills(folder=".", limit=10):

    files = [f for f in os.listdir(folder) if f.startswith("bill_") and f.endswith(".pdf")]

    files.sort(key=lambda x: os.path.getctime(os.path.join(folder, x)))

    while len(files) > limit:
        file_to_delete = files.pop(0)
        os.remove(os.path.join(folder, file_to_delete))


# ---------------- MAIN BILLING WINDOW ----------------
def open_billing_window():

    bill_items = []

    win = tk.Toplevel()
    win.title("Billing System")
    win.geometry("600x600")

    # ---------------- FUNCTIONS ----------------

    def search_medicine():
        keyword = entry_search.get()

        conn = sqlite3.connect("medical_shop.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, name, stock_quantity, selling_price
        FROM medicines
        WHERE name LIKE ?
        """, ('%' + keyword + '%',))

        results = cursor.fetchall()
        conn.close()

        listbox.delete(0, tk.END)

        for row in results:
            display = f"{row[0]} | {row[1]} | Stock:{row[2]} | ₹{row[3]}"
            listbox.insert(tk.END, display)


    def add_to_bill():
        try:
            selected = listbox.get(listbox.curselection())
            qty = int(entry_qty.get())

            parts = selected.split("|")
            med_id = int(parts[0].strip())
            med_name = parts[1].strip()
            stock = int(parts[2].replace("Stock:", "").strip())
            price = float(parts[3].replace("₹", "").strip())

            if qty > stock:
                messagebox.showerror("Error", "Not enough stock")
                return

            total = qty * price

            bill_items.append({
                "id": med_id,
                "name": med_name,
                "quantity": qty,
                "price": price,
                "total": total
            })

            update_bill_display()

        except:
            messagebox.showerror("Error", "Select medicine & enter valid quantity")


    def remove_item():
        try:
            index = bill_listbox.curselection()[0]
            bill_items.pop(index)
            update_bill_display()
        except:
            messagebox.showerror("Error", "Select item to remove")


    def update_bill_display():
        bill_listbox.delete(0, tk.END)
        total_amount = 0

        for item in bill_items:
            line = f"{item['name']} x {item['quantity']} = ₹{item['total']}"
            bill_listbox.insert(tk.END, line)
            total_amount += item['total']

        label_total.config(text=f"Total: ₹{total_amount}")


    def generate_final_bill():
        if not bill_items:
            messagebox.showwarning("Warning", "No items in bill")
            return

        customer_name = entry_name.get()

        conn = sqlite3.connect("medical_shop.db")
        cursor = conn.cursor()

        for item in bill_items:
            cursor.execute("""
            INSERT INTO sales (medicine_id, quantity, total_price, sale_date)
            VALUES (?, ?, ?, ?)
            """, (item["id"], item["quantity"], item["total"], date.today()))

            cursor.execute("""
            UPDATE medicines
            SET stock_quantity = stock_quantity - ?
            WHERE id = ?
            """, (item["quantity"], item["id"]))

        conn.commit()
        conn.close()

        # 💰 Total calculation
        total_amount = sum(item['total'] for item in bill_items)

        # 📄 Generate PDF
        generate_pdf_bill(customer_name, bill_items, total_amount)

        # 🧹 Cleanup old bills
        cleanup_old_bills(limit=10)

        messagebox.showinfo("Success", f"Bill generated for {customer_name}")

        bill_items.clear()
        update_bill_display()

    # ---------------- UI ----------------

    tk.Label(win, text="Billing System", font=("Arial", 16)).pack(pady=10)

    # Customer
    tk.Label(win, text="Customer Name").pack()
    entry_name = tk.Entry(win)
    entry_name.pack()

    # Search
    entry_search = tk.Entry(win)
    entry_search.pack(pady=5)

    tk.Button(win, text="Search", command=search_medicine).pack()

    listbox = tk.Listbox(win, width=50)
    listbox.pack(pady=5)

    # Quantity
    tk.Label(win, text="Quantity").pack()
    entry_qty = tk.Entry(win)
    entry_qty.pack()

    tk.Button(win, text="Add to Bill", command=add_to_bill).pack(pady=5)

    # Bill
    tk.Label(win, text="Bill Items").pack()

    bill_listbox = tk.Listbox(win, width=50)
    bill_listbox.pack()

    tk.Button(win, text="Remove Item", command=remove_item).pack(pady=5)

    # Total
    label_total = tk.Label(win, text="Total: ₹0")
    label_total.pack()

    # Final Bill
    tk.Button(win, text="Generate Final Bill", command=generate_final_bill,
              bg="green", fg="white").pack(pady=10)