import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk

#imports
from ui.billing_ui import open_billing_window
from ui.inventory_ui import open_add_medicine_window, open_inventory_window
from ui.reports_ui import open_reports_window

# backend
from inventory.inventory_manager import add_medicine, view_inventory
from analysis.sales_analysis import sales_summary

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Medical Shop Management System")
root.geometry("500x400")

# ---------------- TITLE ----------------
tk.Label(root, text="Medical Shop System", font=("Arial", 16)).pack(pady=20)

# ---------------- BUTTONS ----------------
tk.Button(root, text="Add Medicine", width=25, command=open_add_medicine_window).pack(pady=5)
tk.Button(root, text="View Inventory", width=25, command=open_inventory_window).pack(pady=5)

# 🔥 Billing Button
tk.Button(root, text="Generate Bill", width=25, command=open_billing_window).pack(pady=5)

tk.Button(root, text="Reports", width=25, command=open_reports_window).pack(pady=5)

# Exit
tk.Button(root, text="Exit", width=25, command=root.quit, bg="red", fg="white").pack(pady=20)

# ---------------- RUN ----------------
root.mainloop()