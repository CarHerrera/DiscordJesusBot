from datetime import datetime
import discord
from discord.ext import commands
from main import timeChecker
emoteTimer = datetime.utcnow()
booingTimer = datetime.utcnow()
class Reactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        emoji_file = open('./settings/emojis.txt', 'w').close()
        emoji_file = open('./settings/emojis.txt', 'w')
        for emoji in after:
            emoji_file.write("<:" + emoji.name+ ":" + str(emoji.id) +  ">"+"\n")
        emoji_file.close()
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member == self.client.user:
            return
        global emoteTimer,booingTimer
        guild = self.client.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        lastMessage = await channel.fetch_message(channel.last_message_id)
        print('Reaction found at {0}, authour of message is {1}'.format(channel, message.author))
        print('Most recent message sent by {0}'.format(lastMessage.author))
        currentTime = datetime.utcnow()
        messageTime = message.created_at
        # print('Checks if message is older than 45: {0}'.format(timeChecker(currentTime, messageTime, 45)))
        # print('Booing timer should fire: {0} '.format(timeChecker(currentTime,booingTimer, 10)))
        # print('Emote timer should fire: {0}'.format(timeChecker(currentTime,emoteTimer,10)))
        if lastMessage.author == self.client.user:
            return
        elif timeChecker(currentTime, messageTime, 30) is True:
            return
        else:
            # if payload.emoji.id == 797305732063297536 and timeChecker(datetime.utcnow(),booingTimer, 10) and message.author == self.client.user:
            #     await channel.send('Why are you booing me? I\'m right')
            #     booingTimer = datetime.utcnow()
            if timeChecker(datetime.utcnow(),emoteTimer, 10) is True:
                await channel.send('we boolin')
                emoteTimer = datetime.utcnow()
def setup(client):
    client.add_cog(Reactions(client))
