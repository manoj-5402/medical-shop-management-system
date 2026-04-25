import sqlite3

def add_category():
    conn = sqlite3.connect("medical_shop.db")
    cursor = conn.cursor()
    
    category_name = input("Enter category name: ")
    
    cursor.execute(
        "INSERT INTO categories (category_name) values (?)",
        (category_name,)
    )
    
    
    
    conn.commit()
    conn.close()
    
    print("Category added sucessfully!!!")
    
def view_category():
    conn = sqlite3.connect("medical_shop.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM categories")
    
    rows = cursor.fetchall()
    
    print("\ncategories:")
    if len(rows) == 0:
        print("No categories found")
    else:
        for row in rows:
            print(row)
        
    conn.close()
    
def add_medicine():

    import sqlite3

    conn = sqlite3.connect("medical_shop.db")
    cursor = conn.cursor()

    choice = input("\n1. Add New Medicine\n2. Update Existing Stock\nEnter choice: ")

    # 🆕 ADD NEW MEDICINE
    if choice == "1":

        name = input("Enter medicine name: ")
        category_id = int(input("Enter category ID: "))
        quantity = int(input("Enter quantity: "))
        cost_price = float(input("Enter cost price: "))
        selling_price = float(input("Enter selling price: "))
        expiry_date = input("Enter expiry date (YYYY-MM-DD): ")

        cursor.execute("""
            INSERT INTO medicines 
            (name, category_id, stock_quantity, cost_price, selling_price, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, category_id, quantity, cost_price, selling_price, expiry_date))

        print("✅ New medicine added!")

    # 🔄 UPDATE EXISTING STOCK (SMART SEARCH)
    elif choice == "2":

        search = input("🔍 Search medicine: ")

        cursor.execute("""
            SELECT id, name, stock_quantity 
            FROM medicines 
            WHERE name LIKE ?
        """, ('%' + search + '%',))

        results = cursor.fetchall()

        if not results:
            print("❌ No medicine found")
            return

        print("\nAvailable Medicines:")
        print("ID   Name              Stock")
        print("--------------------------------")

        for row in results:
            print(f"{row[0]:<5}{row[1]:<18}{row[2]}")

        try:
            med_id = int(input("\nEnter Medicine ID: "))
        except ValueError:
            print("❌ Invalid input")
            return

        cursor.execute("""
            SELECT stock_quantity FROM medicines WHERE id = ?
        """, (med_id,))

        result = cursor.fetchone()

        if not result:
            print("❌ Invalid ID")
            return

        current_stock = result[0]

        try:
            add_qty = int(input("Enter quantity to add: "))
        except ValueError:
            print("❌ Invalid quantity")
            return

        new_stock = current_stock + add_qty

        cursor.execute("""
            UPDATE medicines 
            SET stock_quantity = ?
            WHERE id = ?
        """, (new_stock, med_id))

        print(f"✅ Stock updated! New stock: {new_stock}")

    else:
        print("❌ Invalid choice")

    conn.commit()
    conn.close()
    
    
def view_inventory():
    conn = sqlite3.connect("medical_shop.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT m.id, m.name, c.category_name, m.stock_quantity, m.expiry_Date 
    FROM medicines m
    JOIN categories c
    ON m.category_id = c.category_id
                   """)
    
    rows = cursor.fetchall()
    
    print("\nInventory:")
    print("ID   Name           Category    Stock    Expiry")
    print("------------------------------------------------")
    
    for row in rows:
        print(f"{row[0]:<5}{row[1]:<18}{row[2]:<13}{row[3]:<10}{row[4]}")
        
    conn.close()
    
def low_stock_alert():
    conn = sqlite3.connect("medical_shop.db")
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT name, stock_quantity
                   FROM medicines
                   WHERE stock_quantity < 50
                   """)
    
    rows = cursor.fetchall()
    
    print("\n⚠️ Low Stock Medicines:")
    print("--------------------------------")
    
    if not rows:
        print("All stocks are sufficient ✅")
        
    else:
        for row in rows:
            print(f"{row[0]} -> {row[1]} left")
            
    conn.close()
    
def expiry_alert():
    
    from datetime import datetime, timedelta
    
    conn = sqlite3.connect("medical_shop.db")
    cursor = conn.cursor()
    
    today = datetime.now().date()
    next_30_days = today + timedelta(days=30)
    
    cursor.execute("""
                   SELECT name, expiry_date
                   FROM medicines
                   """)
    
    rows = cursor.fetchall()
    
    print("\n⏰ Expiring Soon Medicines:")
    print("--------------------------------")
    
    found = False
    
    for row in rows:
        expiry = datetime.strptime(row[1], "%Y-%m-%d").date()
        
        if today <= expiry <= next_30_days:
            print(f"{row[0]} -> {row[1]}")
            found = True
            
    if not found:
        print("No medicines expiring soon ✅")
        
    conn.close
    
def search_medicine():
    import sqlite3
    
    conn = sqlite3.connect("medical_shop.db")
    cursor = conn.cursor()

    keyword = input("Enter medicine name to search: ")

    cursor.execute("""
        SELECT id, name, stock_quantity, selling_price 
        FROM medicines 
        WHERE name LIKE ?
    """, ('%' + keyword + '%',))

    results = cursor.fetchall()

    if results:
        print("\n🔍 Search Results:")
        print("ID   Name              Stock   Price")
        print("----------------------------------------")
        
        for row in results:
            print(f"{row[0]:<5}{row[1]:<18}{row[2]:<8}{row[3]}")
    else:
        print("❌ No matching medicines found")

    conn.close()