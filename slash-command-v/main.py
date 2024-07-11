import discord
from discord.ext import commands
import sqlite3
import os
import json
import random
from discord import app_commands

bot = commands.Bot(command_prefix="p-", intents=discord.Intents.all(), help_command=None)

conn = sqlite3.connect("database.db")

cur = conn.cursor()

@bot.event
async def on_ready():
    print("Hello world!")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded Cog \"cogs.{filename[:-3]}\"")

@bot.tree.command(name='help')
async def help(interaction: discord.Interaction):
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
    await interaction.response.send_message(embed=em)

async def load_statuses(filename):
    with open(filename, 'r') as file:
        statuses = json.load(file)
    return statuses

@bot.tree.command(name="roll", description="Rolls a random number and gives you rank! (+5 -P per roll)")
async def roll(interaction: discord.Interaction):
        
        async def weighted_choice(statuses):
            items = [item['rank'] for item in statuses]
            weights = [item['rarity'] for item in statuses]
            
            # Convert weights to probabilities
            total_weight = sum(weights)
            probabilities = [weight / total_weight for weight in weights]
            
            selected_status = random.choices(statuses, probabilities, k=1)[0]
            return selected_status

        # Load statuses from JSON file
        statuses = load_statuses('statuses.json')

        res = weighted_choice(statuses)

        em = discord.Embed(title="Roll", color=0x00ff00)
        em.add_field(name="Result", value=res['rank'], inline=False)
        em.add_field(name="Rarity", value=f"{res['rarity']}%", inline=False)

        await interaction.response.send_message(embed=em)

@bot.command(name="sync") 
async def sync(ctx):
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s).")

cur.execute("CREATE TABLE IF NOT EXISTS data(userid INTEGER, balance INTEGER, bank INTEGER, maxbank INTEGER)")
print("database created/initialized!")

cur.execute("CREATE TABLE IF NOT EXISTS stocks(stock_name TEXT, stock_id TEXT, stock_price INTEGER, amount INTEGER)")
print("stock database created/initialized!")

bot.run("token") # slash command version