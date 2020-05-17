import discord
import os
import sys
from discord.ext import commands
import json

import yfinance as yf
import lxml

from variables import FILEPATH

def set_defaults(bot, fp):
    with open(fp, 'w+') as f:
        data = dict()
        # data[f'<@!{bot.user.id}>'] = None
        json.dump(data, f, indent=4)

def check_stock(stock):
    ss = yf.Ticker(stock)
    ss.info
    hist = ss.history(period="max")

async def add_stocks(ctx, user, tickers):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    ser = f'{ctx.guild.id}'
    for elem in tickers:
        up = elem.upper()
        test = yf.Ticker(up)
        info_json = f'{test.history(period="5d").to_json()}'
        info = json.loads(info_json)
        if info["Open"]:
            if up not in mdata[ser][user]['stocks']:
                mdata[ser][user]['stocks'].append(up)
        else:
            await ctx.send(f":no_entry_sign: **Data not found for {up}, "
                            "sorry.**")
            
    with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
        json.dump(mdata, fm, indent=4)
    await ctx.send(':white_check_mark: **OK, done.**')
    await list_stocks(ctx, user, mdata[ser][user]['stocks'])
    
async def del_stocks(ctx, user, tickers):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    ser = f'{ctx.guild.id}'
    for elem in tickers:
        up = elem.upper()
        if up in mdata[ser][user]['stocks']:
            mdata[ser][user]['stocks'].remove(up)
    with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
        json.dump(mdata, fm, indent=4)
    await ctx.send(':white_check_mark: **OK, done.**')
    await list_stocks(ctx, user, mdata[ser][user]['stocks'])

async def clear_stocks(ctx, user):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    ser = f'{ctx.guild.id}'
    mdata[ser][user]['stocks'].clear()
    with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
        json.dump(mdata, fm, indent=4)
    await ctx.send(':white_check_mark: **OK, done.**')

async def list_stocks(ctx, user, tickers):
    str1 = ''
    embed = discord.Embed(title=f"{ctx.author}'s symbol list", 
        description=f":chart_with_upwards_trend: **A quick list of stock symbols "
                    f"for {ctx.author}**")
    embed.set_thumbnail(url=ctx.author.avatar_url)
    for sym in tickers:
        str1 += f'{sym}\n'
    embed.add_field(name='Symbols', value=str1, inline=False)
    await ctx.send(embed=embed)

class MemInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None