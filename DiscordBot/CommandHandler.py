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
default_prefix = '$'
bot = commands.Bot(command_prefix= default_prefix)
modules = ['Modules.TextModule', 'Modules.CustomModule']


filepath = 'keys.txt'
key = ''
with open(filepath) as fp:
   key = fp.readline()

prefixes = {}
filesize = os.path.getsize("prefixes.json")
if filesize!=0:
    with open('prefixes.json') as json_file:
        prefixes = json.load(json_file)


@bot.event
async def on_ready() :
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("with your feelings")
    await bot.change_presence(status=discord.Status.online, activity=game)
    for m in modules:
        bot.load_extension(m)

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
    
       
bot.run(key)
