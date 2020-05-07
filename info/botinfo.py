import discord
from discord.ext import commands
import json
import os
import datetime

def check_json(bot, file):
    try:
        data = json.load(file)
        data['info']['Server count'] = len(bot.guilds)
        data['info']['Last accessed'] = datetime.datetime.now().isoformat()
    except ValueError:
        data = dict()
        info = dict()
        data['Title'] = 'RemBot'
        data['Description'] = bot.description
        info['Author'] = '<@260913181734469655>'
        info['Server count'] = len(bot.guilds)
        info['Date created'] = datetime.datetime(2020, 4, 30, 17, 55, 000000).isoformat()
        info['Last accessed'] = datetime.datetime.now().isoformat()
        data['info'] = info
        data['thumbnail'] = "https://i.imgur.com/oNUY7dx.jpg"
        data['commands'] = dict()
        json.dump(data, file, indent=4)
    output = json.dumps(data)
    return output


async def about(str1: str, message):
    data = json.loads(str1)
    embed = discord.Embed(title=data['Title'], description=data['Description'])
    embed.set_thumbnail(url=data['thumbnail'])
    for key in data['info']:
        embed.add_field(name=f'{key}', value=data['info'][f'{key}'], inline=False)
        # embed.set_image(url="https://i.imgur.com/oNUY7dx.jpg")

    await message.channel.send(content="About me:", embed=embed)

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command()
    async def commands(self, ctx, *, str1: str = None):
        # if str1==None:
        #     await ctx.send('hello there')
        # else:
        #     await ctx.send(f'hello {str1}')
        with open('botinfo.json') as f:
            try:
                data = json.load(f)
            except ValueError:
                data = dict()