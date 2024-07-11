import discord
from discord.ext import commands
import sqlite3
import os

bot = commands.Bot(command_prefix="p-", intents=discord.Intents.all(), help_command=None)

conn = sqlite3.connect("database.db")

cur = conn.cursor()

@bot.event
async def on_ready():
    print("Hello world!")

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded Cog \"cogs.{filename[:-3]}\"")

@bot.command()
async def help(ctx):
    em = discord.Embed(title="Help Menu V1.1", color=0x00ff00)
    em.add_field(name="**Management**", value="", inline=False)
    # em.add_field(name="p-register", value="Registers you into the database.", inline=True)
    em.add_field(name="p-balance", value="Shows your balance.", inline=True)
    em.add_field(name="**Money related**", value="", inline=False)
    em.add_field(name="p-fish", value="Fishes for -P.", inline=True)
    em.add_field(name="**Stocks (Beta)**", value="", inline=False)
    em.add_field(name="p-stock [FUNCTIONS]", value="Shows your stock.", inline=True)
    em.add_field(name="List of FUNCTIONS", value="", inline=True)
    em.add_field(name="buy", value="Buys a stock.", inline=True)
    em.add_field(name="sell", value="Sells a stock.", inline=True)
    em.add_field(name="price", value="Shows the price of a stock.", inline=True)
    em.add_field(name="add", value="Adds a stock.", inline=True)
    await ctx.send(embed=em)


cur.execute("CREATE TABLE IF NOT EXISTS data(userid INTEGER, balance INTEGER, bank INTEGER, maxbank INTEGER)")
print("database created/initialized!")

cur.execute("CREATE TABLE IF NOT EXISTS stocks(stock_name TEXT, stock_id INTEGER, stock_price INTEGER, amount INTEGER)")
print("stock database created/initialized!")

bot.run("token") # non-slash command version