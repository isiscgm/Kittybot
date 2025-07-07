import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed = discord.Embed(
            title="Bem-vindo ao servidor! 🎉",
            description=f"Olá {member.mention}, seja bem-vindo(a) ao servidor! Esperamos que você se divirta aqui! ✨",
            color=0xff69b4
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
        embed.set_footer(text=f"ID do usuário: {member.id}")
        canal = self.bot.get_channel(1391462069253181490)
        if canal:
            await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        embed = discord.Embed(
            title="Até logo! 👋",
            description=f"{member.mention} saiu do servidor. Esperamos que volte em breve! 😕",
            color=0xff69b4
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
        embed.set_footer(text=f"ID do usuário: {member.id}")
        canal = self.bot.get_channel(1391462069253181490)
        if canal:
            await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Events(bot))
