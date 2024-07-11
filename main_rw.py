import discord
from db import Database
from discord.ext import commands

bot = commands.Bot(command_prefix="p-" intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Hello world!")
    await bot.db.create_tables()
    bot.loop.create_task(update_market())

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    await bot.process_commands(message)
    if await bot.db.user_exists(message.author.id):
        await bot.db.increase_balance(message.author.id, 5)
        await 