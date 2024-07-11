import sqlite3
import os

def cls():
    os.system('cls')

conn = sqlite3.connect("database.db")

cur = conn.cursor()

sep = "-"*30

print(f"{sep} Options {sep}")
print("1.       delete stock")
print("2.       add stock")
print("3.       modify user database")
print("4.       delete user database")

opt = int(input("Enter option: "))

cls()

if opt == 1:
    cur.execute("SELECT * FROM stocks")
    stocks = cur.fetchall()

    print("Choose the stock to delete (by ID or name): ")
    for stock in stocks:
        print(f"Stock name: {stock[1]} | ID: {stock[0]} | Price: {stock[2]} | Amount: {stock[3]}")
    
    stock_input = input("Enter stock ID or name: ")

    try:
        # Try to interpret the input as an integer (stock ID)
        stock_id = str(stock_input)
        cur.execute("DELETE FROM stocks WHERE stock_id = ?", (stock_id,))
    except ValueError:
        # If it fails, treat the input as a stock name
        stock_name = stock_input
        cur.execute("DELETE FROM stocks WHERE stock_name = ?", (stock_name,))
    
    conn.commit()  # Commit the changes to the database

elif opt == 2:
    name = input("Enter stock name: ")
    id = int(input("Enter stock id: "))
    price = int(input("Enter stock price: "))
    amount = int(input("Enter stock amount: "))

    cur.execute("INSERT INTO stocks(stock_name, stock_id, stock_price, amount) VALUES(?, ?, ?, ?)", (name, id, price, amount))
    conn.commit()  # Commit the changes to the database

elif opt == 3:
    usr = str(input("Enter user ID: "))

    cur.execute("SELECT * FROM data WHERE userid = ?", (usr,))
    user_data = cur.fetchone()

    if user_data:
        print("User chosen: ", user_data)

        print("------------------------------------------")
        print("Select options: ")
        print("1. Modify balance")
        print("2. Modify bank balance")
        print("3. Modify max bank balance")

        opti = int(input("Enter option: "))

        if opti == 1:
            bal = int(input("Enter new balance: "))
            cur.execute("UPDATE data SET balance = ? WHERE userid = ?", (bal, usr))
        elif opti == 2:
            bal = int(input("Enter new bank balance: "))
            cur.execute("UPDATE data SET bank = ? WHERE userid = ?", (bal, usr))
        elif opti == 3:
            bal = int(input("Enter new max bank balance: "))
            cur.execute("UPDATE data SET maxbank = ? WHERE userid = ?", (bal, usr))
        else:
            print("Invalid option.")
        conn.commit()  # Commit the changes to the database
    else:
        print("User not found.")

elif opt == 4:
    usr = str(input("Enter user ID: "))

    cur.execute("DELETE FROM data WHERE userid = ?", (usr,))
    conn.commit()  # Commit the changes to the database

else:
    print("Invalid option.")

conn.close()  # Close the database connection when done
