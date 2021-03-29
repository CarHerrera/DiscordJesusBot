import discord
import json
from random import randint
from discord.ext import commands, tasks
from datetime import datetime
from main import timeChecker
import pandas, csv, os
from dotenv import load_dotenv
import db_uploader
file = open("./private/swearWords.txt")
bad_words = file.read().split()
file.close()
file = open("./private/positive-words.txt")
good_words = file.read().split()
file.close()
timer = {}
last_reset = datetime.now()
stars = None
rules_followed = {"Guilds":{}}
load_dotenv(dotenv_path = "./private/.env")
# cities = pandas.DataFrame(columns=['Guild', 'Member', 'Reason', 'Added', 'Stars', 'Day', 'MSGID', 'Channel'])
# cities.to_csv('./private/good_noodle_data.csv', index = False)
try:
    stars_data = open("./private/good_noodle_data.csv", "a")
except FileNotFoundError:
    cities = pandas.DataFrame(columns=['Guild', 'Member', 'Reason', 'Added', 'Stars', 'Day', 'MSGID', 'Channel'])
    cities.to_csv('./private/good_noodle_data.csv', index = False)
    stars_data = open("./private/good_noodle_data.csv", "a")
class Stars(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.reset_weekly_stars.start()
    @tasks.loop(minutes = 1)
    # This loops every 24 hours and resets the servers weekly stars and send a message with who had the highest and lowest stars
    async def reset_weekly_stars(self):
        global last_reset, stars, stars_data
        day = datetime.now().strftime("%A")
        time = datetime.now()
        count = 0
        for guild in self.client.guilds:
            sent = stars["Guilds"][guild.name]["Sent"]
            if (day == "Monday" and time.hour == 12) and sent is False:
                number_of_stars = []
                members_list = []
                for member in guild.members:
                    if member.bot is True:
                        continue
                    # Checks if the member has weekly stars then resets it
                    if member.name not in stars["Guilds"][guild.name]["Members"]:
                       stars["Guilds"][guild.name]["Members"][member.name] = {"Stars":0}
                       print(member.name) 
                    if "Weekly Stars" in stars["Guilds"][guild.name]["Members"][member.name]:
                        number_of_stars.append(stars["Guilds"][guild.name]["Members"][member.name]["Weekly Stars"])
                        members_list.append(member.name)
                        stars["Guilds"][guild.name]["Members"][member.name]["Weekly Stars"] = 0
                if len(number_of_stars) > 0:
                    channel = discord.utils.get(guild.text_channels, name='bot-spam')
                    highest_stars = max(number_of_stars)
                    hs_index = number_of_stars.index(highest_stars)
                    user = members_list[hs_index]
                    member = discord.utils.find(lambda m: m.name == user, guild.members)
                    lowest_stars = min(number_of_stars)
                    user_low = members_list[number_of_stars.index(lowest_stars)]
                    lowest_member = discord.utils.find(lambda m: m.name == user_low, guild.members)
                    print(f'Sent out {guild.name} star information')
                    await channel.send(f"{member.mention} got this weeks highest stars at {highest_stars} and unsurprisngly {lowest_member.mention} got the lowest amount of stars at {lowest_stars}")
                    stars["Guilds"][guild.name]["Sent"] = True
                    count+=1
                    if stars["Guilds"][guild.name]["Sent"] is True and count == 1:
                        try:
                            file_trasnfer = db_uploader.TransferData(os.getenv('ACCESS_TOKEN'))
                            file_from = "./private/good_noodle_data.csv"
                            today = datetime.now().strftime("%m-%d-%y")
                            file_to = f"/code/Python/Discord/StarsData/{today} stars.csv"
                            file_trasnfer.upload_file(file_from, file_to)
                            if stars_data.closed:
                                stars_data = open("./private/good_noodle_data.csv", "w")
                                stars_data.write("Guild,Member,Reason,Added,Stars,Day,MSGID,Channel")
                                stars_data.close()
                            else:
                                stars_data.close()
                                stars_data = open("./private/good_noodle_data.csv", "w")
                                stars_data.write("Guild,Member,Reason,Added,Stars,Day,MSGID,Channel")
                                stars_data.close()
                        except Exception:
                            print(str(Exception))
            elif day != "Monday":
                stars["Guilds"][guild.name]["Sent"] = False
        file = open('./settings/stars.txt', "w")
        file.write(json.dumps(stars, indent = 4))
        file.close()

    @reset_weekly_stars.before_loop
    async def before_check(self):
        await self.client.wait_until_ready()
        global stars, rules_followed
        async for guild in self.client.fetch_guilds():
            rules_followed["Guilds"][guild.name] = {"Members":{}}
        try:
            file = open('./settings/stars.txt', "r")
            stars = json.loads(file.read())
            file.close()
            # async for guild in self.client.fetch_guilds():
                # rules_followed["Guilds"][guild.name] = {"Members":{}}
                # async for member in guild.fetch_members():
                    # if member.name not in stars["Guilds"][guild.name]["Members"] and member.bot is False:
                        # stars["Guilds"][guild.name]["Members"][member.name] = {"Stars":0}
                        # # print(member.name, sep = " ")
            # file = open('./settings/stars.txt', "w")
            # file.write(json.dumps(stars, indent = 4))
            # file.close()
            print("Opened existing file")
        except FileNotFoundError:
            stars = {"Guilds":{}}
            async for guild in self.client.fetch_guilds():
                if guild.name not in stars["Guilds"].keys():
                    stars["Guilds"][guild.name] = {"Members":{}}
                    stars["Guilds"][guild.name]["Sent"] = False
                async for member in guild.fetch_members():
                    if member.name not in stars["Guilds"][guild.name]["Members"].keys() and member.bot is False:
                        stars["Guilds"][guild.name]["Members"][member.name] = {"Stars": 0}
            print("Created a stars file")
            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(stars, indent = 4))
            file.close()
    def remove_stars(self, user, channel, rand_num, reason = ""):
        """This function removes stars"""
        if user.bot is True:
            return
        global stars
        member = user
        name = member.name
        guild = member.guild
        print("Weekly Stars" in stars["Guilds"][guild.name]["Members"][name].keys())
        if name in stars["Guilds"][guild.name]["Members"]:
            if "Weekly Stars" in stars["Guilds"][guild.name]["Members"][name].keys():
                stars["Guilds"][guild.name]["Members"][name]["Weekly Stars"] -= rand_num
                stars["Guilds"][guild.name]["Members"][name]["Stars"] -= rand_num
            else:
                stars["Guilds"][guild.name]["Members"][name]["Weekly Stars"] = -rand_num
                stars["Guilds"][guild.name]["Members"][name]["Stars"] -= rand_num
        file = open('./settings/stars.txt', "w+")
        file.write(json.dumps(stars, indent = 4))
        file.close()
        return f"{name} loses {rand_num} good noodle star(s){reason}"
    def add_stars(self, user, channel, rand_num, reason = ""):
        """This function adds stars"""
        if user.bot is True:
            return
        global stars
        member = user
        name = member.name
        guild = member.guild
        print("Weekly Stars" in stars["Guilds"][guild.name]["Members"][name].keys())
        if name in stars["Guilds"][guild.name]["Members"]:
            if "Weekly Stars" in stars["Guilds"][guild.name]["Members"][name].keys():
                stars["Guilds"][guild.name]["Members"][name]["Weekly Stars"] += rand_num
                stars["Guilds"][guild.name]["Members"][name]["Stars"] += rand_num
            else:
                stars["Guilds"][guild.name]["Members"][name]["Weekly Stars"] = rand_num
                stars["Guilds"][guild.name]["Members"][name]["Stars"] += rand_num
        file = open('./settings/stars.txt', "w+")
        file.write(json.dumps(stars, indent = 4))
        file.close()
        return f"{name} gains {rand_num} good noodle star(s){reason}"
    def data_gatherer(self, msg, reason, added, stars):
        global stars_data
        if stars_data.closed:
            stars_data = open("./private/good_noodle_data.csv", "a")
        if type(msg) == discord.Message:
            guild = msg.guild.name
            name = msg.author.name
            now = datetime.now()
            time = now.strftime("%m/%d/%y %H:%M")
            string = guild + "," + name + "," + reason + "," + str(added) + "," + str(stars) + "," + time + "," + str(msg.id) + "," + msg.channel.name
            stars_data.write(string + "\n")
            stars_data.close()
        elif type(msg) == discord.Member:
            member = msg
            guild = member.guild.name
            name = member.name
            now = datetime.now()
            time = now.strftime("%m/%d/%y %H:%M")
            string = guild + "," + name + "," + reason + "," + str(added) + "," + str(stars) + "," + time + "," + "None" + "," + "None"
            stars_data.write(string + "\n")
            stars_data.close()
    @commands.Cog.listener('on_message')
    async def star_message(self, msg):
        global rules_followed
        if msg.author == self.client.user:
            return
        elif msg.author.bot == True:
            return
        rand_num = randint(1, 30)
        guild = msg.guild
        count = 0
        spam = discord.utils.get(guild.text_channels, name='bot-spam')
        if msg.guild.name in rules_followed["Guilds"]:
            # Checks if the user that sent a message is in the dictionary, if not will add it to it
            if msg.author.name not in rules_followed["Guilds"][guild.name]["Members"].keys():
                rules_followed["Guilds"][guild.name]["Members"][msg.author.name]= 0
        try:
            difference = timeChecker(datetime.now(), timer[msg.author.name], 5)
        except:
            difference = None
        rules_followed_counter = rules_followed["Guilds"][guild.name]["Members"][msg.author.name]
        async for message in msg.channel.history(limit = 10):
            if len(message.attachments) > 0 or len(message.embeds) > 0:
                pass
            elif message.author == msg.author:
                count+= 1
        if any(word in msg.content.casefold() for word in bad_words):
            if msg.author.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[msg.author.name], 10)
                if dif is True:
                    await spam.send(self.remove_stars(msg.author, msg.channel, randint(1, 30)))
                    rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
                    timer.update({msg.author.name:datetime.now()})
                    self.data_gatherer(msg, "Bad words", False, -rand_num)
            else:
                await spam.send(self.remove_stars(msg.author, msg.channel, randint(1, 30)))
                rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
                timer.update({msg.author.name:datetime.now()})
                self.data_gatherer(msg, "Bad words", False, -rand_num)
            return
        elif count > 8:
            await spam.send(self.remove_stars(msg.author, msg.channel, rand_num, reason = " for being a dick head"))
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
            self.data_gatherer(msg, "Spammed Messages", False, -rand_num)
        elif len(msg.content) > 300:
            if len(msg.embeds) > 0 or len(msg.attachments) > 0:
                return
            else:
                await spam.send(self.remove_stars(msg.author, msg.channel, rand_num, reason = " for sending way to long of a message"))
                rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
                self.data_gatherer(msg, "Long message", False, -rand_num)
        elif msg.content.isupper():
            await spam.send(self.remove_stars(msg.author, msg.channel, rand_num, reason = " for being aggressive"))
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
            self.data_gatherer(msg, "Message in caps", False, -rand_num)
            return
        elif "bot" in msg.content.casefold() and "poppin" in msg.content.casefold():
            await spam.send(self.add_stars(msg.author, msg.author.channel, rand_num))
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] += 1
            self.data_gatherer(msg, "Complimented Bot", True, rand_num)
        elif rules_followed_counter > 20:
            await spam.send(self.add_stars(msg.author, msg.channel, rand_num))
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
            self.data_gatherer(msg, "Didn't trigger an if statement", True, rand_num)
        elif any(word in msg.content.casefold() for word in good_words):
            if msg.author.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[msg.author.name], 10)
                if dif is True:
                    await spam.send(self.add_stars(msg.author, msg.channel, randint(5,15)))
                    rules_followed["Guilds"][guild.name]["Members"][msg.author.name] += 1
                    timer.update({msg.author.name:datetime.now()})
                    self.data_gatherer(msg, "Said nice word", True, rand_num)
            else:
                await spam.send(self.add_stars(msg.author, msg.channel, randint(5,15)))
                timer.update({msg.author.name:datetime.now()})
                self.data_gatherer(msg, "Said nice word", True, rand_num)
        else:
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] += 1

    @commands.Cog.listener('on_raw_reaction_add')
    async def check_reaction(self, payload):
        global stars
        channel = await self.client.fetch_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        guild = self.client.get_guild(751678259657441339)
        spam = discord.utils.get(guild.text_channels, name='bot-spam')
        bonked = randint(20, 70)
        emote = randint(1,15)
        if payload.member == self.client.user:
            return
        # Bonk Emoji
        if payload.emoji.id == 797305732063297536 and msg.author.bot is False:
            # Checks if person who reacted has reacted before
            if payload.member.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[payload.member.name], 5)
                if dif is True:
                    # Removes stars from the person who sent the message
                    await spam.send(self.remove_stars(msg.author, channel, bonked, reason = f" for being bonked by {payload.member.name}"))
                    timer.update({payload.member.name:datetime.now()})
                    self.data_gatherer(msg, "got bonked", False, -bonked)
                    return
            else:
                await spam.send(self.remove_stars(msg.author, channel, bonked, reason = f" for being bonked by {payload.member.name}"))
                # Adds person to the timer dictionary
                timer.update({payload.member.name:datetime.now()})
                self.data_gatherer(msg, "got bonked", False, -bonked)
                return
        # Any other emoji
        else:
            if payload.member.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[payload.member.name], 20)
                if dif:
                    await spam.send(self.add_stars(payload.member, msg, emote, reason = " for emoting"))
                    timer.update({payload.member.name:datetime.now()})
                    self.data_gatherer(payload.member, "Reacted to a message", True, emote)
                    return
            else:
                await spam.send(self.add_stars(payload.member, msg, emote, reason = " for emoting"))
                timer.update({payload.member.name:datetime.now()})
                self.data_gatherer(payload.member, "Reacted to a message", True, emote)
                return
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = self.client.get_guild(member.guild.id)
        spam = discord.utils.get(guild.text_channels, name='bot-spam')
        channel = guild.system_channel
        # print(after.deaf)
        # print(after.mute)
        rand_num = randint(20, 50)
        audit_logs = guild.audit_logs(limit = 5)
        if after.deaf or after.mute:
            counter = 1
            async for thing in audit_logs:
                if thing.action == discord.AuditLogAction.member_update:
                    await spam.send(self.remove_stars(thing.user, channel,rand_num, reason = f" for muting/deafing {member.name}"))
                    self.data_gatherer(thing.user, "Deafened a person", False, -rand_num)
                    return
    @commands.Cog.listener()
    async def on_member_join(member):
        stars["Guilds"][member.guild.name]["Members"][member.name] = {"Stars":0}
        file = open('./settings/stars.txt', "w+")
        file.write(json.dumps(stars, indent = 4))
        file.close()
        # print(member.name, sep = " ")
    @commands.Cog.listener()
    async def on_member_remove(member):
        stars["Guilds"][member.guild.name]["Members"].pop(member.name)
        file = open('./settings/stars.txt', "w+")
        file.write(json.dumps(stars, indent = 4))
        file.close()
    @commands.command()
    async def stars(self, ctx):
        """This commands allow the user to see how many stars they have, or the person they pinged has"""
        global stars
        author = ctx.author
        name = author.name
        guild = ctx.message.guild
        if len(ctx.message.mentions) == 1:
            member = ctx.message.mentions[0]
            if member.bot is True:
                return
            member_name = member.name
            if member_name in stars["Guilds"][guild.name]["Members"]:
                user_stars = stars["Guilds"][guild.name]["Members"][member.name]["Stars"]
                if "Weekly Stars" in stars["Guilds"][guild.name]["Members"][member.name]:
                    weekly_stars = stars["Guilds"][guild.name]["Members"][member.name]["Weekly Stars"]
                    await ctx.send(f'{member_name} has {user_stars} and also got {weekly_stars} this week')
                else:
                    await ctx.send(f'{member_name} has {user_stars}')
            else:
                await ctx.send(f'Something went wrong, could not find {member_name} on the good noodle board, maybe they are not on the board?')
        elif len(ctx.message.mentions) > 1:
            await ctx.send("Too many members in the command")
        elif len(ctx.message.mentions) == 0:
            if name in stars["Guilds"][guild.name]["Members"]:
                user_stars = stars["Guilds"][guild.name]["Members"][name]["Stars"]
                if "Weekly Stars" in stars["Guilds"][guild.name]["Members"][name]:
                    weekly_stars = stars["Guilds"][guild.name]["Members"][name]["Weekly Stars"]
                    await ctx.send(f'{name} has {user_stars} and also got {weekly_stars} this week')
                    return
                else:
                    await ctx.send(f'{name} has {user_stars}')
            else:
                await ctx.send(f'Something went wrong, could not find you on the good noodle board, maybe you are not on the board?')




def setup(client):
    client.add_cog(Stars(client))
