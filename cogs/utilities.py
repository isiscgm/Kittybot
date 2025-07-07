import discord
from discord.ext import commands
from discord import app_commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Mostra a latência do bot.")
    async def ping_slash(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="Pong! 🏓",
            description=f"Latência: {latency}ms",
            color=0xff69b4
        )
        await interaction.response.send_message(embed=embed)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="Pong! 🏓",
            description=f"Latência: {latency}ms",
            color=0xff69b4
        )
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Utilities(bot))
