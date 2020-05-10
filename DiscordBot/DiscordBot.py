import discord
import time as timee
import sched
import json
import os
import _thread
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from discord.ext import commands
filepath = 'keys.txt'
with open(filepath) as fp:
   key = fp.readline()
prefixes = {}
so7oorlist = set()
filesize = os.path.getsize("prefixes.json")
if filesize!=0:
    with open('prefixes.json') as json_file:
        prefixes = json.load(json_file)
data = []
with open('times.txt') as f:
    for line in f:
        data.append(int(line.split()[0]))
default_prefix = '$'

bot = commands.Bot(command_prefix= default_prefix)
@bot.event
async def on_ready() :
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("with your feelings")
    await bot.change_presence(status=discord.Status.online, activity=game)
    await fajr()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    t = message.content
    t = t.split()
    if len(t) == 2 and len(t[1])==1 and t[0] == 'prefix':
        prefix = t[1]
        prefixes[str(message.author.guild.id)] = prefix
        with open('prefixes.json', 'w') as outfile:
            json.dump(prefixes, outfile)
        bot.command_prefix = prefix

    if str(message.author.guild.id) in prefixes:
        bot.command_prefix = prefixes[str(message.author.guild.id)]   
    else:
        bot.command_prefix = default_prefix
        prefixes[str(message.author.guild.id)] = default_prefix
        with open('prefixes.json', 'w') as outfile:
            json.dump(prefixes, outfile)
    if message.content == 'prefix':
        await message.channel.send(prefixes[str(message.author.guild.id)])
    await bot.process_commands(message)


@bot.command()
async def notify(ctx, arg):
    if ctx.author.id == 99566441992290304 or arg == ctx.author.mention:
        so7oorlist.add(arg)
    else:
        pass
@bot.command()
async def sendnow(ctx):
    for name in so7oorlist:
        await ctx.send(name)
@bot.command()
async def time(ctx):
    t = timee.localtime()
    await ctx.send(str(t.tm_hour) + ':' + str(t.tm_min))
@bot.command()
async def broadcast(ctx, *args):
    if ctx.author.id == 99566441992290304:
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.type.name =='text' and channel.name =='general':
                    await channel.send(' '.join(args))
@bot.command()
async def echo(ctx, *args):
    await ctx.send(' '.join(args))
@bot.command()
async def mention(ctx,arg):
    for guild in bot.guilds:
        for member in guild.members:
            if member.name.lower().find(arg.lower())!=-1:
                await guild.channels[2].send(member.mention)
                c= 1
            d = 1


@bot.command()
async def mentionall(ctx):
    voiceChannels = []
    for c in ctx.guild.channels:
        if c.type.name == 'voice':
            voiceChannels.append(c)
    for c in voiceChannels:
        for user in c.members:
            if user.bot == False:
                    await ctx.send(user.mention)
@bot.command()
async def marmt(ctx):
    user = ctx.message.mentions[0]
    voiceChannels = []
    members = None
    for c in ctx.guild.channels:
        if c.type.name == 'voice':
            voiceChannels.append(c)
            members = ctx.guild.members
    if user in members:
        original = user.voice.channel
        if original == None:
            await ctx.send("User not in a voice channel")
        else:
            if user.bot == False:
                if len(voiceChannels)>1:
                    for currentChannel in voiceChannels:
                        if currentChannel!=original:
                            await user.move_to(currentChannel)
                    await user.move_to(original)
    else:
        await ctx.send("User not here")
@bot.command()
async def fajr():
    index = 0
    target = 215
    while True:
        
        t = timee.localtime()
        hour = t.tm_hour
        min = t.tm_min
        timenow = hour*60 + min
        #target = data[index]
        delay = target-timenow
        if(delay<0):
            delay+=1440
        print(delay)
        await asyncio.sleep(delay*60)  # every 30 minutes
        index+=1
        target+=1
        currenttext = None
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.type.name =='text' and channel.name =='general':
                    #channel = bot.get_channel(702681453028442115)
                    #await channel.send('eshrab maya now')
                    currenttext = channel
            voiceChannels = []
            for c in guild.channels:
                if c.type.name == 'voice':
                    voiceChannels.append(c)
            for c in voiceChannels:
                for user in c.members:
                    if user.bot == False:
                        await currenttext.send(user.mention)
bot.run(key)
