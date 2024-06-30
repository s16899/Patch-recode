import discord
from discord.ext import commands

class management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def balance(self, ctx):
        # if member == None:
        #     member = ctx.author
        
        await ctx.send("Yo!")

async def setup(bot):
    await bot.add_cog(management(bot))