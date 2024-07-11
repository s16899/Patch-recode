import discord
from discord.ext import commands, tasks
import random
import sqlite3

class StockMarket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("database.db")
        self.cur = self.conn.cursor()
        self.create_table()
        self.update_stock_prices.start()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS data (
                userid INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                bank INTEGER DEFAULT 0,
                maxbank INTEGER DEFAULT 500
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_name TEXT,
                stock_price INTEGER,
                amount INTEGER
            )
        """)
        self.conn.commit()

    async def database_check(self, user_id=None):
        if user_id is None:
            return

        self.cur.execute("SELECT * FROM data WHERE userid = ?", (user_id,))
        user_row = self.cur.fetchone()
        if not user_row:
            self.cur.execute("INSERT INTO data (userid, balance, bank, maxbank) VALUES (?, ?, ?, ?)", (user_id, 0, 0, 500))
            self.conn.commit()
    
    @tasks.loop(minutes=5)
    async def update_stock_prices(self):
        self.cur.execute("SELECT * FROM stocks")
        stocks = self.cur.fetchall()
        for stock in stocks:
            stock_id, stock_name, stock_price, amount = stock
            new_price = stock_price + random.randint(-5, 5)
            if new_price < 1:
                new_price = 1
            self.cur.execute("UPDATE stocks SET stock_price = ? WHERE stock_id = ?", (new_price, stock_id))
        self.conn.commit()
        print("Stock prices updated")

    action_choices = ["buy", "sell", "price", "add"]

    @commands.hybrid_command(name="stock", description="A stock market, you can run multiple commands in this one command to manage your stock.")
    async def stock(self, ctx, action: str, stock_id: str = None, stock_name: str = None, stock_price: int = None, amount: int = 1):
        try:
            if stock_id is not None:
                stock_id = int(stock_id)
        except ValueError:
            await ctx.send("Invalid stock ID. It must be an integer.")
            return

        await self.database_check(ctx.author.id)

        if action == self.action_choices[0]:  # "buy"
            stock_name = None
            stock_price = None
            user_id = ctx.author.id
            self.cur.execute("SELECT balance FROM data WHERE userid = ?", (user_id,))
            balance = self.cur.fetchone()
            if not balance or balance[0] <= 1:
                await ctx.send("You don't have enough balance.")
                return
            
            self.cur.execute("SELECT stock_price, amount FROM stocks WHERE stock_id = ?", (stock_id,))
            stock = self.cur.fetchone()

            if not stock:
                await ctx.send("Stock not found.")
                return
        
            stock_price, stock_amount = stock
            total_price = stock_price * amount
            if balance[0] < total_price:
                await ctx.send(f"You don't have enough -P to buy the stock. You need {total_price - balance[0]} more -P.")
                return

            new_balance = balance[0] - total_price
            self.cur.execute("UPDATE data SET balance = ? WHERE userid = ?", (new_balance, user_id))
            new_stock_amount = stock_amount + amount
            self.cur.execute("UPDATE stocks SET amount = ? WHERE stock_id = ?", (new_stock_amount, stock_id))
            self.conn.commit()
            await ctx.send(f"You have bought {amount} shares of stock {stock_id} for -P {total_price}")
            
        elif action == self.action_choices[1]:  # "sell"
            user_id = ctx.author.id
            self.cur.execute("SELECT balance FROM data WHERE userid = ?", (user_id,))
            balance = self.cur.fetchone()
            if not balance:
                await ctx.send("You don't have a balance record.")
                return
            
            self.cur.execute("SELECT stock_price, amount FROM stocks WHERE stock_id = ?", (stock_id,))
            stock = self.cur.fetchone()
            if not stock:
                await ctx.send("Stock not found.")
                return
        
            stock_price, stock_amount = stock
            if stock_amount < amount:
                await ctx.send("Not enough stock available to sell.")
                return

            total_price = stock_price * amount
            new_balance = balance[0] + total_price
            self.cur.execute("UPDATE data SET balance = ? WHERE userid = ?", (new_balance, user_id))
            new_stock_amount = stock_amount - amount
            self.cur.execute("UPDATE stocks SET amount = ? WHERE stock_id = ?", (new_stock_amount, stock_id))
            self.conn.commit()
            await ctx.send(f"You have sold {amount} shares of stock {stock_id} for -P {total_price}")
            
        elif action == self.action_choices[2]:  # "price"
            stock_name = None
            stock_price = None
            if stock_id is None:
                self.cur.execute("SELECT * FROM stocks")
                stocks = self.cur.fetchall()
                e = discord.Embed(title="Stock Market", color=discord.Color.green())
                for stock in stocks:
                    stock_id, stock_name, stock_price, amount = stock
                    e.add_field(name=f"Stock Name: {stock_name} (ID: {stock_id})", value=f"Price: {stock_price} -P, Amount: {amount}")
                await ctx.send(embed=e)
            else:
                self.cur.execute("SELECT * FROM stocks WHERE stock_id = ?", (stock_id,))
                stock = self.cur.fetchone()
                if stock:
                    stock_id, stock_name, stock_price, amount = stock
                    await ctx.send(f"Stock Name: {stock_name}\nStock ID: {stock_id}\nStock Price: {stock_price}\nAmount: {amount}")
                else:
                    await ctx.send("Stock not found.")

        elif action == self.action_choices[3]:  # "add"
            self.cur.execute("SELECT balance FROM data WHERE userid = ?", (ctx.author.id,))
            balance = self.cur.fetchone()
            if not balance or balance[0] < 1000:
                await ctx.send("You don't have enough -P to create/add new stock!")
                return
            
            self.cur.execute("INSERT INTO stocks (stock_name, stock_price, amount) VALUES (?, ?, ?)", (stock_name, stock_price, 0))
            self.conn.commit()
            await ctx.send(f"Stock {stock_name} added with initial price of -P {stock_price}")

async def setup(bot):
    await bot.add_cog(StockMarket(bot))
