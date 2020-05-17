import discord
import os
import sys
from discord.ext import commands
import json
# import requests

import yfinance as yf
import lxml

import datetime

from variables import FILEPATH

class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        with open(f'{FILEPATH}/data/bot.json', 'r') as f:
            data = json.load(f)
        if 'hello' not in data['commands']:
            info = dict()
            info['Name'] = 'hello'
            info['Description'] = 'The bot says hello back!'
            info['Usage'] = '!hello'
            data['commands']['hello'] = info
            with open(f'{FILEPATH}/data/bot.json', 'w') as f:
                json.dump(data, f, indent=4)
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.mention}~')
        else:
            await ctx.send(f'Hello {member.mention}... this feels familiar...')
        self._last_member = member

    @commands.command()
    async def ping(self, ctx):
        with open(f'{FILEPATH}/data/bot.json', 'r') as f:
            data = json.load(f)
        if 'ping' not in data['commands']:
            info = dict()
            info['Name'] = 'ping'
            info['Description'] = 'Returns client roundtrip time.'
            info['Usage'] = '!ping'
            data['commands']['ping'] = info
            with open(f'{FILEPATH}/data/bot.json', 'w') as f:
                json.dump(data, f, indent=4)
        await ctx.send(f'{ctx.author.mention} Pong! {round(self.bot.latency*1000)} ms.')

    
            
            


    

    