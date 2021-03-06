import discord
import time as timee
import sched
import json
import os
from os import walk
from os import path
import sys
import asyncio
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
from os import system
import urllib.request
from bs4 import BeautifulSoup
import lyricsgenius as genius
song = ''
geniuspath = os.path.dirname(os.path.abspath(__file__))
filepath = geniuspath +'\..\\keys.txt'
key = ''
with open(filepath) as fp:
    key = fp.readline()
    key = fp.readline()
api = genius.Genius(key)

def lyrr(artist, songg):
    song = api.search_song(songg, artist)
    if song == None:
        return ("Couldn't find the lyrics for this song: **" + songg+'**')
    return('**' + song.artist + ' - ' + song.title + '**' + '\n' + song.lyrics)
def youtubeSearch(song):
    query = urllib.parse.quote(song)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if (vid['href'].find('watch?v')!=-1):
            return('https://www.youtube.com' + vid['href'])
youtube_dl.utils.bug_reports_message = lambda: ''
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
    global song
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
    async def stream(self, ctx, *url):
        global song
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
        newurl = ''
        if len(url)==0:
            await ctx.send('Enter the name or the link of a song.')
        else:
            if url[0].find('.com')==-1:
                song = ' '.join(url)
                newurl = youtubeSearch(song)
            else:
                newurl = url[0]
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
            player = await YTDLSource.from_url(newurl, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(
                'Player error: %s' % e) if e else None)
        embed = discord.Embed(title = "Now playing:", description = player.title, color = 0x00FFFF)
        song = player.title
        await ctx.send(embed = embed)

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

    @commands.command(aliases = ['next','skip'])
    async def stop(self, ctx):
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.stop()
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
    async def lyrics(self, ctx, *arg):
        global song
        if len(arg)==0:
            pass
        else:
            song = ' '.join(arg)
        lyrics = ''
        if song.find(',') != -1:
            lyrics = lyrr(song[song.find(',')+1:], song[:song.find(',')]).split('\n')
        else:
            lyrics = lyrr('', song).split('\n')
        current = ''
        for i in range(len(lyrics)):
            if len(lyrics[i]) > 1:
                current += lyrics[i] + '\n'
            if((i % 10 == 0 and i > 0) or i == len(lyrics)-1):
                await ctx.send(current)
                worked = 0
            if i % 10 == 0 and i != 0:
                current = ''

    @commands.command()
    async def play(self, ctx, *url):
        global song
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
        newurl = ''
        if len(url)==0:
            await ctx.send('Enter the name or the link of a song.')
        else:
            if url[0].find('.com')==-1:
                song = ' '.join(url)
                newurl = youtubeSearch(song)
            else:
                newurl = url[0]
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
                ydl.download([newurl])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, 'song.mp3')
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio('song.mp3'))
            ctx.voice_client.play(source, after=lambda e: print(
                'Player error: %s' % e) if e else None)
            player = await YTDLSource.from_url(newurl, loop=self.bot.loop, stream=True)
            embed = discord.Embed(title = "Now playing:", description = player.title, color = 0x00FFFF)
            song = player.title
            await ctx.send(embed = embed)
    @commands.command()
    async def saved(self, ctx, *arg):
        global song
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
        v = 1.0 
        folder = ''
        if len(arg)==0:
            folder = 'sia'
        else:
            folder = arg[0]
        channel = None
        if ctx.author.voice != None:
            channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            if ctx.voice_client == ctx.author.voice.channel:
                pass
            else:
                await ctx.voice_client.move_to(channel)
        elif channel != None:
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
            i = 0
            msg = []
            msg = [None] * len(names)
            for name in names:
                name = str(name)
                if name!='names.txt' and path.exists(mypath+"\..\\savedmusic\\" + folder.lower() +"\\" +name):
                    source = discord.PCMVolumeTransformer(
                        discord.FFmpegPCMAudio(mypath+"\..\\savedmusic\\" + folder.lower() +"\\" +name))
                    ctx.voice_client.play(source, after=lambda e: print(
                        'Player error: %s' % e) if e else None)
                    ctx.voice_client.source.volume = v  
                    embed = discord.Embed(title = "Now playing:", description = name[:-4], color = 0x00FFFF)
                    msg[i] = await ctx.send(embed = embed)
                    song = name[:-4]
                    if i>0:
                        await msg[i-1].delete()
                    while ctx.voice_client.is_playing() or ctx.voice_client.is_paused() :
                        v = ctx.voice_client.source.volume
                        await asyncio.sleep(1)
                    i+=1
            voice = get(ctx.bot.voice_clients, guild=ctx.guild)
            voice.stop()

def setup(bot):
    bot.add_cog(VoiceModule(bot))
