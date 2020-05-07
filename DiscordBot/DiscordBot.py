import discord
import lyricsgenius as genius
from joke.jokes import *
import math
from random import choice
from googletrans import Translator
import urbandictionary as ud
from PyLyrics import *
from archbase import handle
client = discord.Client()
translator = Translator()
filepath = 'keys.txt'
with open(filepath) as fp:
   key = fp.readline()
   geniuskey = fp.readline()
geniusCreds = geniuskey
api = genius.Genius(geniusCreds)
def lyrr(artist,songg):
    song = api.search_song(songg, artist)
    if song == None:
        return ("Couldn't find the lyrics for this song: **" + songg+'**'   ) 
    return('**' + song.artist + ' - ' + song.title+ '**' + '\n' + song.lyrics)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

help_message = '''**!sb** - convert from RV32 to binary
!sh** - convert from RV32 to hexa
**!tr** - translate from any language to Arabic
**!u** - search urban dictionary
**!joke** - get a random bad joke that's probably about Chuck Norris
**good bot** - to make the bot happy
'''
worked = 0
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    t = message.content
    if t.startswith('!u'):
        defs = ud.define(t[3:])
        t = defs[0].definition
        t = t.replace(']','')
        t = t.replace('[','')
        await message.channel.send(t)
    elif t.startswith('!tr'):
        await message.channel.send(translator.translate(t[4:],dest = 'ar').text)
    elif t.startswith('!sh'):
        await message.channel.send(handle(message.content[3:],'h'))
    elif t.startswith('!sb'):
        await message.channel.send(handle(message.content[3:],'b'))
    elif t.startswith('!joke'):
        await message.channel.send(choice([geek, icanhazdad, chucknorris, icndb])())
    elif t.startswith('good bot'):
        await message.channel.send('<3')
    elif t.startswith('bad bot'):
        await message.channel.send('<3')
    elif t.startswith('!help'):
        await message.channel.send(help_message)
    elif t.startswith('!lyrics'):
        await message.channel.send("Searching...")
        lyrics = ''
        if t.find(',')!=-1:
            lyrics = lyrr(t[t.find(',')+1:],t[8:t.find(',')]).split('\n')
        else:
            lyrics = lyrr('',t[8:]).split('\n')
        current = ''
        for i in range (len(lyrics)):
            if len(lyrics[i])>1:
                current+=lyrics[i] + '\n'
            if((i%10==0 and i>0) or i==len(lyrics)-1):
                await message.channel.send(current)
                worked = 0
            if i%10==0 and i!=0:
                current = ''
        

client.run(key[:-1])
