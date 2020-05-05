import discord
from discord.ext import commands
import json

async def about(bot, message):
    embed = discord.Embed(title="RemBot", description=bot.description)
    embed.set_thumbnail(url="https://i.imgur.com/oNUY7dx.jpg")
    embed.add_field(name="Author", value='<@260913181734469655>')
    embed.add_field(name="Server count", value=f'{len(bot.guilds)}')
    embed.add_field(name="Date created", value='2020/04/30')
    # embed.set_image(url="https://i.imgur.com/oNUY7dx.jpg")

    await message.channel.send(content="About me:", embed=embed)

