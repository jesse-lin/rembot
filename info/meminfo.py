import discord
import os
import sys
from discord.ext import commands
import json

import yfinance as yf
import lxml

from variables import FILEPATH

class MemInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None