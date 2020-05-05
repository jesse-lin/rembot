import discord
import os
import sys
from discord.ext import commands

sys.path.append('/home/jesse/projects/rembot')

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.mention}~')
        else:
            await ctx.send(f'Hello {member.mention}... this feels familiar...')
        self._last_member = member

    @commands.command()
    async def rembot(self, ctx):
        embed = discord.Embed(title="RemBot", description=self.bot.description)
        embed.set_thumbnail(url="https://i.imgur.com/oNUY7dx.jpg")
        embed.add_field(name="Author", value='<@260913181734469655>')
        embed.add_field(name="Server count", value=f'{len(self.bot.guilds)}')
        embed.add_field(name="Date created", value='2020/04/30')
        # embed.set_image(url="https://i.imgur.com/oNUY7dx.jpg")

        await ctx.send(content=None, embed=embed)