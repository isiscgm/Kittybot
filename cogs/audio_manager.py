import discord
from discord.ext import commands
import yt_dlp
import random
import asyncio
import lyricsgenius
import time

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.current_songs = {}
        self.looping = {}

        # Genius API
        GENIUS_TOKEN = "wx4BekjlmDnlzZO0I1OdIRzeo1jQ-3gFdFhvyjx4yUHwsJtLZ4gS6l2KMxEzBLZz"
        self.genius = lyricsgenius.Genius(GENIUS_TOKEN)
        self.genius.skip_non_songs = True
        self.genius.excluded_terms = ["(Remix)", "(Live)"]

    def get_queue(self, guild_id):
        return self.queues.setdefault(guild_id, [])

    def get_current(self, guild_id):
        return self.current_songs.get(guild_id)

    def set_current(self, guild_id, song):
        self.current_songs[guild_id] = song

    def is_looping(self, guild_id):
        return self.looping.get(guild_id, False)

    def toggle_loop(self, guild_id):
        self.looping[guild_id] = not self.looping.get(guild_id, False)
        return self.looping[guild_id]

    def ffmpeg_options(self):
        return {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

    def after_playing(self, error, guild_id, voice_client, ctx):
        if error:
            print(f"Erro na reprodução: {error}")

        channel = ctx.channel

        async def play_next():
            queue = self.get_queue(guild_id)
            current = self.get_current(guild_id)

            if self.is_looping(guild_id) and current:
                url = current["url"]
                title = current["title"]
                source = discord.FFmpegPCMAudio(url, **self.ffmpeg_options())
                voice_client.play(source, after=lambda e: self.after_playing(e, guild_id, voice_client, ctx))
                await channel.send(f"🔁 Repetindo: **{title}**")
                return

            if queue:
                next_song = queue.pop(0)
                self.set_current(guild_id, next_song)
                source = discord.FFmpegPCMAudio(next_song["url"], **self.ffmpeg_options())
                voice_client.play(source, after=lambda e: self.after_playing(e, guild_id, voice_client, ctx))
                embed = discord.Embed(
                    title="🎶 Tocando agora",
                    description=f"**{next_song['title']}**",
                    color=0xff69b4
                )
                await channel.send(embed=embed)
            else:
                self.set_current(guild_id, None)
                embed = discord.Embed(
                    title="✅ A fila acabou.",
                    description="Nenhuma outra música foi adicionada a fila.",
                    color=0xff69b4
                )
                await channel.send(embed=embed)

        fut = asyncio.run_coroutine_threadsafe(play_next(), self.bot.loop)
        fut.result()

    # --- COMANDOS ---

    @commands.command(aliases=["ly", "l"])
    async def lyrics(self, ctx, *, query: str = None):
        if not query:
            await ctx.reply("❌ Você precisa enviar o nome da música ou artista para buscar a letra.")
            return
        try:
            song = self.genius.search_song(query)
            if not song:
                await ctx.reply("🚫 Não encontrei a letra dessa música 😿")
                return

            letra = song.lyrics
            if len(letra) > 4000:
                letra = letra[:3990] + "...\n(Letra cortada)"

            embed = discord.Embed(
                title=f"🎶 Lyrics: {song.title} - {song.artist}",
                description=letra,
                color=0xff69b4
            )
            await ctx.reply(embed=embed)

        except Exception as e:
            await ctx.reply(f"❌ Ocorreu um erro ao buscar a letra:\n`{e}`")

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.reply("🚫 Você precisa estar em um canal de voz para que eu possa entrar.")
            return
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.reply(f"✅ Entrei no canal **{channel.name}**!")
        else:
            await ctx.reply("🚫 Já estou em um canal de voz.")

    @commands.command(aliases=["p", "P"])
    async def play(self, ctx, *, query: str = None):
        guild_id = ctx.guild.id

        if ctx.author.voice is None:
            await ctx.reply("🚫 Você precisa estar em um canal de voz para tocar música.")
            return

        if not query:
            await ctx.reply("❌ Você precisa enviar um link válido do YouTube ou o nome da música.")
            return

        channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            voice_client = await channel.connect()
        else:
            voice_client = ctx.voice_client
            if voice_client.channel != channel:
                await voice_client.move_to(channel)

        if not (query.startswith("http://") or query.startswith("https://")):
            search_query = f"ytsearch1:{query}"
        else:
            search_query = query

        ydl_opts = {
            'format': 'bestaudio[ext=webm]/bestaudio',
            'quiet': True,
            'noplaylist': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                title = info.get("title", "Música")
                audio_url = info["url"]
                duration = info.get("duration", 0)  # duração em segundos

            source = discord.FFmpegPCMAudio(audio_url, **self.ffmpeg_options())

            song_data = {
                "url": audio_url,
                "title": title,
                "duration": duration,
                "start_time": time.time()
            }

            if voice_client.is_playing():
                self.get_queue(guild_id).append(song_data)
                await ctx.reply(f"✅ Música **{title}** adicionada à fila!")
            else:
                self.set_current(guild_id, song_data)
                voice_client.play(source, after=lambda e: self.after_playing(e, guild_id, voice_client, ctx))
                await ctx.reply(f"🎶 Tocando agora: **{title}**")

        except Exception as e:
            await ctx.reply(f"❌ Erro ao tocar a música:\n`{e}`")

    @commands.command(aliases=["s"])
    async def skip(self, ctx):
        guild_id = ctx.guild.id

        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            await ctx.reply("🚫 Não há música tocando no momento.")
            return

        ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            await ctx.reply("🚫 Não há música tocando no momento.")
            return

        ctx.voice_client.pause()
        await ctx.reply("🛑 Música pausada.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None or not ctx.voice_client.is_paused():
            await ctx.reply("🚫 Não há música pausada no momento.")
            return

        ctx.voice_client.resume()
        await ctx.reply("▶️ Música retomada.")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is None:
            await ctx.reply("🚫 O bot não está em um canal de voz.")
            return

        await ctx.voice_client.disconnect()
        guild_id = ctx.guild.id
        self.set_current(guild_id, None)
        self.get_queue(guild_id).clear()
        await ctx.reply("👋 Turum! ")

    @commands.command(aliases=["q"])
    async def queuel(self, ctx):
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        current_song = self.get_current(guild_id)

        if current_song is None and not queue:
            await ctx.reply("🚫 A fila está vazia.")
            return

        embed = discord.Embed(
            title="Fila atual 🎶",
            color=0xff69b4
        )

        if current_song:
            embed.add_field(name="▶️ TOCANDO AGORA", value=current_song["title"], inline=False)
        else:
            embed.add_field(name="▶️ TOCANDO AGORA", value="Nada no momento", inline=False)

        if queue:
            for i, song in enumerate(queue, start=1):
                embed.add_field(name=f"Posição {i}", value=song["title"], inline=False)
        else:
            embed.add_field(name="Próximas músicas", value="A fila está vazia.", inline=False)

        await ctx.reply(embed=embed)

    @commands.command()
    async def clear(self, ctx):
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)

        if not queue:
            await ctx.reply("🚫 A fila já está vazia.")
            return

        queue.clear()
        await ctx.reply("✅ Fila limpa com sucesso!")

    @commands.command()
    async def shuffle(self, ctx):
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)

        if not queue:
            await ctx.reply("🚫 A fila está vazia, não há como deixar aleatória.")
            return

        random.shuffle(queue)
        await ctx.reply("✅ Fila embaralhada com sucesso!")

    @commands.command()
    async def remove(self, ctx, position: int):
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)

        if not queue:
            await ctx.reply("🚫 A fila está vazia, não há músicas para remover.")
            return

        if position < 1 or position > len(queue):
            await ctx.reply("❌ Posição inválida. Use `k!queuel` para ver a fila atual.")
            return

        removed_song = queue.pop(position - 1)
        await ctx.reply(f"✅ Música **{removed_song['title']}** removida da fila.")

    @commands.command()
    async def move(self, ctx, from_pos: int, to_pos: int):
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)

        if not queue:
            await ctx.reply("🚫 A fila está vazia.")
            return

        if from_pos < 1 or from_pos > len(queue) or to_pos < 1 or to_pos > len(queue):
            await ctx.reply("❌ Posições inválidas. Use `k!queuel` para ver a fila atual.")
            return

        song = queue.pop(from_pos - 1)
        queue.insert(to_pos - 1, song)
        await ctx.reply(f"✅ Música **{song['title']}** movida de posição {from_pos} para {to_pos}.")

    @commands.command()
    async def loop(self, ctx):
        guild_id = ctx.guild.id

        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            await ctx.reply("🚫 Não há música tocando no momento.")
            return

        status = self.toggle_loop(guild_id)
        msg = "ativado" if status else "desativado"
        await ctx.reply(f"🔁 Loop {msg}!")

    @commands.command(aliases=["np"])
    async def nowplaying(self, ctx):
        song = self.get_current(ctx.guild.id)

        if song:
            start_time = song.get("start_time", None)
            duration = song.get("duration", 0)
            title = song.get("title", "Desconhecida")

            if start_time is None:
                elapsed = 0
            else:
                elapsed = int(time.time() - start_time)
                if elapsed > duration:
                    elapsed = duration

            def format_time(seconds):
                minutes = seconds // 60
                seconds = seconds % 60
                return f"{minutes:02d}:{seconds:02d}"

            embed = discord.Embed(
                title="🎶 Tocando agora",
                description=f"**{title}**\n\n` ▶ {format_time(elapsed)} / {format_time(duration)}`",
                color=0xff69b4
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("🚫 Nenhuma música está tocando no momento.")

async def setup(bot):
    await bot.add_cog(Music(bot))
