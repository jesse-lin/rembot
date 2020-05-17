import discord
import os
import sys
from discord.ext import commands

from variables import TOKEN, FILEPATH
from commands import defaultcommands, funcommands
from info import botinfo, meminfo
from utils import default

BOT_PREFIX = '!'


bot = commands.Bot(command_prefix=BOT_PREFIX, description='A discord bot designed with simple commands.')
bot.add_cog(defaultcommands.Default(bot))
bot.add_cog(funcommands.Fun(bot))
bot.add_cog(botinfo.BotInfo(bot))
bot.add_cog(meminfo.MemInfo(bot))


@bot.event
async def on_ready():
    default.update_bot(bot)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!commands"))
    print(f'Logged in as {bot.user.name}{bot.user.id}------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == f'<@!{bot.user.id}>':
        await botinfo.about(message)
    await bot.process_commands(message)


bot.run(TOKEN)
