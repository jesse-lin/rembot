import discord
import os
import sys
from discord.ext import commands
import json

import datetime

import yfinance as yf
import lxml

from variables import FILEPATH

async def load_stocks(ctx, data, tickers):
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

async def add_stocks(ctx, user, tickers):
    counter = False
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    guild_id = f'{ctx.guild.id}'

    for elem in tickers:
        sym = elem.upper()
        ticker = yf.Ticker(sym)
        info_json = f'{ticker.history(period="5d").to_json()}'
        info_check = json.loads(info_json)
        if info_check["Open"]:
            if sym not in mdata[guild_id][user]['stocks']:
                mdata[guild_id][user]['stocks'].append(sym)
                await ctx.send(f':white_check_mark: **{sym} added.**')
            else:
                await ctx.send(f":warning: **{sym} already in list.**")
        else:
            await ctx.send(f":no_entry_sign: **Data not found for {sym}, "
                            "sorry.**")
            
    with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
        json.dump(mdata, fm, indent=4)        
    await list_stocks(ctx, user, mdata[guild_id][user]['stocks'])
    
async def del_stocks(ctx, user, tickers):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    guild_id = f'{ctx.guild.id}'
    for elem in tickers:
        sym = elem.upper()
        if sym in mdata[guild_id][user]['stocks']:
            mdata[guild_id][user]['stocks'].remove(sym)
            await ctx.send(f':white_check_mark: **{sym} removed.**')
        else:
            ctx.send(f':warning: **{sym} not in list.**')
    with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
        json.dump(mdata, fm, indent=4)
    
    await list_stocks(ctx, user, mdata[guild_id][user]['stocks'])

async def clear_stocks(ctx, user):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    guild_id = f'{ctx.guild.id}'
    mdata[guild_id][user]['stocks'].clear()
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

class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @commands.command(name='stock')
    async def stock_market(self, ctx, *, kwargs: str=None):
        with open(f'{FILEPATH}/data/bot.json', 'r') as f:
            data = json.load(f)
        if 'stock' not in data['commands']:
            info = dict()
            info['Name'] = 'stock'
            info['Description'] = 'Shows 5-day history for stock symbols.'
            usage = "!stock\n!stock list\n" \
                "!stock <list of symbols separated by spaces>\n" \
                "!stock add <list of symbols separated by spaces>\n" \
                "!stock delete <list of symbols separated by spaces>"
            info['Usage'] = usage
            data['commands']['stock'] = info
            with open(f'{FILEPATH}/data/bot.json', 'w') as f:
                json.dump(data, f, indent=4)

        with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
            mdata = json.load(fm)

        user = f'{ctx.author.id}'
        guild_id = f'{ctx.guild.id}'

        if guild_id not in mdata:
            mdata[guild_id] = dict()
        if user not in mdata[guild_id]:
            mdata[guild_id][user] = dict()
        if 'stocks' not in mdata[guild_id][user]:
            mdata[guild_id][user]['stocks'] = list()
        with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
            json.dump(mdata, fm, indent=4)

        if kwargs==None:
            if mdata[guild_id][user]['stocks']:
                await load_stocks(ctx, data, mdata[guild_id][user]['stocks'])
            else:
                await ctx.send(f':no_entry_sign: **You have no stock symbols saved.**')

        elif kwargs=="list":
            if mdata[guild_id][user]['stocks']:
                tickers = mdata[guild_id][user]['stocks']
                await list_stocks(ctx, user, tickers)
            else:
                with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
                    json.dump(mdata, fm, indent=4)
                await ctx.send(f':no_entry_sign: **You have no stock symbols saved.**')

        else:
            tickers = kwargs.split(' ')
            if kwargs.startswith("add"):
                tickers.pop(0)
                if not(tickers):
                    await ctx.send(":no_entry_sign: **Please enter at least one symbol "
                        "to be added.**")
                else:
                    await add_stocks(ctx, user, tickers)
            elif kwargs.startswith("delete"):
                tickers.pop(0)
                if not(tickers):
                    await ctx.send(":no_entry_sign: **Please enter at least one symbol "
                        "to be deleted.**")
                else:
                    await del_stocks(ctx, user, tickers)
            elif kwargs.startswith("clear"):
                await clear_stocks(ctx, user)
            else:
                await load_stocks(ctx, data, tickers)