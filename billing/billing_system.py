import sqlite3

def generate_bill():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("medical_shop.db")
    cursor = conn.cursor()

    total_amount = 0
    bill_items = []

    while True:

        search = input("\n🔍 Search medicine (or type 'q' to finish): ")

        if search.lower() == 'q':
            break

        # 🔎 Search medicines
        cursor.execute("""
            SELECT id, name, stock_quantity, selling_price 
            FROM medicines 
            WHERE name LIKE ?
        """, ('%' + search + '%',))

        results = cursor.fetchall()

        if not results:
            print("❌ No medicine found")
            continue

        # 📋 Show results
        print("\nAvailable Medicines:")
        print("ID   Name              Stock   Price")
        print("----------------------------------------")

        for row in results:
            print(f"{row[0]:<5}{row[1]:<18}{row[2]:<8}{row[3]}")

        # 🧾 Select medicine
        try:
            med_id = int(input("\nEnter Medicine ID: "))
        except ValueError:
            print("❌ Invalid input")
            continue

        # 📦 Fetch selected medicine
        cursor.execute("""
            SELECT name, stock_quantity, selling_price 
            FROM medicines 
            WHERE id = ?
        """, (med_id,))

        medicine = cursor.fetchone()

        if not medicine:
            print("❌ Invalid ID selected")
            continue

        name, stock, price = medicine

        # 🔢 Enter quantity
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("❌ Invalid quantity")
            continue

        if quantity > stock:
            print("❌ Not enough stock")
            continue

        # 💰 Calculate amount
        amount = quantity * price
        total_amount += amount

        # 🧾 Store for bill summary
        bill_items.append((name, quantity, price, amount))

        print(f"✅ Added: {name} x {quantity} = {amount}")

        # 📉 Update stock
        new_stock = stock - quantity
        cursor.execute("""
            UPDATE medicines 
            SET stock_quantity = ? 
            WHERE id = ?
        """, (new_stock, med_id))

        # 🧾 Insert into sales
        sale_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO sales (medicine_id, quantity, total_price, sale_date)
            VALUES (?, ?, ?, ?)
        """, (med_id, quantity, amount, sale_date))

    # 🧾 Final Bill Summary
    print("\n🧾 BILL SUMMARY")
    print("------------------------------------------------")
    print("Name           Qty     Price     Total")
    print("------------------------------------------------")

    for item in bill_items:
        print(f"{item[0]:<15}{item[1]:<8}{item[2]:<10}{item[3]}")

    print("------------------------------------------------")
    print(f"TOTAL AMOUNT: ₹{total_amount}")

    conn.commit()
    conn.close()
    
def view_sales():

    conn = sqlite3.connect("medical_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT s.sale_id, m.name, s.quantity, s.total_price, s.sale_date
    FROM sales s
    JOIN medicines m ON s.medicine_id = m.id
    """)

    rows = cursor.fetchall()

    print("\nSales Data:")
    print("ID   Medicine        Qty    Amount    Date")
    print("------------------------------------------------")

    for row in rows:
        print(f"{row[0]:<5}{row[1]:<15}{row[2]:<7}{row[3]:<10}{row[4]}")

    conn.close()