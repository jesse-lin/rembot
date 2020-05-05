import discord
import os
import sys
from discord.ext import commands

from variables import TOKEN
from functions import basic_functions

BOT_PREFIX = '!'

bot = commands.Bot(command_prefix=BOT_PREFIX, description='A discord bot designed with simple commands.')
bot.add_cog(basic_functions.Basic(bot))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}{bot.user.id}------')

bot.run(TOKEN)
