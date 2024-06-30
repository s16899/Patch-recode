import discord
from discord.ext import commands
import sqlite3
import os

bot = commands.Bot(command_prefix="p-", intents=discord.Intents.all())

conn = sqlite3.connect("database.db")

cur = conn.cursor()

@bot.event
async def on_ready():
    print("Hello world!")

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded Cog \"cogs.{filename[:-3]}\"")

cur.execute("CREATE TABLE IF NOT EXISTS balance(userid INTEGER, balance INTEGER, bank INTEGER, maxbank INTEGER)")
print("database created/initialized!")

bot.run(token)