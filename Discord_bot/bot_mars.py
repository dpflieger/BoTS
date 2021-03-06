#!/usr/bin/env python3
# coding: utf-8

import aiohttp
import asyncio
import discord
import json
import random
import requests
from discord.ext.commands import CommandNotFound
from discord.ext.commands import Bot
from discord.ext import commands
from string import Template

BOT_PREFIX = ("?", "!")

with open("token.txt", "r") as f:
    TOKEN = f.read()

bot = Bot(command_prefix=BOT_PREFIX, description="A 'funny' BOT")

def get_fotw():
    """
    Returns a random youtube link from DotaCinema Fails of the Week playlist
    Link to channel --> https://www.youtube.com/channel/UCNRQ-DWUXf4UVN9L31Y9f3Q
    """
    # Channel
    url = "https://www.youtube.com/playlist?list=PLE14F2057980335BE"
    page = requests.get(url).content
    data = str(page).split(' ')
    item = 'href="/watch?'
    vids = [line.replace('href="', '"https://www.youtube.com').strip('"') for line in data if item in line]
    return(random.choice(vids))

def get_joke():
    """
    Returns a random joke from the jokes.txt file
    """
    with open("jokes.txt", encoding = "UTF-8") as f:
        joke = random.choice(f.readlines())
        return(joke)

def get_dota_joke():
    """
    Returns a random joke from the mars.txt file
    The mars.txt is an old heritage of the battle.net bots
    """
    with open("mars.txt", encoding = "UTF-8") as f:
        joke = random.choice(f.readlines())
        return(joke)

# #https://stackoverflow.com/questions/43963366/discord-py-module-how-do-i-remove-the-command-text-afterwards
# @bot.event
# async def on_message(message):
#     """
#     Removes command message
#     """
#     if message.content.startswith(BOT_PREFIX):
#         await message.delete()
#     await bot.process_commands(message)

@bot.event
async def on_ready():
    print("------------------------------------")
    print("Bot Name: ", bot.user.name)
    print("Bot ID: ", bot.user.id)
    print("Discord version: ", discord.__version__)
    print("------------------------------------")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

# see https://stackoverflow.com/questions/52348148/delete-messages-with-python-discord-bot
@bot.command(pass_context=True)
async def purge(ctx, limit = 1, member: discord.Member = None, *, matches: str = None):
    """
    Purge all messages, optionally from `member` or contains `matches`.
    """
    def check_msg(msg):
        if msg.id == ctx.message.id:
            return True
        if member is not None:
            if msg.author.id != member.id:
                return False
        if matches is not None:
            if matches not in msg.content:
                return False
        return True
    deleted = await ctx.channel.purge(limit=limit, check=check_msg)
    ##msg = await ctx.send(ctx, 'purge', len(deleted))
    ##await asyncio.sleep(1)
    #await msg.delete()
    await ctx.send('Deleted {} message(s)'.format(len(deleted)))

@bot.command(pass_context = True)
async def hello(ctx):
    await ctx.send(f"Hi {ctx.message.author.display_name}!")

@bot.command()
async def bitcoin(ctx):
    """
    Get the bitcoin price in Euro
    """
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await ctx.send(f"Bitcoin price is: € {response['bpi']['EUR']['rate']}")

@bot.command()
async def ping(ctx):
    """
    Get the latency of the bot
    """
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(round(latency, 3))

@bot.command()
async def echo(ctx, *, content : str):
    await ctx.send(content)

@bot.command()
async def mras(ctx):
    await ctx.send("https://giphy.com/gifs/mars-dave-chapelle-chapell-show-h3KQUcJ6T3os0")

@bot.command()
async def masr(ctx):
    await ctx.send("https://giphy.com/gifs/mars-dave-chapelle-chapell-show-h3KQUcJ6T3os0")

@bot.command()
async def amrs(ctx):
    await ctx.send("https://giphy.com/gifs/mars-dave-chapelle-chapell-show-h3KQUcJ6T3os0")

@bot.command()
async def amsr(ctx):
    await ctx.send("https://giphy.com/gifs/mars-dave-chapelle-chapell-show-h3KQUcJ6T3os0")

@bot.command(pass_context = True)
async def mars(ctx):
    """
    Return a DotA joke.
    Similar to the good old !mars command of the battle.net bots :)
    """
    random_user = random.choice([user for user in bot.users if user != ctx.message.author])
    dota_joke = Template(get_dota_joke())
    dota_joke = dota_joke.substitute(victim = ctx.message.author.display_name, random = random_user.display_name)
    await ctx.send(dota_joke)

@bot.command()
async def joke(ctx):
    await ctx.send(get_joke())

@bot.command()
async def fotw(ctx):
    await ctx.send(get_fotw())

bot.run(TOKEN)
