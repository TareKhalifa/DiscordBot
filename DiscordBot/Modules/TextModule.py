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
import discord
from discord.ext import commands
from CommandHandler import bot
class TextModule(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='!', case_insensitive=True, fetch_offline_members=True,
                         description="sssssssssssssssssssssssss")

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