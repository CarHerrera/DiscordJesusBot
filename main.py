# bot.py
import discord
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
from random import seed
from random import randint
from datetime import datetime
seed(1)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
counter = 1757
emoteTimer = datetime.utcnow()
booingTimer = datetime.utcnow()
fuckOffTimer = datetime.utcnow()
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
def helpMessage():
    attempt = discord.Embed(title = "All the commands currently in this bot", type = 'rich')
    attempt.set_thumbnail(url = 'https://i.imgur.com/GbDdMj2.png')
    attempt.add_field(name = "Commands", value = "$help commands")
    attempt.add_field(name = "Trigger Words", value ="$help trigger words")
    attempt.add_field(name = "User Responses", value = "$help user responses")
    attempt.add_field(name = 'Work in Progress', value = "$help in progress")
    attempt.add_field(name = "Emoting", value = '$help emotes')
    return attempt
def helpCommands():
    commands = discord.Embed(title = "Current comands the bot supports")
    commands.add_field(name = '$help', value = 'use to get more information on commands', inline = False)
    commands.add_field(name = '$hello', value = 'Literally tells you to fuck off', inline = False)
    commands.add_field(name = '$father', value = '@\'s the person the bot is based off of', inline = False)
    return commands
def triggerCommands():
    trigger = discord.Embed(title = 'Phrases the bot is triggered by')
    trigger.add_field(name = 'Justin', value = 'If any message has justin in it, it will repsond "Yooooooo, I got a friend named justin that\'s cracked at fornite my gaiiiii :weary:"', inline = False)
    trigger.add_field(name = 'can you buy me this', value = 'If any message has can you buy me this in it, it will repsond "Sure."', inline = False)
    trigger.add_field(name = 'Jesus\'s mom ', value = 'If any message has Jesus and his mom in it, it will repsond "Best not be talking about my mom you bitch"', inline = False)
    return trigger
def userResponses():
    responses = discord.Embed(title = 'How the bot responds to user input')
    responses.add_field(name = 'Mentioning the Bot', value = 'If the bot is mentioned in a message, and enough time has passed, it will tell you to fuck off', inline = False)
    responses.add_field(name = 'Mr.Lettuce', value = 'If Mr.Lettuce sends enough messages for the criteria to be met, he will be called cringe by the bot', inline = False)
    responses.add_field(name = 'Mr.Arsenate', value = 'If Mr.Arsenate sends enough messages for the criteria to be met, he will be told to fuck off by the bot', inline = False)
    responses.add_field(name = 'Mr.Potato', value = 'If Mr.Potato sends enough messages for the criteria to be met, he will be bonked by the bot', inline = False)
    responses.add_field(name = 'Mr.Spaghetti', value = 'If Mr.Spaghetti sends enough messages for the criteria to be met, he will be told he has a small penis at Mr.Jesus\'s request', inline = False)
    responses.add_field(name = 'The FryMakers', value = 'If the criteria is met, and the last user that has the FryMaker role, will be mentioned and asked to make fries for the bot', inline = False)
    return responses
def reactions():
    reactions = discord.Embed(title = 'Emoting')
    reactions.set_thumbnail(url = 'https://i.imgur.com/Ygoheor.png')
    reactions.add_field(name = 'How do I emote?', value = 'Whenever someone reacts to a recent enough message the bot will say "Yo, how do I emote"')
    reactions.add_field(name = 'Why are you booing me', value = 'Whenever someone bonks a message sent by the bot will say "Why are you booing me, I\'m right"')
    return reactions
def workInProgress():
    progress = discord.Embed(title = 'Things that are currently a work in progress',inline = False)
    progress.add_field(name = '$bonk', value = "Is meant to join the discord channel and play a bonking sound", inline = False)
    progress.add_field(name = 'Ball itch', value = "If the 'Repost is ball itch' image is sent in the server, the bot will send the image as well", inline = False)
    return progress
def momChecker(String):
    if "jesus" and "mom" in String.casefold():
        print('found jesus and or mom in: \n' + String)
        return True
    else:
        return False
async def print_members():
    for guild in client.guilds:
        for member in guild.members:
                print(member.name)
async def print_guilds():
    for guild in client.guilds:
        print(guild.name)
async def print_roles():
    for guild in client.guilds:
        for roles in guild.roles:
            print(roles.name, roles.id)
async def print_emojis():
    for guild in client.guilds:
        for emoji in client.emojis:
            print(emoji.name ,emoji.id)
async def print_channels():
    for guild in client.guilds:
        for channel in guild.channels:
            print(channel.category)
@client.event
async def on_ready():
  global guild
  # game = discord.Game('with my pee pee')
  Stream = discord.Streaming(name = 'The overlords stream :pleading_face:',url = 'https://www.twitch.tv/ulm_nation')
  await client.change_presence(status = discord.Status.online, activity = Stream)
  guild = client.get_guild(751678259657441339)
  print('We have logged in as {0.user}'.format(client))

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
    elif timeChecker(currentTime, messageTime, 45) is True:
        return
    else:
        if payload.emoji.id == 797305732063297536 and timeChecker(datetime.utcnow(),booingTimer, 10) and message.author == client.user:
            await channel.send('Why are you booing me? I\'m right')
            booingTimer = datetime.utcnow()
        elif timeChecker(datetime.utcnow(),emoteTimer,10) is True:
            await channel.send('Yoooooooooo, how do I emote')
            emoteTimer = datetime.utcnow()
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global counter
    user = message.author.mention
    userId = message.author.id
    counter += 1
    carlosDiscordID = 263054069885566977
    fryMakerRoleID = 783852650314596362
    jayNatDiscordID = 412385688332402689
    alexDiscordID = 113820933013110788
    patrickDiscordID = 251770515432275968
    bonkEmoji = '<:Bonk:797305732063297536>'
    jesusMember = await guild.fetch_member(213090776001937409)
    jesusAt = jesusMember.mention
    yoIndicator = randint(65, 99)
    niceIndicator = randint(50, 70)
    # if len(message.mentions) > 0 and message.author.id == jayNatDiscordID:
    #           await message.channel.send(user)
    #           await message.add_reaction(bonkEmoji)
    if len(message.mentions) > 0:
        for mention in message.mentions:
          # print(mention)
          # print(client.user)
          if mention == client.user and timeChecker(datetime.utcnow(),fuckOffTimer, 10) is True:
            await message.channel.send("Fuck off you daft cunt ")
    if counter % yoIndicator == 0:
        await message.channel.send('Yoooooooooooooooo')
    elif counter % niceIndicator == 0:
        await message.channel.send('nice')
    else:
      if message.author.bot is False:
        for roles in message.author.roles:
            if roles.id == fryMakerRoleID:
                if counter % 6 == 0:
                    await message.channel.send('Yoooooooooo ' + user + ', can you make me some fries.')
      if message.author.id == carlosDiscordID:
          counter += 1
          if counter % 13 == 0:
              await message.channel.send(user + ' Just fuck off already')
      elif message.author.id == jayNatDiscordID:
          if counter % 12 == 0:
              await message.channel.send(user + ' cringe')
      elif message.author.id == alexDiscordID:
          if counter % 9 == 0:
              await message.channel.send(bonkEmoji)
      elif message.author.id == patrickDiscordID:
          if counter% 19 == 0:
            await message.channel.send(user + ' Haha, small pee pee')
      if 'can you buy me this' in message.content.casefold():
          await message.channel.send('Sure.')
      elif 'Justin' in message.content.casefold():
          await message.channel.send('Yooooooo, I got a friend named justin that\'s cracked at fornite my gaiiiii :weary:')
      elif momChecker(message.content.casefold()) is True:
          await message.channel.send('Best not be talking about my mom you bitch')
      if '$help commands' in message.content.casefold():
        await message.channel.send(embed = helpCommands())
      elif '$help trigger words' in message.content.casefold():
        await message.channel.send(embed = triggerCommands())
      elif '$help user responses' in message.content.casefold():
         await message.channel.send(embed = userResponses())
      elif '$help in progress' in message.content.casefold():
        await message.channel.send(embed = workInProgress())
      elif '$help emotes' in message.content.casefold():
        await message.channel.send(embed = reactions())
      elif message.content.startswith('$hello'):
          await message.channel.send('Fuck off cunt')
      elif message.content.startswith('$help'):
          # await message.channel.send('Fuck off if you think I\'m gonna help you')
          attempt = helpMessage()
          await message.channel.send(embed = attempt)
      elif message.content.startswith('$father'):
          await message.channel.send(jesusAt + ' father :pleading_face:')
    print('Messages sent: ', counter)
    print('Current random Int: ', yoIndicator)
    print('Current random Int: ', niceIndicator)

keep_alive()
client.run(TOKEN)
