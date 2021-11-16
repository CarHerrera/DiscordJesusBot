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
stars = None
rules_followed = {"Guilds":{}}
load_dotenv(dotenv_path = "./private/.env")
# cities = pandas.DataFrame(columns=['Guild', 'Member', 'Reason', 'Added', 'Stars', 'Day', 'MSGID', 'Channel'])
# cities.to_csv('./private/good_noodle_data.csv', index = False)
voice_state = {"Guilds": {}}
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
        self.time = datetime.now()
        if self.time.hour != 0:
            self.time = datetime(self.time.year, self.time.month, self.time.day, hour=0)

    def weekFunc(dict, tup):
        # print("IN Func")
        key,d = tup
        # print(dict)
        # print(tup)
        return d['Weekly Stars']

    @tasks.loop(minutes = 1)
    # This loops every 24 hours and resets the servers weekly stars and send a message with who had the highest and lowest stars
    async def reset_weekly_stars(self):
        global stars, stars_data
        file = open('./private/server_settings.txt', "r")
        settings = json.loads(file.read())
        file.close()
        day = datetime.now().strftime("%A")
        time = datetime.now()
        for guild in self.client.guilds:
            sent = stars["Guilds"][guild.name]["Sent"]
            if settings['Guilds'][guild.name]['Settings']['Stars']['All Stars'] is False:
                return
            elif settings['Guilds'][guild.name]['Settings']['Stars']['Weekly Stars'] is False:
                return
            elif day != "Monday":
                stars["Guilds"][guild.name]["Sent"] = False
            elif day == "Monday" and time.hour == 15 and sent is False:
                members = stars["Guilds"][guild.name]["Members"]
                ordered_stars = sorted(members.items(), key = self.weekFunc, reverse = True)
                top3 = ordered_stars[:3]
                bot3 = ordered_stars[-3:]
                channel_name = settings['Guilds'][guild.name]['Settings']['Pref Channel']
                channel = discord.utils.get(guild.text_channels, name= channel_name)
                weekly_leaderboard = discord.Embed(title = f"🏆Top 3 Users of the week on {guild.name}🏆")
                for x in range(len(top3)):
                    member = await guild.fetch_member(int(top3[x][0]))
                    if x == 0:
                        weekly_leaderboard.add_field(name =f"🥇Number 1🥇", value = f"{member.name} with {top3[0][1]['Weekly Stars']} 🌟🌟🌟")
                    elif x == 1:
                        weekly_leaderboard.add_field(name =f"🥈Number 2🥈", value = f"{member.name} with {top3[1][1]['Weekly Stars']} 🌟🌟")
                    elif x == 2:
                        weekly_leaderboard.add_field(name =f"🥉Number 3🥉", value = f"{member.name} with {top3[2][1]['Weekly Stars']} 🌟")
                bot_3_board = discord.Embed(title = f"Bottom 3 Users of the week on {guild.name}")
                for x in range(len(bot3)):
                    member = await guild.fetch_member(int(bot3[x][0]))
                    if x == 0:
                        bot_3_board.add_field(name =f"Number 1", value = f"{member.name} with {bot3[0][2]['Weekly Stars']}")
                    elif x == 1:
                        bot_3_board.add_field(name =f"Number 2", value = f"{member.name} with {bot3[1][1]['Weekly Stars']}")
                    elif x == 2:
                        bot_3_board.add_field(name =f"Number 3", value = f"{member.name} with {bot3[2][0]['Weekly Stars']}")
                await channel.send(embed = weekly_leaderboard)
                await channel.send(embed = bot_3_board)
                stars["Guilds"][guild.name]["Sent"] = True
                for members in guild.members:
                    id = str(member.id)
                    stars["Guilds"][guild.name]["Members"][id]["Weekly Stars"] = 0
                try:
                    file_trasnfer = db_uploader.TransferData(os.getenv('ACCESS_TOKEN'))
                    file_from = "./private/good_noodle_data.csv"
                    today = datetime.now().strftime("%m-%d-%y")
                    file_to = f"/code/Python/Discord/StarsData/{today} stars.csv"
                    file_trasnfer.upload_file(file_from, file_to)
                    if stars_data.closed:
                        stars_data = open("./private/good_noodle_data.csv", "w")
                        stars_data.write("Guild,Member,Reason,Added,Stars,Day,MSGID,Channel\n")
                        stars_data.close()
                    else:
                        stars_data.close()
                        stars_data = open("./private/good_noodle_data.csv", "w")
                        stars_data.write("Guild,Member,Reason,Added,Stars,Day,MSGID,Channel\n")
                        stars_data.close()
                except Exception:
                    print(str(Exception))
        file = open('./settings/stars.txt', "w")
        file.write(json.dumps(stars, indent = 4))
        file.close()

    @reset_weekly_stars.before_loop
    async def before_check(self):
        await self.client.wait_until_ready()
        global stars, rules_followed
        async for guild in self.client.fetch_guilds():
            rules_followed["Guilds"][guild.name] = {"Members":{}}
            voice_state["Guilds"][guild.name] = {"Members":{}}
        try:
            file = open('./settings/stars.txt', "r")
            stars = json.loads(file.read())
            file.close()
            # # async for guild in self.client.fetch_guilds():
            # #     async for member in guild.fetch_members():
            # #         if member.bot is True:
            # #             continue
            # #         if 'Weekly Stars' not in stars['Guilds'][guild.name]['Members'][member.name].keys():
            # #             stars["Guilds"][guild.name]["Members"][member.name]['Weekly Stars'] = 0
            # #         stars["Guilds"][guild.name]["Members"][member.name]['Daily'] = 0
            # file = open('./settings/stars.txt', "w+")
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
                        stars["Guilds"][guild.name]["Members"][member.name] = {
                        "Stars": 0,
                        'Weekly Stars': 0,
                        'Daily': 0
                        }
            print("Created a stars file")
            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(stars, indent = 4))
            file.close()
    def remove_stars(self, user, rand_num, reason = ""):
        """This function removes stars"""
        if user.bot is True:
            return
        global stars
        file = open('./private/server_settings.txt', "r")
        settings = json.loads(file.read())
        file.close()
        member = user
        name = member.name
        guild = member.guild
        id = str(member.id)
        time_dif = datetime.now() - self.time
        if time_dif.days > 0:
            self.time = datetime.now()
            stars['Guilds'][guild.name]['Members'][id]['Daily'] = 0
        if id in stars["Guilds"][guild.name]["Members"]:
            stars['Guilds'][guild.name]['Members'][id]['Daily'] -= rand_num
            stars['Guilds'][guild.name]['Members'][id]['Weekly Stars'] -= rand_num
            stars['Guilds'][guild.name]['Members'][id]['Stars'] -= rand_num
        file = open('./settings/stars.txt', "w+")
        file.write(json.dumps(stars, indent = 4))
        file.close()
        return f"{name} loses {rand_num} good noodle star(s){reason}"
    def add_stars(self, user, rand_num, reason = ""):
        # TODO implement a way to make daily stars work
        # Idea 1: Make it so that if the server has daily limit on, add it that stars file only Then resets at midnight
        """This function adds stars"""
        if user.bot is True:
            return
        global stars
        file = open('./private/server_settings.txt', "r")
        settings = json.loads(file.read())
        file.close()
        member = user
        name = member.name
        guild = member.guild
        id = str(member.id)
        time_dif = datetime.now() - self.time
        if time_dif.days > 0:
            self.time = datetime.now()
            stars['Guilds'][guild.name]['Members'][id]['Daily'] = 0
        daily_cap = settings['Guilds'][guild.name]['Settings']['Stars']['Daily Cap']
        if id in stars["Guilds"][guild.name]["Members"]:
            if daily_cap == None:
                stars['Guilds'][guild.name]['Members'][id]['Daily'] += rand_num
                stars['Guilds'][guild.name]['Members'][id]['Weekly Stars'] += rand_num
                stars['Guilds'][guild.name]['Members'][id]['Stars'] += rand_num
            else:
                if stars['Guilds'][guild.name]['Members'][id]['Daily'] >= daily_cap:
                    stars['Guilds'][guild.name]['Members'][id]['Daily'] = daily_cap
                    return
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
        rand_num = randint(10, 90)
        guild = msg.guild
        local_change = os.path.getmtime('./private/server_settings.txt')
        file = open('./private/server_settings.txt', "r")
        settings = json.loads(file.read())
        file.close()
        if msg.author == self.client.user:
            return
        elif msg.author.bot == True:
            return
        elif settings['Guilds'][guild.name]['Settings']['Stars']['All Stars'] is False:
            return
        elif settings['Guilds'][guild.name]['Settings']['Stars']['MSG Stars'] is False:
            return
        count = 0
        file = open('./settings/counter.txt')
        message_count = int(file.read().split('=')[1]) % 1000
        file.close()
        # print(message_count)
        pref_channel = settings['Guilds'][guild.name]['Settings']['Pref Channel']
        spam = discord.utils.get(guild.text_channels, name= pref_channel)
        star_update = None
        if msg.guild.name in rules_followed["Guilds"]:
            # Checks if the user that sent a message is in the dictionary, if not will add it to it
            if msg.author.name not in rules_followed["Guilds"][guild.name]["Members"].keys():
                rules_followed["Guilds"][guild.name]["Members"][msg.author.name]= 0
        try:
            difference = timeChecker(datetime.now(), timer[msg.author.name], 5)
        except:
            difference = None
        rules_followed_counter = rules_followed["Guilds"][guild.name]["Members"][msg.author.name]
        if msg.channel.id == 762894482311217172 or msg.channel.id == 776308635369472030:
            pass
        else:
            async for message in msg.channel.history(limit = 10):
                time_dif = datetime.utcnow() - message.created_at
                if time_dif.total_seconds() < 600:
                    if message.author == msg.author:
                        count+= 1
        if any(word in msg.content.casefold() for word in bad_words):
            bad_rand = randint(1, 69)
            if msg.author.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[msg.author.name], 10)
                if dif is True:
                    star_update = self.remove_stars(msg.author, bad_rand)
                    # await spam.send()
                    rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
                    timer.update({msg.author.name:datetime.now()})
                    self.data_gatherer(msg, "Bad words", False, -bad_rand)
            else:
                star_update = self.remove_stars(msg.author, bad_rand)
                # await spam.send(self.remove_stars(msg.author, bad_rand))
                rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
                timer.update({msg.author.name:datetime.now()})
                self.data_gatherer(msg, "Bad words", False, -bad_rand)
            return
        elif rand_num == 69:
            good_stars = randint(1000, 2000)
            star_update = self.add_stars(msg.author, good_stars, reason =" bc u haven't pissed me off yet")
            self.data_gatherer(msg, "Bad RNG", True ,good_stars)
        elif message_count % 997 == 0:
            rand_chance_stars = randint(1000, 70000)
            # spam.send()
            star_update = self.remove_stars(msg.author, rand_chance_stars, reason =" bc fuck you thats why")
            self.data_gatherer(msg, "Bad RNG", True ,-rand_chance_stars)
        elif count > 8:
            spam_rand = randint(10, 70)
            # await spam.send()
            star_update = self.remove_stars(msg.author, spam_rand, reason = " for being a dick head")
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
            self.data_gatherer(msg, "Spammed Messages", False, -spam_rand)
        elif len(msg.content) > 300:
            if len(msg.embeds) > 0 or len(msg.attachments) > 0:
                return
            else:
                star_update = self.remove_stars(msg.author, rand_num, reason = " for sending way to long of a message")
                # await spam.send()
                rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
                self.data_gatherer(msg, "Long message", False, -rand_num)
        elif msg.content.isupper():
            if len(msg.content) > 4:
                star_update = self.remove_stars(msg.author, rand_num, reason = " for being aggressive")
                # await spam.send()
                rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
                self.data_gatherer(msg, "Message in caps", False, -rand_num)
                return
            else:
                return
        elif "bot" in msg.content.casefold() and "poppin" in msg.content.casefold():
            star_update = self.add_stars(msg.author, rand_num)
            # await spam.send()
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] += 1
            self.data_gatherer(msg, "Complimented Bot", True, rand_num)
        elif rules_followed_counter > 19:
            no_trigger = randint(40, 180)
            star_update = self.add_stars(msg.author, no_trigger)
            # await spam.send()
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
            self.data_gatherer(msg, "Didn't trigger an if statement", True, no_trigger)
        elif any(word in msg.content.casefold() for word in good_words):
            nice_rand = randint(10, 50)
            if msg.author.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[msg.author.name], 10)
                if dif is True:
                    star_update = self.add_stars(msg.author, nice_rand)
                    # await spam.send()
                    rules_followed["Guilds"][guild.name]["Members"][msg.author.name] += 1
                    timer.update({msg.author.name:datetime.now()})
                    self.data_gatherer(msg, "Said nice word", True, nice_rand)
            else:
                star_update = self.add_stars(msg.author, nice_rand)
                # await spam.send(self.add_stars(msg.author, nice_rand))
                timer.update({msg.author.name:datetime.now()})
                self.data_gatherer(msg, "Said nice word", True, nice_rand)
        else:
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] += 1
        if settings['Guilds'][guild.name]['Settings']['Stars']['Star Updates'] and star_update is not None:
            print(star_update)
            await spam.send(star_update)
        else:
            return

    @commands.Cog.listener('on_raw_reaction_add')
    async def check_reaction(self, payload):
        global stars, rules_followed
        channel = await self.client.fetch_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        guild = self.client.get_guild(payload.guild_id)
        file = open('./private/server_settings.txt', "r")
        settings = json.loads(file.read())
        file.close()
        pref_channel = settings['Guilds'][guild.name]['Settings']['Pref Channel']
        spam = discord.utils.get(guild.text_channels, name= pref_channel)
        bonked = randint(30, 80)
        emote = randint(5,20)
        star_update = None
        member = payload.member.name
        if payload.member == self.client.user:
            return
        elif settings['Guilds'][guild.name]['Settings']['Stars']['All Stars'] is False:
            return
        elif settings['Guilds'][guild.name]['Settings']['Stars']['Emote Stars'] is False:
            return
        # Bonk Emoji
        if payload.emoji.id == 797305732063297536 and msg.author.bot is False:
            # Checks if person who reacted has reacted before
            if member in timer.keys():
                dif = datetime.now() - timer[member]
                if dif.total_seconds() >= 300:
                    # Removes stars from the person who sent the message
                    star_update = self.remove_stars(msg.author, bonked, reason = f" for being bonked by {payload.member.name}")
                    timer.update({payload.member.name:datetime.now()})
                    self.data_gatherer(msg, "got bonked", False, -bonked)
                else:
                    star_update = self.remove_stars(msg.author, bonked, reason = f" for being bonked by {payload.member.name}")
                    # Adds person to the timer dictionary
                    timer.update({payload.member.name:datetime.now()})
                    self.data_gatherer(msg, "got bonked", False, -bonked)
        elif payload.emoji.id == 815051855859023872 and msg.author.bot is False:
            hunter = await guild.fetch_member(352550834103386133)
            star_update = self.add_stars(hunter, randint(1,10), reason = f" hunter tax")
        # Any other emoji
        else:
            if  member in timer.keys():
                dif = datetime.now() - timer[member]
                if dif.total_seconds() >= 300:
                    star_update = self.add_stars(payload.member, emote, reason = " for emoting")
                    # await spam.send(self.add_stars(payload.member, emote, reason = " for emoting"))
                    timer.update({payload.member.name:datetime.now()})
                    self.data_gatherer(payload.member, "Reacted to a message", True, emote)
            else:
                star_update = self.add_stars(payload.member, emote, reason = " for emoting")
                timer.update({payload.member.name:datetime.now()})
                self.data_gatherer(payload.member, "Reacted to a message", True, emote)
        if settings['Guilds'][guild.name]['Settings']['Stars']['Star Updates'] and star_update is not None:
            await spam.send(star_update + " " + msg.jump_url)
            # print(msg.jump_url)
        else:
            return
    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #     global rules_followed
    #     guild = self.client.get_guild(member.guild.id)
    #     if settings['Guilds'][guild.name]['Settings']['Stars']['All Stars'] is False:
    #         return
    #     elif settings['Guilds'][guild.name]['Settings']['Stars']['Mod Checks'] is False:
    #         return
    #     pref_channel = settings['Guilds'][guild.name]['Settings']['Pref Channel']
    #     spam = discord.utils.get(guild.text_channels, name= pref_channel)
    #     channel = guild.system_channel
    #     # print(after.deaf)
    #     # print(after.mute)
    #     rand_num = randint(20, 50)
    #     audit_logs = guild.audit_logs(limit = 5)
    #     if after.deaf or after.mute:
    #         counter = 1
    #         async for thing in audit_logs:
    #             if thing.action == discord.AuditLogAction.member_update:
    #                 await spam.send(self.remove_stars(thing.user,rand_num, reason = f" for muting/deafing {member.name}"))
    #                 self.data_gatherer(thing.user, "Deafened a person", False, -rand_num)
    #                 if guild.name in rules_followed["Guilds"]:
    #                     # Checks if the user that sent a message is in the dictionary, if not will add it to it
    #                     if thing.user.name not in rules_followed["Guilds"][guild.name]["Members"].keys():
    #                         rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
    #                     else:
    #                         rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
    #                 return
    @commands.Cog.listener()
    async def on_member_join(self, member):
        stars["Guilds"][member.guild.name]["Members"][member.id] = {
        "Stars":0,
        'Weekly Stars' : 0,
        'Daily' : 0,
        "Name":member.name,
        }
        file = open('./settings/stars.txt', "w+")
        file.write(json.dumps(stars, indent = 4))
        file.close()
        # print(member.name, sep = " ")
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        stars["Guilds"][member.guild.name]["Members"].pop(member.id)
        file = open('./settings/stars.txt', "w+")
        file.write(json.dumps(stars, indent = 4))
        file.close()

    # @commands.Cog.listener()
    # async def on_user_update(self, before, after):
    #     if before.bot or after.bot:
    #         return
    #     if before.name != after.name:
    #         async for guild in self.client.fetch_guilds():
    #             # async for member in guild.fetch_members():
    #             if before.name in stars['Guilds'][guild.name]["Members"].keys():
    #                 temp_stars = stars['Guilds'][guild.name]["Members"][before.name]
    #                 stars["Guilds"][member.guild.name]["Members"].pop(before.name)
    #                 stars["Guilds"][member.guild.name]["Members"][after.name] = temp_stars
    #         file = open('./settings/stars.txt', "w+")
    #         file.write(json.dumps(stars, indent = 4))
    #         file.close()
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global voice_state
        guild = member.guild
        file = open('./private/server_settings.txt', "r")
        settings = json.loads(file.read())
        file.close()
        if member.bot is True:
            return
        elif settings['Guilds'][guild.name]['Settings']['Stars']['All Stars'] is False:
            return
        elif settings['Guilds'][guild.name]['Settings']['Stars']['VC Stars'] is False:
            return
        pref_channel = settings['Guilds'][guild.name]['Settings']['Pref Channel']
        spam = discord.utils.get(guild.text_channels, name= pref_channel)
        stars = 0
        star_update = None
        try:
            if guild.name in voice_state["Guilds"]:
                if after.channel is not None and member.name not in voice_state['Guilds'][guild.name]["Members"]:
                    voice_state['Guilds'][guild.name]["Members"][member.name] = datetime.now()
            if after.channel is None:
                delta_obj = datetime.now() -voice_state['Guilds'][guild.name]["Members"][member.name]
                difference_in_secs = delta_obj.total_seconds()
                if difference_in_secs < 300:
                    return
                stars = int(difference_in_secs * 0.01)
                if stars < 5:
                    stars = 5
                elif stars > 180:
                    stars = 180
                if before.afk:
                    stars *= -1
                    star_update = self.remove_stars(member, stars, reason = " being in afk channel")
                    # await spam.send(self.remove_stars(member, stars, reason = " being in afk channel"))
                    self.data_gatherer(member, "Was in afk channel", False, stars)
                else:
                    star_update = self.add_stars(member, stars)
                    # await spam.send(self.add_stars(member, stars))
                    self.data_gatherer(member, "Being in a VC", False, stars)
                voice_state['Guilds'][guild.name]["Members"].pop(member.name)
            if settings['Guilds'][guild.name]['Settings']['Stars']['Star Updates'] and star_update is not None:
                await spam.send(star_update)
            else:
                return
        except:
            print('Was in a voice channel and was not added to dict')
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.name != after.name:
            stars["Guilds"][after.name] = stars["Guilds"][before.name]
            del stars["Guilds"][before.name]
            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(stars, indent = 4))
            file.close()
    @commands.command()
    async def stars(self, ctx):
        """This commands allow the user to see how many stars they have, or the person they pinged has"""
        global stars
        author = ctx.author
        name = author.name
        id = str(author.id)
        guild = ctx.message.guild
        if self.time.day != datetime.now().day:
            self.time = datetime.now()
            stars['Guilds'][guild.name]['Members'][id]['Daily'] = 0
            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(stars, indent = 4))
            file.close()
        if len(ctx.message.mentions) == 1:
            member = ctx.message.mentions[0]
            if member.bot is True:
                return
            member_name = member.name
            member_id = str(member.id)
            if member_id in stars["Guilds"][guild.name]["Members"]:
                user_stars = stars["Guilds"][guild.name]["Members"][member_id]["Stars"]
                daily = stars["Guilds"][guild.name]["Members"][member_id]["Daily"]
                await ctx.send(f'{member_name} has {user_stars} and also got {daily} today')
            else:
                await ctx.send(f'Something went wrong, could not find {member_name} on the good noodle board, maybe they are not on the board?')
        elif len(ctx.message.mentions) > 1:
            await ctx.send("Too many members in the command")
        elif len(ctx.message.mentions) == 0:
            if id in stars["Guilds"][guild.name]["Members"]:
                user_stars = stars["Guilds"][guild.name]["Members"][id]["Stars"]
                daily = stars["Guilds"][guild.name]["Members"][id]["Daily"]
                await ctx.send(f'{name} has {user_stars} and also got {daily} today')
            else:
                await ctx.send(f'Something went wrong, could not find you on the good noodle board, maybe you are not on the board?')

    def keyFunc(dict, tup):
        # print("IN Func")
        key,d = tup
        # print(dict)
        # print(tup)
        return d['Stars']

    @commands.command()
    async def leaderboard(self, ctx, *args):
        global stars
        guild = ctx.message.guild
        members = stars["Guilds"][guild.name]["Members"]
        ordered_stars = sorted(members.items(), key = self.keyFunc, reverse = True)
        x = 5
        if(len(args) == 1):
            try:
                print(type(args[0]))
                x = int(args[0])
            except:
                await ctx.send("Hmu when you learn how the command works ✌️")
                return
        topX = ordered_stars[:x]
        leaderboard = discord.Embed(title = f"🏆Top {x} Users on {guild.name}🏆")
        for i in range(len(topX)):
            member = await guild.fetch_member(int(topX[i][0]))
            if( i == 0):
                leaderboard.add_field(name =f"🥇Number {i+1}🥇", value = f"{member.name} with {topX[i][1]['Stars']} 🌟🌟🌟")
            elif i == 1:
                leaderboard.add_field(name =f"🥈Number {i+1}🥈", value = f"{member.name} with {topX[i][1]['Stars']} 🌟🌟")
            elif i==2:
                leaderboard.add_field(name =f"🥉Number {i+1}🥉", value = f"{member.name} with {topX[i][1]['Stars']} 🌟")
            else:
                leaderboard.add_field(name =f"Number {i+1}", value = f"{member.name} with {topX[i][1]['Stars']} ⭐")
        await ctx.send(embed =leaderboard)

    def check_for_owner_of_bot(self, ctx):
        return ctx.message.author.id == 263054069885566977
        # print(ordered_stars[:5])
    @commands.command()
    async def resetFile(self, ctx):
        if self.check_for_owner_of_bot(ctx):
            global stars
            guild = ctx.message.guild
            name = ctx.message.author.name
            member_list = stars["Guilds"][guild.name]["Members"]
            print(member_list[name])
            async for member in guild.fetch_members():
                if member.name not in member_list and member.bot is False:
                    # print(member.name)
                    stars["Guilds"][guild.name]["Members"][member.name] = {
                    "Stars": 0,
                    'Weekly Stars': 0,
                    'Daily': 0,
                    }
            people_not_in = []
            for x,y in stars["Guilds"][guild.name]["Members"].items():
                # print(y)
                if(guild.get_member_named(x) is None):
                    people_not_in.append(x)
            print(people_not_in)
            for x in people_not_in:
                stars["Guilds"][member.guild.name]["Members"].pop(x)

            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(stars, indent = 4))
            file.close()
        else:
            await ctx.send('No')
    @commands.command()
    async def fake(self, ctx):
        if self.check_for_owner_of_bot(ctx):
            file = open('./settings/stars.txt', "r")
            local_stars = json.loads(file.read())
            file.close()
            guild = ctx.message.guild
            name = ctx.message.author.name
            # member_list = stars["Guilds"][guild.name]["Members"]
            # print(member_list[name])
            print(local_stars)
            newStars = {"Guilds": {}}
            async for guild in self.client.fetch_guilds():
                newStars["Guilds"][guild.name] = {"Members":{}}
                newStars["Guilds"][guild.name]["Sent"] = False
                async for member in guild.fetch_members():
                    if member.bot is False and member.name not in newStars['Guilds'][guild.name]["Members"].keys():
                        member_stars = local_stars['Guilds'][guild.name]["Members"][member.name]
                        # print(member_stars)
                        newStars['Guilds'][guild.name]["Members"][member.id] = member_stars
                        newStars['Guilds'][guild.name]["Members"][member.id]["Name"] = member.name
                        # newStars['Guilds'][guild.name]["Members"]["ID"]["Name"] =
            print(newStars)
            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(newStars, indent = 4))
            file.close()
            # print(newStars['Guilds'][guild.name]["Members"]["ID"])
            # print(newStars['Guilds'][guild.name]["Members"][name])
        else:
            await ctx.send('Fuck off please')


def setup(client):
    client.add_cog(Stars(client))
