import random
import discord
import json
import os
from discord.ext import commands
from discord import app_commands


with open(os.path.join("assets", "media.json"), "r", encoding="utf-8") as f:
    media = json.load(f)

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gatinhos")
    async def gatinhos(self, ctx: commands.Context):
        url_gatinhos = random.choice(media["gifs"]["gatinhos"])
        embed = discord.Embed(
            title="Gatinho! 🐱",
            color=0xff69b4
        )
        embed.set_image(url=url_gatinhos)
        if url_gatinhos == "https://i.pinimg.com/736x/9b/d4/7e/9bd47e1ccd4ef174764f68d6101da84e.jpg":
            embed.set_footer(text="Esse gatinho tá de castigo, mas é um castigo bonitinho 🥺")
        elif url_gatinhos == "https://i.pinimg.com/736x/bf/44/78/bf4478888a2da33dbb185b14cb6e779a.jpg":
            embed.set_footer(text="😳😨")
        elif url_gatinhos == "https://images-ext-1.discordapp.net/external/03rJR9SF16vYYOxnlLrHGgRvNtjnf8pMIVf5gsxJwZc/https/i.pinimg.com/736x/09/c9/c8/09c9c8b00dafa7654ad4226a6c2c884e.jpg?format=webp":
            embed.set_footer(text="😱")
        else:
            embed.set_footer(text="Olha que gatinho bonitinho 🥺")
        await ctx.reply(embed=embed)

    @app_commands.command(name="gatinhos", description="Mostra um gif de gatinho aleatório")
    async def gatinhos_slash(self, interaction: discord.Interaction):
        url_gatinhos = random.choice(media["gifs"]["gatinhos"])
        embed = discord.Embed(
            title="Gatinho! 🐱",
            color=0xff69b4
        )
        embed.set_image(url=url_gatinhos)
        if url_gatinhos == "https://i.pinimg.com/736x/9b/d4/7e/9bd47e1ccd4ef174764f68d6101da84e.jpg":
            embed.set_footer(text="Esse gatinho tá de castigo, mas é um castigo bonitinho 🥺")
        elif url_gatinhos == "https://i.pinimg.com/736x/bf/44/78/bf4478888a2da33dbb185b14cb6e779a.jpg":
            embed.set_footer(text="😳😨")
        elif url_gatinhos == "https://images-ext-1.discordapp.net/external/03rJR9SF16vYYOxnlLrHGgRvNtjnf8pMIVf5gsxJwZc/https/i.pinimg.com/736x/09/c9/c8/09c9c8b00dafa7654ad4226a6c2c884e.jpg?format=webp":
            embed.set_footer(text="😱")
        else:
            embed.set_footer(text="Olha que gatinho bonitinho 🥺")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kiss", description="Um bjinho")
    async def kiss(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(
            description=f"{interaction.user.mention} beijou {member.mention}!",
            color=0xff69b4
        )
        url_kiss = random.choice(media["gifs"]["kiss"])
        embed.set_image(url=url_kiss)
        embed.set_footer(text="MMwwaaaa")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
