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
intents = discord.Intents.all()
client = discord.Client(intents = intents)
counter = 2580
emoteTimer = datetime.utcnow()
booingTimer = datetime.utcnow()
fuckOffTimer = datetime.utcnow()
rps_bool = False
excitement_words = ['YOOOOOOOOOOOOOOOOOOO', 'nice', 'sick','poggers', 'owa owa', '+1 good meme', 'nice lmao', 'pog pog pog pog', 'W','mood', 'epic', 'epic sauce']
disgusted_words = ['wtf', 'die', 'stinky', 'just fuck off already','no', 'gay','cringe','nope','why','I really hate you','sus','shut up','pain',]
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
  Stream = discord.Streaming(name = 'The overlords stream',url = 'https://www.twitch.tv/ulm_nation')
  await client.change_presence(status = discord.Status.online, activity = Stream)
  guild = client.get_guild(751678259657441339)
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_update(before, after):
    # print("Status change? {}".format(before.status != after.status))
    # print("Nickname change? {}".format(before.nick != after.nick))
    # print("Activity change? {}".format(before.activity != after.activity))
    # print("Email Verified change? {}".format(before.pending != after.pending))
    # print("Role change? {}".format(before.roles != after.roles))
    if before.bot == True or after.bot == True:
        return
    elif before.status != after.status:
        return
    elif before.nick != after.nick:
        return
    elif before.activity != after.activity:
        return
    elif before.pending != after.pending:
        return
    elif before.roles != after.roles:
        pass
        # carlosDiscordID = 263054069885566977
        # jesusMemberId= 213090776001937409
        # guild = before.guild
        # jesusMember = await guild.fetch_member(jesusMemberId)
        # carlosMember = await guild.fetch_member(carlosDiscordID)
        # hasFishFucker = False
        # if after == jesusMember:
        #   for role in after.roles:
        #     if role.name.casefold() == "fish fucker":
        #       print("Has fish fucker role")
        #       hasFishFucker = True
        #   if hasFishFucker == False:
        #     dmChannel = await carlosMember.create_dm()
        #     await dmChannel.send('Fish fucker role does not exist')
            # fish_fucker_role = await before.guild.create_role(name = "fish fucker")
            # await jesusMember.add_roles(fish_fucker_role)
        # print(guild.roles)
    # if after.id == jesusId:
    #     print( "fish fucker" in after.roles.name.casefold())
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
async def on_guild_role_update(before, after):
  oldRole = before
  newRole = after
  print(oldRole.name)
  print(newRole.name)
  # if oldRole.name.casefold() == 'fish fucker':
  #   await after.edit(name = "fish fucker", colour = discord.Colour.default())
@client.event
async def on_message(message):
    global counter, rps_bool
    counter += 1
    if message.author == client.user:
      return
    elif message.author.bot == True:
      return 
    elif message.channel.name == 'politics':
      return
    user = message.author.mention
    userId = message.author.id
    agreement_words = ['yes', 'y', 'sure', 'mhmm', 'okay', 'yup', 'ofc', 'ok','okey dokey',]
    quit = ['nope', 'no', 'stop', 'quit', 'n', 'exit', 'leave', 'fuck off', 'die']
    options = ['rock', 'paper','scissors']
    try:
      carlosDiscordID = 263054069885566977
      fryMakerRoleID = 783852650314596362
      jayNatDiscordID = 412385688332402689
      alexDiscordID = 113820933013110788
      patrickDiscordID = 251770515432275968
      bonkEmoji = '<:Bonk:797305732063297536>'
      jesusMember = await message.guild.fetch_member(213090776001937409)
      jesusAt = jesusMember.mention
    except:
      print('One of these people are not in the server')
    agreementIndicator = randint(60, 150)
    disgustIndicator = randint(65, 140 )
    # if len(message.mentions) > 0 and message.author.id == jayNatDiscordID:
    #           await message.channel.send(user)
    #           await message.add_reaction(bonkEmoji)
    if rps_bool == False:
      if len(message.mentions) > 0:
          for mention in message.mentions:
            # print(mention)
            # print(client.user)
            if mention == client.user and timeChecker(datetime.utcnow(),fuckOffTimer, 10) is True:
              await message.channel.send("Fuck off you daft cunt ")
      if counter % agreementIndicator == 0:
          excited = excitement_words[randint(0, len(excitement_words))]
          await message.channel.send('{0}'.format(excited))
      elif counter % disgustIndicator == 0:
          disagreement = disgusted_words[randint(0, len(disgusted_words))]
          await message.channel.send('{0}'.format(disagreement))
      else:
        if message.author.bot is False:
          for roles in message.author.roles:
              if roles.id == fryMakerRoleID:
                  if counter % 6 == 0:
                      await message.channel.send('Yoooooooooo ' + user + ', can you make me some fries.')
        if message.author.id == carlosDiscordID:
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
      elif message.content.startswith('$rps'):
          rps_bool = True
          repeat_bool = True
          await message.channel.send('Hey {0}, wanna play rock paper scissors?'.format(user))
          channel = message.channel
          author = message.author
          def check(m):
            return m.content.casefold() in agreement_words and m.channel == channel and m.author == author
          try:      
            msg = await client.wait_for('message', check=check, timeout = 30)
          except:
            await channel.send('You took too long cunt')
            return
          while repeat_bool:
            await channel.send('Alright, on 3 {0}'.format(user))
            currentTimeInSeconds = datetime.utcnow().second
            localCounter = 1
            while datetime.utcnow().second - currentTimeInSeconds <= 3:
              if datetime.utcnow().second - currentTimeInSeconds < 0:
                # timeElapsed = (datetime.utcnow().second + 60) - currentTimeInSeconds
                # print("2: Seconds gone by {0}".format((datetime.utcnow().second + 60)- currentTimeInSeconds))
                if ((datetime.utcnow().second + 60) - currentTimeInSeconds) == localCounter and localCounter != 4:
                  localCounter+= 1
                  await channel.send("{0}".format((datetime.utcnow().second + 60) - currentTimeInSeconds))
              else:
                if datetime.utcnow().second - currentTimeInSeconds == localCounter and localCounter != 4:
                  await channel.send("{0}".format(datetime.utcnow().second - currentTimeInSeconds))
                  localCounter+= 1
                # print("1: Seconds gone by {0}".format(datetime.utcnow().second - currentTimeInSeconds))
            def check(m):
              return m.content.casefold() in options and m.channel == channel and m.author == author
            try:
              msg = await client.wait_for('message', check = check)
            except:
              await channel.send('You took too long idiot')
              break
            await channel.send('rock')
            if msg.content == 'rock':
              await channel.send('Nice, again?')
              await channel.send('Say yes to go again no to fuck off')
            elif msg.content == 'scissors':
              await channel.send('Get fucked. Wanna play again?')
              await channel.send('Say yes to go again no to fuck off')
            else: 
              await channel.send('Alright, you got it, you got it. Again?')
              await channel.send('Say yes to go again no to fuck off')
            def check(m):
              return m.content.casefold() in quit  or m.content.casefold() in agreement_words and m.channel == channel and m.author == author
            try:
              msg = await client.wait_for('message', check = check, timeout = 45)
              quitMessage = msg.content.casefold()
              if quitMessage in quit:
                repeat_bool = False
            except:
              await message.channel.send('You took too long to respond cunt')
              return
          await message.channel.send('Alright fuck off now.')
          rps_bool = False
    print('Messages sent: ', counter)
    print('Current random Int: ', agreementIndicator)
    print('Current random Int: ', disgustIndicator)

keep_alive()
client.run(TOKEN)
