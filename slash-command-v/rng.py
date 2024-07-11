# import discord
# import random
# from discord import app_commands
# from discord.ext import commands
# import json



# class RNG(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @app_commands.command(name="roll", description="Rolls a random number and gives you rank! (+5 -P per roll)")
#     async def rng(self, interaction: discord.Interaction) -> None:
        
#         async def weighted_choice(statuses):
#             items = [item['rank'] for item in statuses]
#             weights = [item['rarity'] for item in statuses]
            
#             # Convert weights to probabilities
#             total_weight = sum(weights)
#             probabilities = [weight / total_weight for weight in weights]
            
#             selected_status = random.choices(statuses, probabilities, k=1)[0]
#             return selected_status

#         # Load statuses from JSON file
#         statuses = load_statuses('statuses.json')

#         res = weighted_choice(statuses)

#         em = discord.Embed(title="Roll", color=0x00ff00)
#         em.add_field(name="Result", value=res['rank'], inline=False)
#         em.add_field(name="Rarity", value=f"{res['rarity']}%", inline=False)

#         await interaction.response.send_message(embed=em)

# async def setup(bot):
#     await bot.add_cog(RNG(bot))