


import csv
import os
from datetime import datetime

INV_FILE = "inventory.csv"
SALES_FILE = "sales.csv"

def init_files():
    if not os.path.exists(INV_FILE):
        with open(INV_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["name","quantity","buy_price","sell_price"])
    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["date","name","quantity","profit"])

def add_stock():
    print("\n--- ADD NEW STOCK ---")
    name = input("Item name: ").lower().strip()
    qty = int(input("Quantity: "))
    buy = float(input("Buying price (KES): "))
    sell = float(input("Selling price (KES): "))
    with open(INV_FILE, 'a', newline='') as f:
        csv.writer(f).writerow([name,qty,buy,sell])
    print(f">> {name.upper()} added successfully!")

def sell_item():
    print("\n--- SELL ITEM ---")
    name = input("Item name: ").lower().strip()
    sell_qty = int(input("Quantity to sell: "))
    rows = []
    sold = False
    profit = 0
    with open(INV_FILE, 'r') as f:
        reader = list(csv.DictReader(f))
        for r in reader:
            if r["name"] == name and int(r["quantity"]) >= sell_qty:
                r["quantity"] = str(int(r["quantity"]) - sell_qty)
                profit = (float(r["sell_price"]) - float(r["buy_price"])) * sell_qty
                sold = True
            rows.append(r)
    if sold:
        with open(INV_FILE, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=["name","quantity","buy_price","sell_price"])
            w.writeheader()
            w.writerows(rows)
        with open(SALES_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d"), name, sell_qty, profit])
        print(f">> Sold {sell_qty}x {name} | Profit: KES {profit}")
    else:
        print(">> Item not found or low stock!")

def view_stock():
    print("\nCURRENT STOCK")
    print("-"*45)
    print(f"{'ITEM':<10} {'QTY':<5} {'BUY':<8} {'SELL':<8}")
    print("-"*45)
    with open(INV_FILE, 'r') as f:
        for r in csv.DictReader(f):
            print(f"{r['name']:<10} {r['quantity']:<5} {r['buy_price']:<8} {r['sell_price']:<8}")
    print("-"*45)

def daily_report():
    print(f"\nDAILY REPORT {datetime.now().strftime('%Y-%m-%d')}")
    print("="*35)
    total_profit = 0
    total_sales = 0
    with open(SALES_FILE, 'r') as f:
        for r in csv.DictReader(f):
            if r["date"] == datetime.now().strftime("%Y-%m-%d"):
                print(f" - {r['name']} x{r['quantity']} -> Profit KES {r['profit']}")
                total_profit += float(r["profit"])
                total_sales += int(r["quantity"])
    print("="*35)
    print(f"TOTAL ITEMS SOLD: {total_sales}")
    print(f"TOTAL PROFIT TODAY: KES {total_profit}")
    print("="*35)

init_files()
while True:
    print("\n" + "="*35)
    print("  DUKA LEDGER SYSTEM - KENYA")
    print("="*35)
    print("1. Add Stock")
    print("2. Sell Item")
    print("3. View Stock")
    print("4. Daily Profit Report")
    print("5. Exit")
    choice = input("\nChoose (1-5): ").strip()
    if choice == "1": add_stock()
    elif choice == "2": sell_item()
    elif choice == "3": view_stock()
    elif choice == "4": daily_report()
    elif choice == "5": 
        print("Goodbye! Keep counting your profit!")
        break