import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run('NjEyMzQxNzE3OTY1OTk2MDQ0.XqoPKQ.Ew_iikAHJGpsEWFLpbPonEVAzdw')