import discord
from discord.ext import commands
class Help(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.group(invoke_without_command = True)
    async def help(self, ctx):
        attempt = discord.Embed(title = "All the commands currently in this bot", type = 'rich')
        attempt.set_thumbnail(url = 'https://i.imgur.com/GbDdMj2.png')
        attempt.add_field(name = "Commands", value = "$help commands")
        attempt.add_field(name = "Trigger Words", value ="$help trigger")
        attempt.add_field(name = "User Responses", value = "$help response")
        attempt.add_field(name = 'Work in Progress', value = "$help ip")
        attempt.add_field(name = "Emoting", value = '$help emotes')
        await ctx.send(embed = attempt)
    @help.command(name = 'commands')
    async def helpCommands(self, ctx):
        commands = discord.Embed(title = "Current comands the bot supports")
        commands.add_field(name = '$help', value = 'use to get more information on commands', inline = False)
        commands.add_field(name = '$hello', value = 'Literally tells you to fuck off', inline = False)
        commands.add_field(name = '$father', value = '@\'s the person the bot is based off of', inline = False)
        commands.add_field(name = '$flip', value='flips a coin')
        commands.add_field(name = '$choose', value = 'Chooses an option out of those provided')
        commads.add_field(name = '$rps', value = 'Plays rock paper scissors with me')
        await ctx.send(embed = commands)
    @help.command(name = 'trigger')
    async def triggerCommands(self, ctx):
        trigger = discord.Embed(title = 'Phrases the bot is triggered by')
        trigger.add_field(name = 'Justin', value = 'If any message has justin in it, it will repsond "Yooooooo, I got a friend named justin that\'s cracked at fornite my gaiiiii :weary:"', inline = False)
        trigger.add_field(name = 'can you buy me this', value = 'If any message has can you buy me this in it, it will repsond "Sure."', inline = False)
        trigger.add_field(name = 'Jesus\'s mom ', value = 'If any message has Jesus and his mom in it, it will repsond "Best not be talking about my mom you bitch"', inline = False)
        await ctx.send( embed = trigger)
    @help.command(name = 'response')
    async def userResponses(self, ctx):
        responses = discord.Embed(title = 'How the bot responds to user input')
        responses.add_field(name = 'Mentioning the Bot', value = 'If the bot is mentioned in a message, and enough time has passed, it will tell you to fuck off', inline = False)
        responses.add_field(name = 'Mr.Lettuce', value = 'If Mr.Lettuce sends enough messages for the criteria to be met, he will be called cringe by the bot', inline = False)
        responses.add_field(name = 'Mr.Arsenate', value = 'If Mr.Arsenate sends enough messages for the criteria to be met, he will be told to fuck off by the bot', inline = False)
        responses.add_field(name = 'Mr.Potato', value = 'If Mr.Potato sends enough messages for the criteria to be met, he will be bonked by the bot', inline = False)
        responses.add_field(name = 'Mr.Spaghetti', value = 'If Mr.Spaghetti sends enough messages for the criteria to be met, he will be told he has a small penis at Mr.Jesus\'s request', inline = False)
        responses.add_field(name = 'The FryMakers', value = 'If the criteria is met, and the last user that has the FryMaker role, will be mentioned and asked to make fries for the bot', inline = False)
        await ctx.send(embed = responses)
    @help.command(name = 'emotes')
    async def reactions(self, ctx):
        reactions = discord.Embed(title = 'Emoting')
        reactions.set_thumbnail(url = 'https://i.imgur.com/Ygoheor.png')
        reactions.add_field(name = 'How do I emote?', value = 'Whenever someone reacts to a recent enough message the bot will say "Yo, how do I emote"')
        reactions.add_field(name = 'Why are you booing me', value = 'Whenever someone bonks a message sent by the bot will say "Why are you booing me, I\'m right"')
        await ctx.send(embed = reactions)
    @help.command(name = 'ip')
    async def workInProgress(self, ctx):
        progress = discord.Embed(title = 'Things that are currently a work in progress',inline = False)
        progress.add_field(name = '$bonk', value = "Is meant to join the discord channel and play a bonking sound", inline = False)
        progress.add_field(name = 'Ball itch', value = "If the 'Repost is ball itch' image is sent in the server, the bot will send the image as well", inline = False)
        await ctx.send(embed = progress)
def setup(client):
    client.add_cog(Help(client))
