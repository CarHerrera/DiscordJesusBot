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
counter = 4050
emoteTimer = datetime.utcnow()
booingTimer = datetime.utcnow()
fuckOffTimer = datetime.utcnow()
client = commands.Bot(command_prefix = '$', intents = intents)
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
    users_name = message.author.name
    agreement_words = ['yes', 'y', 'sure', 'mhmm', 'okay', 'yup', 'ofc', 'ok','okey dokey',]
    quit = ['nope', 'no', 'stop', 'quit', 'n', 'exit', 'leave', 'fuck off', 'die']
    options = ['rock', 'paper','scissors']
    await client.process_commands(message)
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
    agreementIndicator = randint(1, 160)
    disgustIndicator = randint(1, 140)
    divider = counter % 100
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
      if divider % agreementIndicator == 0:
          excited = excitement_words[randint(0, len(excitement_words)-1)]
          await message.channel.send('{0}'.format(excited))
      elif divider % disgustIndicator == 0:
          disagreement = disgusted_words[randint(0, len(disgusted_words)-1)]
          await message.channel.send('{0}'.format(disagreement))
      else:
        if message.author.bot is False:
          for roles in message.author.roles:
              if roles.id == fryMakerRoleID:
                  if counter % 12 == 0:
                      await message.channel.send('Yoooooooooo ' + user + ', I hear your fries are a national delight and I am willing to pay top dollar for them. May I put up this formal request for said fries?')
        if message.author.id == carlosDiscordID:
            if counter % 13 == 0:
                await message.channel.send(user + ' Just fuck off already')
        elif message.author.id == jayNatDiscordID:
            if counter % 25 == 0:
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
      if message.content.startswith('$father'):
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
