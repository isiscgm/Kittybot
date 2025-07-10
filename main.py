# main.py
import os
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import time

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='k!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    sincs = await bot.tree.sync()
    print(f"Sincronizados {len(sincs)} comandos slash.")
    await bot.change_presence(activity=discord.Game(name="✨  k!help para mais informações  ✨"))
    gatin_task.start()
    print("Bot iniciado com sucesso!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.reference:
        return

    if bot.user in message.mentions:
        await message.channel.send(
            f"Oi, {message.author.mention}! Como posso ajudar você hoje? Se quiser saber mais sobre minhas funções, digite `k!help` ✨ !"
        )

    await bot.process_commands(message)


@tasks.loop(time=time(hour=10, minute=0))
async def gatin_task():
    channel = bot.get_channel(1391467247133786202)
    if channel:
        cog = bot.get_cog("Miscellaneous")
        if cog is not None:
            class FakeCtx:
                def __init__(self, channel):
                    self.channel = channel

                async def send(self, *args, **kwargs):
                    await self.channel.send(*args, **kwargs)

            fake_ctx = FakeCtx(channel)
            await cog.send_random_gatinho(fake_ctx)

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            ext_name = f"cogs.{filename[:-3]}"
            if ext_name not in bot.extensions:
                await bot.load_extension(ext_name)
                print(f"Cog carregado: {ext_name}")
            else:
                print(f"Cog já está carregado: {ext_name}")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)

asyncio.run(main())
