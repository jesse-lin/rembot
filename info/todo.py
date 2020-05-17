import discord
import os
import sys
from discord.ext import commands
import json

import datetime

from variables import FILEPATH

async def list_todo(ctx, guild, user):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
        if mdata[guild][user]['todo']:
            embed = discord.Embed(title=f"{ctx.author}'s todo list", 
                description= f"A personalized todo list for {ctx.author}")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            counter = 0
            for entry in mdata[guild][user]['todo']:
                difference = datetime.datetime.now() - datetime.datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")
                embed.add_field(name=f'{counter}', value=f"**{entry['value']}**\nAdded {difference.days} days ago", 
                    inline=False)
                counter += 1
            await ctx.send(embed=embed)
        else:
            await ctx.send(':no_entry_sign: **You have no items in your to-do list.**')

async def del_todo(ctx, guild, user, text):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    if str.isdigit(text):
        try:
            mdata[guild][user]['todo'].pop(int(text))
            with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
                json.dump(mdata, fm, indent=4)
            await ctx.send(f":white_check_mark: **Index {text} removed successfully.**")
            await list_todo(ctx, guild, user)
        except IndexError:
            await ctx.send(f":no_entry_sign: **{text} is not a valid index, try again.**")
    else:
        await ctx.send(":no_entry_sign: **Please enter a single integer value as an argument.**")

async def add_todo(ctx, guild, user, text):
    with open(f'{FILEPATH}/data/mem.json', 'r') as fm:
        mdata = json.load(fm)
    info = dict()
    info['value'] = text
    info['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mdata[guild][user]['todo'].append(info)
    with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
        json.dump(mdata, fm, indent=4)
    await ctx.send(":white_check_mark: **Todo item added.**")
    await list_todo(ctx, guild, user)

class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def todo(self, ctx, *, kwargs: str=None):
        with open(f'{FILEPATH}/data/bot.json', 'r') as f:
            data = json.load(f)
        if 'todo' not in data['commands']:
            info = dict()
            info['Name'] = 'todo'
            info['Description'] = 'A personalized task list for members to utilize.'
            usage = "!todo\n" \
                "!todo add <todo item>\n" \
                "!todo delete <single index as integer value>"
            info['Usage'] = usage
            data['commands']['todo'] = info
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
        if 'todo' not in mdata[guild_id][user]:
            mdata[guild_id][user]['todo'] = list()
        with open(f'{FILEPATH}/data/mem.json', 'w') as fm:
            json.dump(mdata, fm, indent=4)

        if kwargs==None:
            if mdata[guild_id][user]['todo']:
                await list_todo(ctx, guild_id, user)
            else:
                await ctx.send(':no_entry_sign: **You have no items in your to-do list.**')
        else:
            if kwargs.startswith('add'):
                text = kwargs[len('add '):]
                if not text:
                    await ctx.send(":no_entry_sign: **No arguments to add, please try again.**")
                else:
                    await add_todo(ctx, guild_id, user, text)
            elif kwargs.startswith('del'):
                if kwargs.startswith('delete'):
                    text = kwargs[len('delete '):]
                    if not text:
                        await ctx.send(":no_entry_sign: **Missing arguments, please try again.**")
                    else:
                        await del_todo(ctx, guild_id, user, text)
                elif kwargs.startswith('del '):
                    text = kwargs[len('del '):]
                    if not text:
                        await ctx.send(":no_entry_sign: **Missing arguments, please try again.**")
                    else:
                        await del_todo(ctx, guild_id, user, text)
            else:
                await ctx.send(":no_entry_sign: **Invalid arguments, try again.**")