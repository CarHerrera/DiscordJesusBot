import discord
from discord.ext import commands, tasks
class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client
def setup(client):
    client.add_cog(Utils(client))
