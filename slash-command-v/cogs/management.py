import discord
from discord.ext import commands
import sqlite3
from discord import app_commands

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("database.db")
        self.cur = self.conn.cursor()

    async def database_check(self, user_id=None):
        if user_id is None:
            return

        self.cur.execute("SELECT * FROM data WHERE userid = ?", (user_id,))
        user_row = self.cur.fetchone()
        if not user_row:
            # If user not found in database, insert a new row
            self.cur.execute("INSERT INTO data (userid, balance, bank, maxbank) VALUES (?, ?, ?, ?)", (user_id, 0, 0, 500))
            self.conn.commit()

    @commands.hybrid_command(name="balance", description="Shows your balance.")
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        user_id = member.id

        await self.database_check(user_id)

        self.cur.execute("SELECT balance, bank, maxbank FROM data WHERE userid = ?", (user_id,))
        balance_data = self.cur.fetchone()

        if balance_data is None:
            await ctx.send(f"{member.mention} has no balance record. Run `p-register` or `/register` to register.")
            return

        embed = discord.Embed(title=f"{member.display_name}'s Balance", color=0x00ff00)
        embed.add_field(name="**-P**", value=balance_data[0], inline=False)
        embed.add_field(name="**-P Bank**", value=f"{balance_data[1]}/{balance_data[2]}", inline=False)

        await ctx.send(embed=embed)

    # Uncomment and modify the register command as needed
    # @commands.hybrid_command(name="register", description="Registers you into the database.", aliases=["reg", "create"])
    # async def register(self, ctx, affiliate_code: str = None):
    #     with open("affiliate_codes.txt", "r") as f:
    #         affiliate_code = f.read()
    #     e = discord.Embed(title="Account registered Successfully!", color=0x00FF00)
    #     e.add_field(name="Register status", value="Success! ✅")
    #     e.add_field(name="Affiliate code", value=affiliate_code)
    #     if affiliate_code is not None:
    #         e.add_field(name="Thank you!", value="Thank you for using our affiliate code! As for your gift, you have -P 1000 to kickstart your journey to be #1!")
    #         self.cur.execute("INSERT INTO data (userid, balance, bank, maxbank) VALUES (?, ?, ?, ?)", (ctx.author.id, 1000, 100, 500))
    #     else:
    #         self.cur.execute("INSERT INTO data (userid, balance, bank, maxbank) VALUES (?, ?, ?, ?)", (ctx.author.id, 0, 100, 500))
    #     self.conn.commit()
    #     await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(Management(bot))
