import discord
import time as timee
import sched
import json
import os
import asyncio
from discord.ext import commands
class TextModule(commands.Cog):
    def init(self, bot):
            self.bot = bot
    @commands.command(
        name='echo',
        description='echo things',
        aliases=[]
    )
    async def echo(self, ctx, *args):
        await ctx.send(' '.join(args))
    @commands.command(
        name='mentionall',
        description='mention everyone',
        aliases=[]
    )
    async def mentionall(self,ctx):
        voiceChannels = []
        for c in ctx.guild.channels:
            if c.type.name == 'voice':
                voiceChannels.append(c)
        for c in voiceChannels:
            for user in c.members:
                if user.bot == False:
                        await ctx.send(user.mention)
    @commands.command(
        name='mention',
        description='mention someone',
        aliases=[]
    )
    async def mention(self,ctx,arg):
        for guild in bot.guilds:
            for member in guild.members:
                if member.name.lower().find(arg.lower())!=-1:
                    await guild.channels[2].send(member.mention)
                    c= 1
                d = 1
def setup(bot):
    bot.add_cog(TextModule(bot))