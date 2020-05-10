import discord
import time as timee
import sched
import json
import os
import asyncio
from discord.ext import commands
so7oorlist = set()

class CustomModule(commands.Cog):

    def init(self, bot):
            self.bot = bot
    @commands.command(aliases = [])
    async def notify(self,ctx, arg):
        if ctx.author.id == 99566441992290304 or arg == ctx.author.mention:
            so7oorlist.add(arg)
        else:
            pass
    @commands.command(aliases = [])
    async def sendnow(self,ctx):
        for name in so7oorlist:
            await ctx.send(name)
    @commands.command(aliases = [])
    async def time(self,ctx):
        t = timee.localtime()
        await ctx.send(str(t.tm_hour) + ':' + str(t.tm_min))
    @commands.command(aliases = [])
    async def broadcast(self,ctx, *args):
        if ctx.author.id == 99566441992290304:
            for guild in bot.guilds:
                for channel in guild.channels:
                    if channel.type.name =='text' and channel.name =='general':
                        await channel.send(' '.join(args))
    @commands.command(aliases = [])
    async def marmt(self,ctx):
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
    @commands.command(aliases = [])
    async def fajr():
        data = []
        with open('times.txt') as f:
            for line in f:
                data.append(int(line.split()[0]))
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
def setup(bot):
    bot.add_cog(CustomModule(bot))