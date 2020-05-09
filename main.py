import discord
import os
import sys
from discord.ext import commands

from variables import TOKEN, FILEPATH
from commands import default, funcommands
from info import botinfo

BOT_PREFIX = '!'


bot = commands.Bot(command_prefix=BOT_PREFIX, description='A discord bot designed with simple commands.')
bot.add_cog(default.Default(bot))
bot.add_cog(funcommands.Fun(bot))
bot.add_cog(botinfo.BotInfo(bot))


@bot.event
async def on_ready():
    botinfo.check_json(bot, f'{FILEPATH}/data/bot.json')
    print(f'Logged in as {bot.user.name}{bot.user.id}------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == f'<@!{bot.user.id}>':
        await botinfo.about(message)
    await bot.process_commands(message)


bot.run(TOKEN)
