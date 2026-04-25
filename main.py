from inventory.inventory_manager import add_category, view_category, add_medicine, view_inventory, low_stock_alert, expiry_alert, search_medicine
from billing.billing_system import generate_bill, view_sales
from analysis.sales_analysis import sales_summary, category_sales, profit_analysis, monthly_sales_trend


while True:
    
    print("\nMEDICAL SHOP SYSTEM")
    
    print("1 Add Category")
    print("2 View Categories")
    print("3 Add Medicine")
    print("4 view inventory")
    print("5 Generate Bill")
    print("6 View Sales")
    print("7 Sales Summary")
    print("8 low_stock_alert")
    print("9 Expiry Alert")
    print("10 Category Wise Sales")
    print("11 Profit Analysis")
    print("12 Monthly Sales Trend")
    print("13 Search medicine")
    print("14 Exit")
    
    choice = input("Enter choice: ")
    
    if choice == "1":
        add_category()

    elif choice == "2":
        view_category()

    elif choice == "3":
        add_medicine()

    elif choice == "4":
        view_inventory()
        
    elif choice == "5":
        generate_bill()

    elif choice == "6":
        view_sales()
    
    elif choice == "7":
        sales_summary()
        
    elif choice == "8":
        low_stock_alert()
        
    elif choice == "9":
        expiry_alert()
        
    elif choice == "10":
        category_sales()
        
    elif choice == "11":
        profit_analysis()
        
    elif choice == "12":
        monthly_sales_trend()
        
    elif choice == "13":
        search_medicine()
        
    elif choice == "14":
        break
    
    else:
        print("Invalid choice")