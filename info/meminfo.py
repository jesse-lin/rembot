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
        data[f'<@!{bot.user.id}>'] = None
        json.dump(data, f, indent=4)

async def add_stocks(ctx, user, tickers):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    for elem in tickers:
        up = elem.upper()
        if not yf.Ticker(up):
            await ctx.send(f':no_entry_sign: **Data not found for {elem.upper()}, sorry.**')
            tickers.remove(up)
        elif up not in mdata[user]['stocks']:
            mdata[user]['stocks'].append(up)
    with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
        json.dump(mdata, fm, indent=4)
    await ctx.send(':white_check_mark: **OK, done.**')
    
async def del_stocks(ctx, user, tickers):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    for elem in tickers:
        up = elem.upper()
        if up in mdata[user]['stocks']:
            mdata[user]['stocks'].remove(up)
    with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
        json.dump(mdata, fm, indent=4)
    await ctx.send(':white_check_mark: **OK, done.**')


class MemInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None