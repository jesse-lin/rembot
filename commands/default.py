import discord
import os
import sys
from discord.ext import commands
import json

from info import botinfo
from variables import FILEPATH

# sys.path.append('/home/jesse/projects/rembot')

class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        data = json.loads(botinfo.check_json(self.bot))
        if 'hello' not in data['commands']:
            file = open(f'{FILEPATH}/data/bot.json', 'w+')
            info = dict()
            info['Name'] = 'hello'
            info['Description'] = 'The bot says hello back!'
            info['Usage'] = '!hello'
            data['commands']['hello'] = info
            json.dump(data, file, indent=4)
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.mention}~')
        else:
            await ctx.send(f'Hello {member.mention}... this feels familiar...')
        self._last_member = member
    