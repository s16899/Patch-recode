import discord
from discord import app_commands
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

    # action_choices = ["buy", "sell", "price", "add"]

    @app_commands.command(name="add stock", description="Adds new stocks depending on what you wanted", stock_name = "Stock name", stock_id = "acronym for your stock name", stock_price="Stock price", amount = "Amount of stocks available")
    async def add_stock(self, interaction: discord.Interaction, stock_name: str, stock_id: str, stock_price: int, amount: int):
        self.cur.execute("SELECT balance FROM data WHERE userid = ?", (interaction.user.id,))
        balance = self.cur.fetchone()
        if not balance or balance[0] < 1000:
            await interaction.response.send_message("You don't have enough `-P` to create/add new stocks!", ephemeral=True)
            return
        
        self.cur.execute("SELECT * FROM stocks WHERE stock_id = ?", (stock_id,))
        existed = self.cur.fetchone()
        if existed:
            await interaction.response.send_message(f"A stock with Acronym ID of ``{stock_id}`` already exists. Please choose a different Acronym for your stock.")
            return

        if amount is None:
            amount = 1000
            return

        self.cur.execute("INSERT INTO stocks (stock_name, stock_id stock_price, amount) VALUES (?, ?, ?, ?)", (stock_name, stock_id, stock_price, amount))
        
        self.conn.commit()
        await interaction.response.send_message(f"Stock {stock_name} (Acronym ID: {stock_id}) added successfully with a starting price of {stock_price} and stock value of {amount}!", ephemeral=True)
    
    @app_commands.command(name="Buy stock", description="Buys stocks depending on what you wanted", stock_id = "Stock acronym (ID)", amount = "Amount of stocks you are willing to buy")
    async def buy_stock(self, interaction: discord.Interaction, stock_id: int, amount: int):
        await self.database_check(interaction.author.id)

        user_id = interaction.author.id

        self.cur.execute("SELECT balance FROM data WHERE userid = ?", (user_id,))
        balance = self.cur.fetchone()
        if not balance or balance[0] <= 1:
            await interaction.response.send_message("You don't have enough `-P`")
            return

        self.cur.execute("SELECT stock_price, amount FROM stocks WHERE stock_id = ?", (stock_id,))
        
        stock = self.cur.fetchone()

        if not stock:
            await interaction.response.send_message("Stock not found.")
            return

        stock_price, stock_amount = stock
        total_price = stock_price * amount

        if balance[0] < total_price:
            await interaction.response.send_message(f"Dude, you don't even have enough `-P` to buy the stock. You need ``-P {total_price - balance[0]}`` more.")
            return
        
        new_balance = balance[0] - total_price
        self.cur.execute("UPDATE data SET balance = ? WHERE userid = ?", (new_balance, user_id))

        new_stock_amount = stock_amount + amount

        

async def setup(bot):
    await bot.add_cog(StockMarket(bot))
