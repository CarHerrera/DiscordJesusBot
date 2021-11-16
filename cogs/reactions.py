from datetime import datetime
import discord
from discord.ext import commands
from main import timeChecker
from random import randint
import json
emoteTimer = None
# booingTimer = datetime.utcnow()
class Reactions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.lastMoment = datetime.now()
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        emoji_file = open('./settings/emojis.txt', 'w').close()
        emoji_file = open('./settings/emojis.txt', 'w')
        for emoji in after:
            emoji_file.write("<:" + emoji.name+ ":" + str(emoji.id) +  ">"+"\n")
        emoji_file.close()
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     if payload.member == self.client.user:
    #         return
    #     global emoteTimer,booingTimer
    #     guild = self.client.get_guild(payload.guild_id)
    #     channel = guild.get_channel(payload.channel_id)
    #     message = await channel.fetch_message(payload.message_id)
    #     lastMessage = await channel.fetch_message(channel.last_message_id)
    #     print('Reaction found at {0}, authour of message is {1}'.format(channel, message.author))
    #     print('Most recent message sent by {0}'.format(lastMessage.author))
    #     currentTime = datetime.utcnow()
    #     messageTime = message.created_at
    #     emote_list = ['Yo, how do I emote','this shit got me boolin',]
    #     # print('Checks if message is older than 45: {0}'.format(timeChecker(currentTime, messageTime, 45)))
    #     # print('Booing timer should fire: {0} '.format(timeChecker(currentTime,booingTimer, 10)))
    #     # print('Emote timer should fire: {0}'.format(timeChecker(currentTime,emoteTimer,10)))
    #     if lastMessage.author == self.client.user:
    #         return
    #     elif timeChecker(currentTime, messageTime, 30) is True:
    #         return
    #     else:
    #         # if payload.emoji.id == 797305732063297536 and timeChecker(datetime.utcnow(),booingTimer, 10) and message.author == self.client.user:
    #         #     await channel.send('Why are you booing me? I\'m right')
    #         #     booingTimer = datetime.utcnow()
    #         if timeChecker(datetime.utcnow(),emoteTimer, 10) is True:
    #             await channel.send('')
    #             emoteTimer = datetime.utcnow()
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        global emoteTimer
        if reaction.message.author == self.client.user:
            return
        elif reaction.me:
            return
        channel = reaction.message.channel
        lastMessage = await channel.fetch_message(channel.last_message_id)
        e = 'e' * randint(3,10)
        m = 'm' * randint(2,12)
        o = 'o' * randint(4,18)
        t = 't' * randint(1,3)
        emote = e+m+o+t+e
        currentTime = datetime.utcnow()
        messageTime = lastMessage.created_at
        guild = reaction.message.guild
        dif = (currentTime - messageTime).total_seconds()/ 60
        emote_list = ['Y'+'o' * randint(8,50) + ' how do I emote','this shit got me boolin',reaction.emoji,'this emote shit be bussin', 'Your emotes make me so proud',emote, 'lessssgetit', "meow", "bark"*randint(1,9), "FINALLY A GOOD EMOTE", ""]
        if reaction.emoji.id == 815051855859023872:
            time_between_emotes = datetime.now() - self.lastMoment
            diff =":".join(str(time_between_emotes).split(":")[:2])
            seconds = int(float(str(time_between_emotes).split(":")[2]))
            file = open('./private/server_settings.txt', "r")
            settings = json.loads(file.read())
            file.close()
            pref_channel = settings["Guilds"][guild.name]["Settings"]["Pref Channel"]
            spam = discord.utils.get(guild.text_channels, name= pref_channel)
            self.lastMoment = datetime.now()
            await spam.send(f'It\'s been {diff}:{seconds} since last {reaction.emoji}')
        if lastMessage.author == self.client.user:
            return
        elif dif > 20:
            return
        else:
            # if payload.emoji.id == 797305732063297536 and timeChecker(datetime.utcnow(),booingTimer, 10) and message.author == self.client.user:
            #     await channel.send('Why are you booing me? I\'m right')
            #     booingTimer = datetime.utcnow()
            if emoteTimer is None:
                await channel.send(emote_list[randint(0,len(emote_list)-1)])
                emoteTimer = datetime.utcnow()
            else:
                diff = emoteTimer - datetime.utcnow()
                if diff.seconds >= 60:
                    await channel.send(emote_list[randint(0,len(emote_list)-1)])
            # if timeChecker(datetime.utcnow(),emoteTimer, 10) is True:
            #     await channel.send(emote_list[randint(0,len(emote_list)-1)])
    def check_guild(self, ctx):
        return ctx.guild.id == 751678259657441339
    @commands.command()
    async def last_hunter_moment(self, ctx):
        if(self.check_guild(ctx)):
            time_between_emotes = datetime.now() - self.lastMoment
            diff =":".join(str(time_between_emotes).split(":")[:2])
            seconds = int(float(str(time_between_emotes).split(":")[2]))
            hunterMoment = await ctx.guild.fetch_emoji(815051855859023872)
            await ctx.send(f"it's been {diff}:{seconds} since last hunterMoment {hunterMoment}")
def setup(client):
    client.add_cog(Reactions(client))
