# bot.py
#Author is Carlos Herrera
# Todo good noodle star?
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
from random import seed
from random import randint
from datetime import datetime
import json
seedgen = datetime.utcnow().year + datetime.utcnow().month + datetime.utcnow().day + datetime.utcnow().second + datetime.utcnow().minute + datetime.utcnow().microsecond
seed(seedgen)
load_dotenv(dotenv_path = './private/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
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
    if "hunter" in String.casefold() and "dad" in String.casefold():
        print('found hunter and or dad in: \n' + String)
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
@client.command()
async def reload(ctx, extension):
    client.unload_extension('cogs.{}'.format(extension))
    client.load_extension('cogs.{}'.format(extension))
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
    # emoji_file = open('./settings/emojis.txt', 'w')
    # for guild in client.guilds:
    #     for emoji in guild.emojis:
    #         emoji_file.write("<:" + emoji.name+ ":" + str(emoji.id) +  ">"+"\n")
    # emoji_file.close()
    # members_dict = {"Guilds": []}
    # count = 0
    # async for guild in client.fetch_guilds():
    #     members_dict["Guilds"].append({guild.name:guild.id, "Members": []})
    #     async for members in guild.fetch_members():
    #         members_dict["Guilds"][count]["Members"].append({members.name:members.id, "Stars": 0})
    #     count +=1
    # file = open("./settings/good_noodle.txt", "w")
    # file.write(json.dumps(members_dict, indent = 4))
    # file.close()
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
            # print('Before activity is {0} and after is {1}'.format(before.activity, after.activity))
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
async def on_guild_role_update(before, after):
  oldRole = before
  newRole = after
  print(oldRole.name)
  print(newRole.name)
  # if oldRole.name.casefold() == 'fish fucker':
  #   await after.edit(name = "fish fucker", colour = discord.Colour.default())


keep_alive()
client.run(TOKEN)
