# bot.py
#Author is Carlos Herrera
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
from random import seed
from random import randint
from datetime import datetime
seedgen = datetime.utcnow().day + datetime.utcnow().second + datetime.utcnow().minute + datetime.utcnow().microsecond
print(seedgen)
seed(seedgen)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
emoteTimer = datetime.utcnow()
booingTimer = datetime.utcnow()
client = commands.Bot(command_prefix = '$', intents = intents)
#Checks whether or not the given time is larger than the one the bot currently has, also checks if the difference is large enough to return a True statement
def timeChecker(currentTime, originalTime, difference):
    #Checks if the day is the same or not
    difDay = currentTime.day > originalTime.day
    #Checks if the month is different
    difMonth = currentTime.month > originalTime.month
    #Checks if the year year is larger
    difYear = currentTime.year > originalTime.year
    #Checks the difference in hours
    difHour = currentTime.hour > originalTime.hour
    if difYear is False:
        if difMonth is False:
            if difDay is False:
                if difHour is False:
                    minuteDifference = currentTime.minute - originalTime.minute
                    if minuteDifference >= difference:
                        return True
                    else:
                        return False
                else:
                    hourDifference = currentTime.hour - originalTime.hour
                    minuteDifference = ((hourDifference * 60) +currentTime.minute) - originalTime.minute
                    if minuteDifference >= difference:
                        return True
                    else:
                        return False
                    return False
            else:
                return True
        else:
            return True
    else:
        return True

def momChecker(String):
    if "jesus" in String.casefold() and "mom" in String.casefold():
        print('found jesus and or mom in: \n' + String)
        print('Jesus in String {0}'.format('jesus' in String.casefold()))
        print('Mom in String {0}'.format('mom' in String.casefold()))
        return True
    else:
        return False

client.remove_command('help')
@client.command()
async def load(ctx, extension):
    client.load_extension('cogs.{}'.format(extension))
@client.command()
async def unload(ctx, extension):
    client.unload_extension('cogs.{}'.format(extension))
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension('cogs.{}'.format(filename[:-3]))

@client.event
async def on_ready():
    global guild
    game = discord.Game('with my pee pee')
    Stream = discord.Streaming(name = 'The overloads stream :pleading_face:',url = 'https://www.twitch.tv/ulm_nation')
    await client.change_presence(status = discord.Status.online, activity = Stream)
    print('We have logged in as {0.user}'.format(client))
@client.event
async def on_disconnect():
    print('No longer connected to discord')
@client.event
async def on_member_update(before, after):
    # print("Status change? {}".format(before.status != after.status))
    # print("Nickname change? {}".format(before.nick != after.nick))
    # print("Activity change? {}".format(before.activity != after.activity))
    # print("Email Verified change? {}".format(before.pending != after.pending))
    # print("Role change? {}".format(before.roles != after.roles))
    global guild
    if before.bot == True or after.bot == True:
        return
    elif before.status != after.status:
        return
    elif before.nick != after.nick:
        return
    elif before.activity != after.activity:
        jesusMember = await before.guild.fetch_member(213090776001937409)
        if before == jesusMember:
            if type(after) == discord.Streaming:
                print('streaming?')
            print('Before activity is {0} and after is {1}'.format(before.activity, after.activity))
        # if(type(after.activity == discord.activity.Spotify)):
        #   general = guild.get_channel(751678259657441342)
          # await general.send('Listening to {0} {1}? cringe lmao'.format(after.activity.title, after.mention))
          # pass
        return
    elif before.pending != after.pending:
        return
    elif before.roles != after.roles:
        return
    # print(after.activity)
# payload has channel_id, emoji, event_type, guild_id, member, message_id, user_id
# as attributes
@client.event
async def on_raw_reaction_add(payload):
    if payload.member == client.user:
        return
    global emoteTimer,booingTimer
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
    if lastMessage.author == client.user:
        return
    elif timeChecker(currentTime, messageTime, 20) is True:
        return
    else:
        if payload.emoji.id == 797305732063297536 and timeChecker(datetime.utcnow(),booingTimer, 10) and message.author == client.user:
            await channel.send('Why are you booing me? I\'m right')
            booingTimer = datetime.utcnow()
        elif timeChecker(datetime.utcnow(),emoteTimer, 40) is True:
            await channel.send('Yoooooooooo, how do I emote')
            emoteTimer = datetime.utcnow()
@client.event
async def on_guild_role_update(before, after):
  oldRole = before
  newRole = after
  print(oldRole.name)
  print(newRole.name)
  # if oldRole.name.casefold() == 'fish fucker':
  #   await after.edit(name = "fish fucker", colour = discord.Colour.default())


keep_alive()
client.run(TOKEN)
