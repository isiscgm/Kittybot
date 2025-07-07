import random
import discord
from discord.ext import commands
from discord import app_commands

kiss_gifs = [
    "https://media.tenor.com/HYXVuDJDa0kAAAAM/kittykiss-little-kitty.gif",
    "https://i.pinimg.com/originals/2d/13/97/2d139750db1e955f541629abedff550e.gif",
    "https://i.pinimg.com/originals/17/20/35/1720353613d7a0846551ab6aedfc80fb.gif",
    "https://i.pinimg.com/originals/4b/10/0a/4b100ab8e01e2fd042a1bbfd145fdf7a.gif",
    "https://gifdb.com/images/high/cute-love-bears-kiss-6z2hnlkt07swyep3.gif",
    "https://cdn.dribbble.com/userupload/21917588/file/original-5bb2d7704af66ce9847c9d071ecf8bb5.gif",
    "https://i.pinimg.com/originals/af/3f/66/af3f66c717a59ff330dae783025da0f2.gif"
]

gatinhos_url = [
    "https://64.media.tumblr.com/e14c82840178bf95581b35da6be576ef/tumblr_nivevmQOM91roi79do1_500.gif",
    "https://i.pinimg.com/originals/7c/fb/e3/7cfbe3f2823fefddcbe5de69a3ff70dc.gif",
    "https://i.pinimg.com/originals/b6/07/dd/b607ddeffd5084835b2fa170856c6a8b.gif",
    "https://i.pinimg.com/originals/b4/6e/53/b46e534af2aafe9c01e5ba6fa4558c30.gif",
    "https://24.media.tumblr.com/a498420c67dc1d4a6fda9e9d55439207/tumblr_mqrtemtJYS1sv98gio1_500.gif",
]

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gatinhos")
    async def gatinhos(self, ctx: commands.Context):
        url = random.choice(gatinhos_url)
        embed = discord.Embed(
            title="Gatinho do dia! 🐱",
            color=0xff69b4
        )
        embed.set_image(url=url)
        embed.set_footer(text="Olha que gatinho bonitinho 🥺")
        await ctx.send(embed=embed)

    @app_commands.command(name="kiss", description="Um bjinho")
    async def kiss(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(
            description=f"{interaction.user.mention} beijou {member.mention}!",
            color=0xff69b4
        )
        url_kiss = random.choice(kiss_gifs)
        embed.set_image(url=url_kiss)
        embed.set_footer(text="MMwwaaaa")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
