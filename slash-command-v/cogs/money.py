import discord
from discord.ext import commands
import sqlite3
import random

class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS data (
                userid INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                bank INTEGER DEFAULT 0,
                maxbank INTEGER DEFAULT 500
            )
        """)
        self.conn.commit()

    async def database_check(self, user_id=None):
        if user_id is None:
            return

        self.cur.execute("SELECT * FROM data WHERE userid = ?", (user_id,))
        user_row = self.cur.fetchone()
        if not user_row:
            # If user not found in database, insert a new row
            print(f"Inserting new user {user_id} into database.")
            self.cur.execute("INSERT INTO data (userid, balance, bank, maxbank) VALUES (?, ?, ?, ?)", (user_id, 0, 0, 500))
            self.conn.commit()
        else:
            # print(f"User {user_id} already exists in database with balance {user_row[1]}.")
            pass

    @commands.command()
    async def fish(self, ctx):
        await self.database_check(ctx.author.id)

        self.cur.execute("SELECT balance FROM data WHERE userid = ?", (ctx.author.id,))
        balance = self.cur.fetchone()

        if balance is None:
            await ctx.send("You have no balance record.")
            return

        earned = random.randint(0, 256)
        new_balance = balance[0] + earned
        # print(f"User {ctx.author.id} fished and earned {earned} -P. New balance is {new_balance} -P.")

        self.cur.execute("UPDATE data SET balance = ? WHERE userid = ?", (new_balance, ctx.author.id))
        self.conn.commit()

        await ctx.send(f"You fished and earned -P {earned}. Your new balance is -P {new_balance}")

async def setup(bot):
    await bot.add_cog(Money(bot))
