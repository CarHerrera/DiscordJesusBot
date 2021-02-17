import discord
from discord.ext import commands
vc = None
class Sounds(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.command()
    async def join(self, ctx):
        global vc
        try:
            print(vc)
            channel = ctx.author.voice.channel
            if vc == None:
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable = '/usr/bin/ffmpeg', source = '/home/pi/Desktop/DiscordJesusBot/sounds/undertaker.mp3'))
            else:
                vc.play(discord.FFmpegPCMAudio(executable = '/usr/bin/ffmpeg', source = '/home/pi/Desktop/DiscordJesusBot/sounds/undertaker.mp3'))
        except:
            await ctx.send('{.author.name} is not in a channel'.format(ctx))
    @commands.command()
    async def bonk(self,ctx):
        global vc
        try:
            print(vc)
            channel = ctx.author.voice.channel
            if vc == None:
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable = '/usr/bin/ffmpeg', source = '/home/pi/Desktop/DiscordJesusBot/sounds/bonk.mp3'))
            else:
                vc.play(discord.FFmpegPCMAudio(executable = '/usr/bin/ffmpeg', source = '/home/pi/Desktop/DiscordJesusBot/sounds/bonk.mp3'))
        except:
            await ctx.send('user is not in a voice channel')
    @commands.command()
    async def disc(self,ctx):
        global vc
        try:
            await vc.disconnect()
            vc = None
        except:
            await ctx.send('already not in a server')
def setup(client):
    client.add_cog(Sounds(client))
