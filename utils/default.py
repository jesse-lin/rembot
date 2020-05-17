import discord
from discord.ext import commands
import json
import sys
import os
import datetime
from variables import FILEPATH

from info import botinfo, meminfo

def update_bot(bot):
    fp = f'{FILEPATH}/data/bot.json'
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            data = json.load(f)
            data['info']['Server count'] = len(bot.guilds)
            data['info']['Last updated'] = datetime.datetime.now().isoformat()
        with open(fp, 'w') as f:    
            json.dump(data, f, indent=4)
    else:
        botinfo.set_defaults(bot, fp)
    fp = f'{FILEPATH}/data/mem.json'
    if not os.path.exists(fp):
        meminfo.set_defaults(bot, fp)