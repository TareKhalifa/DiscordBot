import discord
import time as timee
import sched
import json
import os
import asyncio
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
from os import system


class VoiceModule(commands.Cog):
    def init(self, bot):
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
        voice.pause()

    @commands.command()
    async def resume(self, ctx):
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.resume()

    @commands.command()
    async def v(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def play(self, ctx, url: str):
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


def setup(bot):
    bot.add_cog(VoiceModule(bot))
