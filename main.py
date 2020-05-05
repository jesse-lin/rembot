import discord
import os
import sys
from discord.ext import commands

from variables import TOKEN
from commands import default
from info import botinfo

BOT_PREFIX = '!'

# client = discord.Client()

bot = commands.Bot(command_prefix=BOT_PREFIX, description='A discord bot designed with simple commands.')
bot.add_cog(default.Default(bot))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}{bot.user.id}------')

@bot.event
async def on_message(message):
    # print(f'{message.content}')
    if message.author == bot.user:
        return

    if message.content == f'<@!{bot.user.id}>':
        botinfo.about(bot, message)

    await bot.process_commands(message)


bot.run(TOKEN)
