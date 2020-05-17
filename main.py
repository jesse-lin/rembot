import discord
import os
import sys
from discord.ext import commands

from variables import TOKEN, FILEPATH
from commands import basic, funcommands
from info import botinfo, meminfo
from utils import default

BOT_PREFIX = '!'


bot = commands.Bot(command_prefix=BOT_PREFIX, description='A discord bot designed with simple commands.')
bot.add_cog(basic.Basic(bot))
bot.add_cog(funcommands.Fun(bot))
bot.add_cog(botinfo.BotInfo(bot))
bot.add_cog(meminfo.MemInfo(bot))


@bot.event
async def on_ready():
    default.update_bot(bot)
    print(f'Logged in as {bot.user.name}{bot.user.id}------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == f'<@!{bot.user.id}>':
        await botinfo.about(message)
    await bot.process_commands(message)


bot.run(TOKEN)
