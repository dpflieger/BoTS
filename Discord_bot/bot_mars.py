import random
import asyncio
import aiohttp
import json
import discord
from string import Template
from discord.ext import commands


BOT_PREFIX = ("?", "!")
TOKEN = open("token.txt", "r").read()

def get_jokes():
    pass

def get_dota_joke():
    with open("mars.txt", "r") as f:
        joke = random.choice(f.readlines())
        return(joke)

bot = commands.Bot(command_prefix=BOT_PREFIX, description='A bot that greets the user back.')

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id)

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
async def echo(ctx, *, content:str):
    await ctx.send(content)

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

@bot.command()
async def mars(ctx):
    dota_joke = Template(get_dota_joke())
    print(dota_joke)
    dota_joke = dota_joke.substitute(victim = ctx.message.author.display_name, random = ctx.message.author.display_name)
    await ctx.send(dota_joke)


""" @client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
 """

bot.run(TOKEN)
