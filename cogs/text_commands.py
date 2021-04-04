import discord
from discord.ext import commands
from datetime import datetime
from random import seed
from random import randint
from main import timeChecker
from main import momChecker
import os
import requests
import requests.auth
import asyncpraw
import json
import betamax
import pprint
import uwuify
import re
settings = open('./settings/counter.txt')
data = settings.read().split("=")
counter = int(data[1])
settings.close()
file = open("./private/redditdeets.txt")
data = file.read()
file.close()
words = re.split('[=\n]', data)
username = words[1]
password = words[3]
client_id = words[5]
client_secret = words[7]
client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
post_data = {"grant_type": "password", "username" : username, "password" : password}
headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
response = response.json()
headers = {"Authorization": "bearer " + response["access_token"], "User-Agent": "ChangeMeClient/0.1 by Unseenninja1"}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
reddit = asyncpraw.Reddit(client_id = client_id, client_secret = client_secret,
password = password, user_agent = "testscript by u/Unseenninja1", username = username, check_for_updates = 'True')
bonk = '<:Bonk:797305732063297536>'
amogus ='<:amogus:810676422981058620>'
drip ='<:DripMoment:800232915028017202>'
PepeThink = '<:PepeThink:762416066570747904>'
HolyPepe = '<:HolyPepe:797304202573119529>'
excitement_words = ['YOOOOOOOOOOOOOOOOOOO', 'nice', 'sick','poggers', 'owa owa', '+1 good meme', 'nice lmao', 'pog pog pog pog', 'W','mood', 'epic', 'epic sauce', amogus, drip, PepeThink]
disgusted_words = ['wtf', 'die', 'stinky', 'just fuck off already','no', 'gay','cringe','nope','why','I really hate you','sus','shut up','pain',bonk, HolyPepe, bonk*6]
buy_me = ['can you buy me this', 'buy me this', 'purchase this for me', 'will you buy me this']
cmd_in_process = False
fuckOffTimer = datetime.utcnow()
seedgen = datetime.utcnow().year + datetime.utcnow().month + datetime.utcnow().day + datetime.utcnow().second + datetime.utcnow().minute + datetime.utcnow().microsecond
seed(seedgen)
memes= []
usedMemes =[]
memeTimer = datetime.utcnow()
class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_message(self, message):
        global counter, cmd_in_process
        counter +=1
        write_file = open('./settings/counter.txt', 'w')
        write_file.write('counter=' + str(counter))
        write_file.close()
        if message.author == self.client.user:
            return
        elif message.author.bot == True:
            return
        try:
            carlosDiscordID = 263054069885566977
            fryMakerRoleID = 783852650314596362
            jayNatDiscordID = 412385688332402689
            alexDiscordID = 113820933013110788
            patrickDiscordID = 251770515432275968
            bonkEmoji = '<:Bonk:797305732063297536>'
            jesusMember = await message.guild.fetch_member(213090776001937409)
            jesusAt = jesusMember.mention
            fry_role = message.guild.get_role(fryMakerRoleID)
        except:
            print('One of these people are not in the server')
            # print(timeChecker(datetime.utcnow(), fuckOffTimer, 10))
        agreementIndicator = randint(23, 69)
        disgustIndicator = randint(23, 69)
        divider = counter % 100
        self_mention = self.client.user.mention
        user = message.author.mention
        if cmd_in_process == False:
            if len(message.mentions)>0:
                for mentions in message.mentions:
                    if mentions == self.client.user and timeChecker(datetime.utcnow(), fuckOffTimer, 10):
                        if 'i agree with' in message.content.casefold():
                            await message.channel.send('Thanks bb')
                        else:
                            await message.channel.send('wtf do you want')
            if divider % agreementIndicator == 0:
                excited = excitement_words[randint(0, len(excitement_words)-1)]
                await message.channel.send('{0}'.format(excited))
            elif divider % disgustIndicator == 0:
                disagreement = disgusted_words[randint(0, len(disgusted_words)-1)]
                await message.channel.send('{0}'.format(disagreement))
            else:
                if message.author.id == alexDiscordID:
                    pass
                    # if counter % 23 == 0:
                    #     await message.channel.send(bonkEmoji)
                # elif any(ele in message.content.casefold() for ele in buy_me):
                #     await message.channel.send('Sure.')
                elif momChecker(message.content.casefold()) is True:
                    print('{0} is where I found mom'.format(message.content))
                    await message.channel.send('Just die already')
                elif fry_role in message.author.roles:
                    if counter % 12 == 0:
                        await message.channel.send('Yoooooooooo ' + user + ', I hear your fries are a national delight and I am willing to pay top dollar for them. May I put up this formal request for said fries?')
        print('Messages sent: ', counter)
        print('Current random Int: ', agreementIndicator)
        print('Current random Int: ', disgustIndicator)
    # @commands.Cog.listener('on_message')
    # async def test_message(self, message):
    #     if message.author.id == 263054069885566977:
    #         await message.channel.send('the second listener')
    @commands.command()
    async def test(self,ctx):
        # print(ctx)
        """Test command that only says 'Hello World!'"""
        global cmd_in_process
        cmd_in_process = True
        await ctx.send('Hello world!')
    @commands.command()
    async def choose(self,ctx, *args):
        """Chooses an option out of those provided"""
        global cmd_in_process
        cmd_in_process = True
        rand_num = randint(0, len(args) -1)
        await ctx.send('Hmmmmmmm, I choose {}'.format(args[rand_num]))
        cmd_in_process = False
    @commands.command()
    async def flip(self, ctx):
        """This command flips a coin"""
        global cmd_in_process
        cmd_in_process = True
        await ctx.send('hold on let me get my lucky nickel')
        currentTimeInSeconds = datetime.utcnow().second
        timer = datetime.utcnow().second
        maxOdds = 10000
        findcoin = randint(0, maxOdds)
        difference = timer - currentTimeInSeconds
        while timer - currentTimeInSeconds < 3:
            if timer - currentTimeInSeconds < 0:
                timer = datetime.utcnow().second + 60
            else:
                timer = datetime.utcnow().second
        else:
            await ctx.send('alright I got it')
            if findcoin < 100:
                await ctx.send('wtf the coin landed on its side, thats like a {0}% chance'.format((100/maxOdds) * 100))
                return
            elif findcoin < 500:
                await ctx.send('wtf I can\'t find the damn thing. this is some bullshit')
                return
            elif findcoin < 5250:
                await ctx.send('the lucky nickel said heads')
            else:
                await ctx.send('the lucky nickel said tails')
            cmd_in_process = False
    @commands.command()
    async def father(self, ctx):
        global cmd_in_process
        cmd_in_process = True
        jesusMember = await ctx.guild.fetch_member(213090776001937409)
        jesusAt = jesusMember.mention
        await ctx.send('{} father :pleading_face:'.format(jesusAt))
        cmd_in_process = False
    @commands.command()
    async def rps(self,ctx):
        global cmd_in_process
        cmd_in_process = True
        agreement_words = ['yes', 'y', 'sure', 'mhmm', 'okay', 'yup', 'ofc', 'ok','okey dokey',]
        quit = ['nope', 'no', 'stop', 'quit', 'n', 'exit', 'leave', 'fuck off', 'die']
        options = ['rock', 'paper','scissors']
        await ctx.send('Hey {0.author.mention} wanna play rock paper scissors?'.format(ctx))
        bot = ctx.bot
        channel = ctx.message.channel
        author = ctx.message.author
        mention = ctx.message.author.mention
        repeat_bool = True
        def check(m):
            return m.content.casefold() in agreement_words and m.channel == channel and m.author == author
        # ctx.bot.add_listener(on_message)
        try:
            msg = await bot.wait_for('message', check=check, timeout = 30)
        except:
            await ctx.send('You took too long')
            return
        while repeat_bool:
            await channel.send('Alright {} on 3'.format(mention))
            currentTimeInSeconds = datetime.utcnow().second
            timer = datetime.utcnow().second
            localCounter = 1
            while timer - currentTimeInSeconds <= 3:
                if timer - currentTimeInSeconds < 0:
                    timer = datetime.utcnow().second + 60
                else:
                    timer = datetime.utcnow().second
                if timer - currentTimeInSeconds == localCounter and localCounter != 4:
                    await channel.send('{0}'.format(localCounter))
                    localCounter +=1
            def check(m):
                return m.content.casefold() in options and m.channel == channel and m.author == author
            try:
                msg = await bot.wait_for('message', check = check, timeout = 30)
            except:
                await channel.send('You took too long')
                return
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
                msg = await bot.wait_for('message', check = check, timeout = 45)
                if msg.content.casefold() in quit:
                    repeat_bool = False
            except:
                await channel.send('You took too long to reply')
                return
        await channel.send('Alright you can go away now')
        cmd_in_process = False

    @commands.command()
    async def meme(self,ctx):
        global memes, memeTime, reddit, cmd_in_process
        cmd_in_process = True
        subreddit = await reddit.subreddit('dankmemes+okbuddyretard+HolUp+SuddenlyGay')
        if len(memes) < 20 or timeChecker(datetime.utcnow(), memeTime, 20):
            async for submission in subreddit.hot():
                memes.append(submission.url)
        randnum = randint(0, len(memes)-1)
        await ctx.send(memes[randnum])
        memes.pop(randnum)
        memeTime = datetime.utcnow()
        cmd_in_process = False
    @commands.command()
    async def uwuify(self, ctx):
        global cmd_in_process
        cmd_in_process = True
        message = ctx.message.content
        messageSend = message[8:]
        await ctx.send(uwuify.uwu(messageSend))
        cmd_in_process = False
def setup(client):
    client.add_cog(Commands(client))
