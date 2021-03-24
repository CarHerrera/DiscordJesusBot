import discord
import json
from random import randint
from discord.ext import commands, tasks
from datetime import datetime
from main import timeChecker
import pandas, csv
file = open("./settings/good_noodle.txt")
data = file.read()
stars = json.loads(data)
file.close()
file = open("./private/swearWords.txt")
bad_words = file.read().split()
file.close()
file = open("./private/positive-words.txt")
good_words = file.read().split()
file.close()
timer = {}
last_reset = datetime.now()
rules_followed = {"Guilds":[]}
test_stars = None
# cities = pandas.DataFrame(columns=['Guild', 'Member', 'Reason', 'Added', 'Stars', 'Day', 'MSGID', 'Channel'])
# cities.to_csv('./private/good_noodle_data.csv', index = False)
try:
    stars_data = open("./private/good_noodle_data.csv", "a")
except FileNotFoundError:
    df = pandas.DataFrame(columns=['Guild', 'Member', 'Reason', 'Added', 'Stars', 'Day', 'MSGID', 'Channel'])
    df.to_csv('./private/good_noodle_data.csv', index = False)
    stars_data = open("./private/good_noodle_data.csv", "a")
class Stars(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.reset_weekly_stars.start()
    @tasks.loop(hours = 24)
    # This loops every 24 hours and resets the servers weekly stars and send a message with who had the highest and lowest stars
    async def reset_weekly_stars(self):
        global last_reset
        day = datetime.now().strftime("%A")
        if day == "Monday":
            last_reset = datetime.now()
            idx = 0
            number_of_stars = []
            members_list = []
            for guild in self.client.guilds:
                if guild.name in stars["Guilds"][idx]:
                    for index in range(len(stars["Guilds"][idx]["Members"])):
                        # Checks if the member has any weekly stars
                        if "Weekly_Stars" in stars["Guilds"][idx]["Members"][index].keys():
                            # Adds the number of weekly stars to a list
                            number_of_stars.append(stars["Guilds"][idx]["Members"][index]["Weekly_Stars"])
                            # Adds members to a seperate list
                            members_list.append(list(iter(stars["Guilds"][idx]["Members"][index].keys()))[0])
                            stars["Guilds"][idx]["Members"][index]["Weekly_Stars"] = 0
                idx += 1
                if len(number_of_stars) > 0:
                    channel = discord.utils.get(guild.text_channels, name='bot-spam')
                    highest_stars = max(number_of_stars)
                    highest = number_of_stars.index(highest_stars)
                    user = members_list[highest]
                    member = discord.utils.find(lambda m: m.name == user, guild.members)
                    lowest_stars = min(number_of_stars)
                    user_low = members_list[number_of_stars.index(lowest_stars)]
                    lowest_member = discord.utils.find(lambda m: m.name == user_low, guild.members)
                    await channel.send(f"{member.mention} got this weeks highest stars at {highest_stars} and unsurprisngly {lowest_member.mention} got the lowest amount of stars at {lowest_stars}")
            file = open("./settings/good_noodle.txt", "w")
            file.write(json.dumps(stars, indent = 4))
            file.close()
            print("Stars have been reset")
    @reset_weekly_stars.before_loop
    async def before_check(self):
        await self.client.wait_until_ready()
        global test_stars, rules_followed
        try:
            file = open('./settings/stars.txt', "r")
            test_stars = json.loads(file.read())
            file.close()
            print("Opened existing file")
        except FileNotFoundError:
            test_stars = {"Guilds":{}}
            async for guild in self.client.fetch_guilds():
                if guild.name not in test_stars["Guilds"].keys():
                    test_stars["Guilds"][guild.name] = {"Members":{}}
                    test_stars["Guilds"][guild.name]["Sent"] = False
                async for member in guild.fetch_members():
                    if member.name not in test_stars["Guilds"][guild.name]["Members"].keys() and member.bot is False:
                        test_stars["Guilds"][guild.name]["Members"][member.name] = {"Stars": 0}
            print("Created a stars file")
            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(test_stars, indent = 4))
            file.close()
    def remove_stars(self, user, channel, rand_num, reason = ""):
        """This function removes stars"""
        global stars
        member = user
        name = member.name
        guild = member.guild
        working_stars = None
        GuildIndex = None
        for index in range(len(stars["Guilds"])):
            if guild.name in stars["Guilds"][index]:
                GuildIndex = index
        for index in range(len(stars["Guilds"][GuildIndex]["Members"])):
            if name in stars["Guilds"][GuildIndex]["Members"][index]:
                if "Weekly_Stars" not in stars["Guilds"][GuildIndex]["Members"][index]:
                    stars["Guilds"][GuildIndex]["Members"][index].update({"Weekly_Stars":0})
                    stars["Guilds"][GuildIndex]["Members"][index]["Weekly_Stars"]-= rand_num
                else:
                    stars["Guilds"][GuildIndex]["Members"][index]["Weekly_Stars"] -= rand_num
                stars["Guilds"][GuildIndex]["Members"][index]["Stars"]-=rand_num
        file = open("./settings/good_noodle.txt", "w")
        file.write(json.dumps(stars, indent = 4))
        file.close()
        return f"{name} loses {rand_num} good noodle star(s){reason}"
    def add_stars(self, user, channel, rand_num, reason = ""):
        """This function adds stars"""
        global stars
        member = user
        name = member.name
        guild = member.guild
        working_stars = None
        GuildIndex = None
        for index in range(len(stars["Guilds"])):
            if guild.name in stars["Guilds"][index]:
                GuildIndex = index
        for index in range(len(stars["Guilds"][GuildIndex]["Members"])):
            if name in stars["Guilds"][GuildIndex]["Members"][index]:
                # Checks if weekly stars are in the members dictionary. If not means either hasn't messaged enough to remove and add stars.
                if "Weekly_Stars" not in stars["Guilds"][GuildIndex]["Members"][index].keys():
                    stars["Guilds"][GuildIndex]["Members"][index].update({"Weekly_Stars":0})
                    stars["Guilds"][GuildIndex]["Members"][index]["Weekly_Stars"] += rand_num
                else:
                    stars["Guilds"][GuildIndex]["Members"][index]["Weekly_Stars"] += rand_num
                stars["Guilds"][GuildIndex]["Members"][index]["Stars"] += rand_num
        file = open("./settings/good_noodle.txt", "w")
        file.write(json.dumps(stars, indent = 4))
        file.close()
        return f"{name} gains {rand_num} good noodle star(s){reason}"
    def generate_rules_followed(self):
        global rules_followed
        counter = 0
        if len(rules_followed["Guilds"]) == 0:
            for guild in self.client.guilds:
                rules_followed["Guilds"].append({guild.name:guild.id, "Members":{}})
            return
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
        count = 0
        index = 0
        guild = msg.guild
        if len(rules_followed["Guilds"]) == 0:
            # Creates a dictionary of all the guilds the client is connected to
            self.generate_rules_followed()
        for server in rules_followed["Guilds"]:
            if msg.guild.name in server.keys():
                # Checks if the user that sent a message is in the dictionary, if not will add it to it
                if msg.author.name not in rules_followed["Guilds"][index]["Members"].keys():
                    rules_followed["Guilds"][index]["Members"].update({msg.author.name:0})
                break
            index += 1
        try:
            difference = timeChecker(datetime.now(), timer[msg.author.name], 5)
        except:
            difference = None
        rules_followed_counter = rules_followed["Guilds"][index]["Members"][msg.author.name]
        async for message in msg.channel.history(limit = 10):
            if len(message.attachments) > 0 or len(message.embeds) > 0:
                pass
            elif message.author == msg.author:
                count+= 1
        if any(word in msg.content.casefold() for word in bad_words):
            if msg.author.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[msg.author.name], 10)
                if dif is True:
                    await msg.channel.send(self.remove_stars(msg.author, msg.channel, randint(1, 30)))
                    rules_followed["Guilds"][index]["Members"][msg.author.name] = 0
                    timer.update({msg.author.name:datetime.now()})
                    self.data_gatherer(msg, "Bad words", False, -rand_num)
            else:
                await msg.channel.send(self.remove_stars(msg.author, msg.channel, randint(1, 30)))
                rules_followed["Guilds"][index]["Members"][msg.author.name] = 0
                timer.update({msg.author.name:datetime.now()})
                self.data_gatherer(msg, "Bad words", False, -rand_num)
            return
        elif count > 8:
            await msg.channel.send(self.remove_stars(msg.author, msg.channel, rand_num, reason = " for being a dick head"))
            rules_followed["Guilds"][index]["Members"][msg.author.name] = 0
            self.data_gatherer(msg, "Spammed Messages", False, -rand_num)
        elif len(msg.content) > 250:
            if len(msg.embeds) > 0 or len(msg.attachments) > 0:
                return
            else:
                await msg.channel.send(self.remove_stars(msg.author, msg.channel, rand_num, reason = " for sending way to long of a message"))
                rules_followed["Guilds"][index]["Members"][msg.author.name] = 0
                self.data_gatherer(msg, "Long message", False, -rand_num)
        elif msg.content.isupper():
            await msg.channel.send(self.remove_stars(msg.author, msg.channel, rand_num, reason = " for being aggressive"))
            rules_followed["Guilds"][index]["Members"][msg.author.name] = 0
            self.data_gatherer(msg, "Message in caps", False, -rand_num)
            return
        elif "bot" in msg.content.casefold() and "poppin" in msg.content.casefold():
            await msg.channel.send(self.add_stars(msg.author, msg.author.channel, rand_num))
            rules_followed["Guilds"][index]["Members"][msg.author.name] += 1
            self.data_gatherer(msg, "Complimented Bot", True, rand_num)
        elif rules_followed_counter > 20:
            star_rules = randint(30, 100)
            await msg.channel.send(self.add_stars(msg.author, msg.channel, star_rules))
            rules_followed["Guilds"][index]["Members"][msg.author.name] = 0
            self.data_gatherer(msg, "Didn't trigger an if statement", True, rand_num)
        elif any(word in msg.content.casefold() for word in good_words):
            if msg.author.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[msg.author.name], 10)
                if dif is True:
                    await msg.channel.send(self.add_stars(msg.author, msg.channel, randint(5,10)))
                    rules_followed["Guilds"][index]["Members"][msg.author.name] += 1
                    timer.update({msg.author.name:datetime.now()})
                    self.data_gatherer(msg, "Said nice word", True, rand_num)
            else:
                await msg.channel.send(self.add_stars(msg.author, msg.channel, randint(5,10)))
                timer.update({msg.author.name:datetime.now()})
                self.data_gatherer(msg, "Said nice word", True, rand_num)
        else:
            rules_followed["Guilds"][index]["Members"][msg.author.name] += 1

    @commands.Cog.listener('on_raw_reaction_add')
    async def check_reaction(self, payload):
        global stars
        channel = await self.client.fetch_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        guild = self.client.get_guild(751678259657441339)
        spam = discord.utils.get(guild.text_channels, name='bot-spam')
        bonked = randint(20, 80)
        emote = randint(1,10)
        if payload.member == self.client.user:
            return
        # Bonk Emoji
        if payload.emoji.id == 797305732063297536:
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
                await spam.send(self.remove_stars(msg.author, channel, rand_num, reason = f" for being bonked by {payload.member.name}"))
                # Adds person to the timer dictionary
                timer.update({payload.member.name:datetime.now()})
                self.data_gatherer(msg, "got bonked", False, -randint(10,60))
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


    @commands.command()
    async def stars(self, ctx):
        """This commands allow the user to see how many stars they have, or the person they pinged has"""
        global stars
        author = ctx.author
        name = author.name
        guild = ctx.message.guild
        working_stars = None
        for key in stars["Guilds"]:
            if guild.name in key:
                working_stars = key
        if len(ctx.message.mentions) == 1:
            member = ctx.message.mentions[0]
            member_name = member.name
            for _ in range(len(working_stars["Members"])):
                if member_name in working_stars["Members"][_]:
                    await ctx.send("{} has {} good noodle stars".format(member_name, working_stars["Members"][_]["Stars"]))
                    if "Weekly_Stars" in working_stars["Members"][_].keys():
                        await ctx.send(f'{member_name} also got {working_stars["Members"][_]["Weekly_Stars"]} this week')
                    return
            else:
                await ctx.send(f"Could not find {name} on the good noodle board")
                return
        elif len(ctx.message.mentions) > 1:
            await ctx.send("Too many members in the command")
        elif len(ctx.message.mentions) == 0:
            for _ in range(len(working_stars["Members"])):
                if name in working_stars["Members"][_]:
                    await ctx.send("{} has {} good noodle stars".format(name, working_stars["Members"][_]["Stars"]))
                    if "Weekly_Stars" in working_stars["Members"][_].keys():
                        await ctx.send(f'{name} also got {working_stars["Members"][_]["Weekly_Stars"]} this week')
                    return
            else:
                await ctx.send(f'Something went wrong, could not find you on the good noodle board, maybe you are not on the board?')
    @commands.command()
    async def reset(self,ctx):
        """This command is meant to reset a users stars"""
        if ctx.author.id == 263054069885566977:
            global stars
            member= ctx.message.mentions[0]
            name = member.name
            guild = member.guild
            print(guild)
            working_stars = None
            GuildIndex = None
            for index in range(len(stars["Guilds"])):
                if guild.name in stars["Guilds"][index]:
                    GuildIndex = index
            for index in range(len(stars["Guilds"][GuildIndex]["Members"])):
                if name in stars["Guilds"][GuildIndex]["Members"][index]:
                    if "Weekly_Stars" not in stars["Guilds"][GuildIndex]["Members"][index].keys():
                        stars["Guilds"][GuildIndex]["Members"][index].update({"Weekly_Stars":0})
                    else:
                        stars["Guilds"][GuildIndex]["Members"][index]["Weekly_Stars"] = 0
                    stars["Guilds"][GuildIndex]["Members"][index]["Stars"] = 0
            file = open("./settings/good_noodle.txt", "w")
            file.write(json.dumps(stars, indent = 4))
            file.close()




def setup(client):
    client.add_cog(Stars(client))
