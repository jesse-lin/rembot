import discord
from discord.ext import commands
import json
import sys
import os
import datetime
from variables import FILEPATH

# sys.path.append(FILEPATH)

def set_defaults(bot, fp):
    with open(fp, 'w+') as f:
            data = dict()
            info = dict()
            data['Title'] = 'RemBot'
            data['Description'] = bot.description
            info['Author'] = '<@260913181734469655>'
            info['Server count'] = len(bot.guilds)
            info['Date created'] = datetime.datetime(2020, 5, 1, 17, 55).strftime("%Y-%m-%d %H:%M:%S")
            info['Last updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data['info'] = info
            data['thumbnail'] = "https://i.imgur.com/oNUY7dx.jpg"
            data['commands'] = dict()
            json.dump(data, f, indent=4)        
        

async def about(message):
    f = open(f'{FILEPATH}/data/bot.json', 'r')
    data = json.load(f)
    f.close()
    embed = discord.Embed(title=data['Title'], description=data['Description'])
    embed.set_thumbnail(url=data['thumbnail'])
    for key in data['info']:
        embed.add_field(name=f'{key}', value=data['info'][f'{key}'], inline=False)
        # embed.set_image(url="https://i.imgur.com/oNUY7dx.jpg")
    embed.add_field(name='Repository link', value = 'https://github.com/jesse-lin/rembot', 
        inline=False)
    embed.add_field(name='For more commands', value = "Type '!commands' to see commands", 
        inline=False)

    await message.channel.send(content="About me:", embed=embed)

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command()
    async def commands(self, ctx, *, str1: str=None):
        f = open(f'{FILEPATH}/data/bot.json', 'r')
        data = json.load(f)
        f.close()
        if str1==None:
            if not data['commands']:
                await ctx.send(':warning: **There are currently no commands in this bot**')
            else:
                embed = discord.Embed(title='List of bot commands', description='')
                embed.set_thumbnail(url=data['thumbnail'])
                for key in data['commands']:
                    embed.add_field(name=f'{key}', value=data['commands'][f'{key}']['Description'], 
                        inline=False)
                await ctx.send(embed=embed)
        else:
            if str1 not in data['commands']:
                await ctx.send(f':no_entry_sign: **The command "{str1}" does not exist**')
            else:
                embed = discord.Embed(title=str1)
                embed.set_thumbnail(url=data['thumbnail'])
                for key in data['commands'][f'{str1}']:
                    embed.add_field(name=f'{key}', value=data['commands'][f'{str1}'][key], 
                        inline=False)
                await ctx.send(embed=embed)

