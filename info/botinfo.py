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