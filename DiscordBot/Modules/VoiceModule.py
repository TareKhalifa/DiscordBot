import discord
import time as timee
import sched
import json
import os
from os import walk
import sys
import asyncio
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
from os import system

youtube_dl.utils.bug_reports_message = lambda: ''

paused = 0
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class VoiceModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *args: discord.VoiceChannel):
        channel = None
        if(len(args) != 0):
            channel = args[0]
        elif ctx.author.voice != None:
            channel = ctx.author.voice.channel
        else:
            await ctx.send("You are not in a voice channel nor did you specify a voice channel.")
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        if channel != None:
            await channel.connect()

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        channel = None
        if ctx.author.voice != None:
            channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        if channel != None:
            await channel.connect()
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(
                'Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def leave(self, ctx):
        channel = None
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("Don't think I am in a voice channel")

    @commands.command()
    async def pause(self, ctx):
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        paused = 1
        voice.pause()

    @commands.command()
    async def stop(self, ctx):
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.stop()
    @commands.command()
    async def resume(self, ctx):
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        paused = 0
        voice.resume()

    @commands.command()
    async def v(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def play(self, ctx, url: str):
        channel = None
        if ctx.author.voice != None:
            channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        if channel != None:
            await channel.connect()
        there = os.path.isfile("song.mp3")
        if there:
            os.remove("song.mp3")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio('song.mp3'))
        ctx.voice_client.play(source, after=lambda e: print(
            'Player error: %s' % e) if e else None)
    
    @commands.command()
    async def saved(self, ctx, *arg):
        folder = ''
        if len(arg)==0:
            folder = 'sia'
        else:
            folder = arg[0]
        channel = None
        if ctx.author.voice != None:
            channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        if channel != None:
            await channel.connect()
        mypath = os.path.dirname(os.path.abspath(__file__))
        f = open(mypath+"\..\\savedmusic\\" + folder.lower() +"\\names.txt")
        content = ''
        try:
            names = [line[:-1] for line in f]
            d= 1
            d = 1
            content = f.read()
        finally:
            f.close()
            print(names)
            #names[0] = names[0][3:]
            for name in names:
                name = str(name)
                if name!='names.txt':
                    source = discord.PCMVolumeTransformer(
                        discord.FFmpegPCMAudio(mypath+"\..\\savedmusic\\" + folder.lower() +"\\" +name))
                    ctx.voice_client.play(source, after=lambda e: print(
                        'Player error: %s' % e) if e else None)
                    await ctx.send('Now playing: '+ name[:-4])
                    while ctx.voice_client.is_playing() or paused==1:
                        await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(VoiceModule(bot))
