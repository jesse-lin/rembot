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

class Basic(commands.Cog):
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

    @commands.command(name='stock')
    async def stock_market(self, ctx, *, sym: str=None):
        with open(f'{FILEPATH}/data/bot.json', 'r') as f:
            data = json.load(f)
        if 'stock' not in data['commands']:
            info = dict()
            info['Name'] = 'stock'
            info['Description'] = 'Shows 5-day history for stock symbols.'
            info['Usage'] = '!stock\n!stock <list of symbols separated by spaces>'
            data['commands']['stock'] = info
            with open(f'{FILEPATH}/data/bot.json', 'w') as f:
                json.dump(data, f, indent=4)
        if sym==None:
            await ctx.send(f':no_entry_sign: **Please enter at least one symbol.**')
        else:
            tickers = sym.split(" ")
            for s in tickers:
                ss = s.upper()
                # stock = requests.get(f'https://query1.finance.yahoo.com/v7/finance/chart/{s.upper()}').json()
                stock = yf.Ticker(ss)
                info_json = f'{stock.history(period="5d").to_json()}'
                info = json.loads(info_json)
                embed = discord.Embed(title=ss, description = f':clock1: A 5-day history of {ss}')
                embed.set_thumbnail(url=data['thumbnail'])
                for key in info:
                    if key != 'Dividends' and key != 'Stock Splits':
                        str1 = ''
                        for val in info[key]:
                            newtime = datetime.date.fromtimestamp(int(val)/1e3).isoformat()
                            str1 += f'**{newtime}:** '
                            if key=='Open' or key=='High' or key=='Low' or key=='Close':
                                str1 += '$'
                            str1 += f'{info[key][val]}\n'
                        embed.add_field(name=key, value=str1, inline=False)
                try:
                    await ctx.send(embed=embed)
                except discord.errors.HTTPException:
                    await ctx.send(f':no_entry_sign: **Data not found for {ss}, try again.**')


    

    