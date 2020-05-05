import discord
import os
import sys
from discord.ext import commands

from variables import TOKEN
from functions import basic_functions

BOT_PREFIX = '!'

client = discord.Client()

bot = commands.Bot(command_prefix=BOT_PREFIX, description='A discord bot designed with simple commands.')
bot.add_cog(basic_functions.Basic(bot))

@bot.event
async def on_message(message):
    # print(f'{message.content}')
    if message.author.bot: return
    if message.content == f'<@!{bot.user.id}>':

        embed = discord.Embed(title="RemBot", description=bot.description)
        embed.set_thumbnail(url="https://i.imgur.com/oNUY7dx.jpg")
        embed.add_field(name="Author", value='<@260913181734469655>')
        embed.add_field(name="Server count", value=f'{len(bot.guilds)}')
        embed.add_field(name="Date created", value='2020/04/30')
        # embed.set_image(url="https://i.imgur.com/oNUY7dx.jpg")

        await message.channel.send(content="About me:", embed=embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}{bot.user.id}------')




bot.run(TOKEN)
