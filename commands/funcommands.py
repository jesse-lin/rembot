import discord
import os
import sys
from discord.ext import commands
import json
import random

from variables import FILEPATH

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='8ball')
    async def eight_ball(self, ctx, str1: str=None):
        with open(f'{FILEPATH}/data/bot.json', 'r') as f:
            data = json.load(f)
        if '8ball' not in data['commands']:
            info = dict()
            info['Name'] = '8ball'
            info['Description'] = 'Answers a yes/no question.'
            info['Usage'] = '!8ball <question>'
            data['commands']['8ball'] = info
            with open(f'{FILEPATH}/data/bot.json', 'w') as f:
                json.dump(data, f, indent=4)
        if str1 == None:
            await ctx.send(f':no_entry_sign: **Please ask a question.**')
        else:
            possible_responses = [
                'As I see it, yes.',
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "It is certain.",
                "It is decidely so.",
                "Most likely.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Outlook good.",
                "Reply hazy, try again.",
                "Signs point to yes.",
                "Very doubtful.",
                "Yes.",
                "Yes - definitely.",
                "You may rely on it."
            ]
            await ctx.send(f'{random.choice(possible_responses)}')