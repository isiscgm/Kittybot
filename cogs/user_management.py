import discord
from discord.ext import commands

class UserManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(
            title=f"Informações do usuário: {member.display_name}",
            color=0xff69b4
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="🆔 ID", value=member.id, inline=False)
        embed.add_field(name="🏷️ Nome", value=member.name, inline=False)
        embed.add_field(name="👤 Apelido", value=member.nick if member.nick else "Nenhum", inline=False)
        embed.add_field(name="📆 Criado em", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        embed.add_field(name="📅 Entrou no servidor em", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        status_map = {
            "online": "Online",
            "offline": "Offline",
            "idle": "Ausente",
            "dnd": "Não perturbe"
        }
        status_str = status_map.get(str(member.status), str(member.status).capitalize())
        embed.add_field(name="💠 Status", value=status_str, inline=False)
        embed.add_field(
            name="🎮 Jogando",
            value=member.activity.name if member.activity and hasattr(member.activity, "name") else "Nada no momento",
            inline=False
        )
        embed.add_field(name="🔗 Perfil", value=f"[Clique aqui]({member.avatar.url})", inline=False)
        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title=f"Informações do servidor: {guild.name}",
            color=0xff69b4
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
        embed.add_field(name="🆔 ID", value=guild.id, inline=False)
        embed.add_field(name="📅 Criado em", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        embed.add_field(name="👑 Dono", value=guild.owner.mention, inline=False)
        embed.add_field(name="👥 Membros", value=guild.member_count, inline=False)
        embed.add_field(name="📊 Canais", value=len(guild.channels), inline=False)

        invite_url = "Permissão insuficiente para criar convite"
        try:
            invite = await ctx.channel.create_invite(max_age=300, max_uses=1, unique=True)
            invite_url = invite.url
        except Exception:
            pass

        embed.add_field(name="🔗 Link de convite", value=f"[Clique aqui]({invite_url})", inline=False)
        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(
            title=f"Avatar de {member.display_name}",
            color=0xff69b4
        )
        embed.set_image(url=member.avatar.url)
        embed.set_footer(text=f"ID do usuário: {member.id}")
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(UserManagement(bot))
