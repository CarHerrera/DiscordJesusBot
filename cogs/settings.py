import discord
from discord.ext import commands, tasks
class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client
def setup(client):
    client.add_cog(Settings(client))
