import discord
import os
import sys
from discord.ext import commands

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def restart(self, ctx: commands.Context):
        if ctx.author.id != 558421253409603585:
            await ctx.reply("🚫 Você não tem permissão para reiniciar o bot.")
            return

        await ctx.reply("♻️ Reiniciando o bot...")
        print("Reiniciando o bot...")
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command()
    async def help(self, ctx:commands.Context):
        embed = discord.Embed(
            title="Comandos disponíveis",
            description="Aqui estão todos os meus comandos disponíveis no momento:",
            color=0xff69b4
        )
        embed.add_field(name="`k!help`", value="Mostra esta mensagem de ajuda.", inline=False)
        embed.add_field(name="`k!kitty`", value="Informações?? Eu tenho! 😄", inline=False)
        embed.add_field(name="`k!avatar [@usuário]`", value="Mostra o avatar do usuário mencionado ou do autor do comando, caso não mencione ninguém!", inline=False)
        embed.add_field(name="`k!ping`", value="Mostra a latência do bot.", inline=False)
        embed.add_field(name="`k!gatinhos`", value="Mostra um gif aleatório de gatinhos", inline=False)
        embed.add_field(name="`k!userinfo [@usuário]`", value="Mostra informações sobre o usuário mencionado ou do autor do comando, caso não mencione ninguém!", inline=False)
        embed.add_field(name="`k!serverinfo`", value="Mostra informações sobre o servidor atual.", inline=False)
        embed.add_field(name="`k!say <mensagem>`", value="Faz o bot enviar a mensagem especificada.", inline=False)
        embed.add_field(name="`k!kiss @usuário`", value="Manda um beijo para o usuário mencionado.", inline=False)
        embed.add_field(name="\u200b", value="", inline=False)
        embed.add_field(name="**🎶 Comandos de música 🎶**", value="\u200b", inline=False)
        embed.add_field(name="`k!play <URL>`", value="Toca uma música do YouTube no canal de voz que você está", inline=False)
        embed.add_field(name="`k!np`", value="Mostra qual música está tocando no momento.", inline=False)
        embed.add_field(name="`k!queuel`", value="Mostra a fila de músicas.", inline=False)
        embed.add_field(name="`k!skip`", value="Pula a música atual.", inline=False)
        embed.add_field(name="`k!pause`", value="Pausa a música atual.", inline=False)
        embed.add_field(name="`k!resume`", value="Retoma a música pausada.", inline=False)
        embed.add_field(name="`k!clear`", value="Limpa a fila de músicas.", inline=False)
        embed.add_field(name="`k!join`", value="Faz o bot entrar no canal de voz que você está.", inline=False)
        embed.add_field(name="`k!shuffle`", value="Embaralha a fila de músicas.", inline=False)
        embed.add_field(name="`k!remove <posição>`", value="Remove uma música da fila pelo número da posição.", inline=False)
        embed.add_field(name="`k!move <de> <para>`", value="Move uma música de uma posição para outra na fila.", inline=False)
        embed.add_field(name="`k!loop`", value="Ativa ou desativa o loop da música atual.", inline=False)
        embed.add_field(name="`k!nowplaying`", value="Mostra a música que está tocando no momento.", inline=False)
        embed.add_field(name="`k!leave`", value="Desconecta o bot do canal de voz.", inline=False)
        embed.set_footer(text="Use e abuse dos comandos! ✨")
        await ctx.reply(embed=embed)

    @commands.command()
    async def kitty(self, ctx:commands.Context):
        nome = ctx.author.mention
        await ctx.reply(f"Oi, {nome}! Como posso ajudar você hoje? Se quiser saber mais sobre minhas funções, digite `k!help` ✨ !")

    @commands.command()
    async def say(self, ctx, *, args: str):
        try:
            canal = ctx.channel
            mensagem = args

            if ctx.message.channel_mentions:
                canal = ctx.message.channel_mentions[0]
                canal_mention_str = f"<#{canal.id}>"
                mensagem = mensagem.replace(canal_mention_str, "").strip()

            if not mensagem:
                await ctx.reply("❌ Você precisa escrever uma mensagem para enviar.")
                return

            await canal.send(mensagem)

            try:
                await ctx.message.delete()
            except discord.Forbidden:
                pass

        except Exception as e:
            await ctx.reply(f"❌ Erro ao tentar enviar a mensagem:\n`{e}`")
    
    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        if ctx.author.id != 558421253409603585:
            await ctx.reply("🚫 Você não tem permissão para desligar o bot.")
            return

        embed = discord.Embed(
            title="Desligando o bot... 🛑",
            description="O bot está sendo desligado. Até a próxima!",
            color=0xff69b4
        )
        await ctx.reply(embed=embed)
        await self.bot.close()
        print("Bot desligado com sucesso!")


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
