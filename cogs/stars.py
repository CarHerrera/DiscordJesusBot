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

    @tasks.loop(minutes = 1)
    # This loops every 24 hours and resets the servers weekly stars and send a message with who had the highest and lowest stars
    async def reset_weekly_stars(self):
        global last_reset, stars, stars_data
        day = datetime.now().strftime("%A")
        time = datetime.now()
        file = open('./private/server_settings.txt', "r")
        settings = json.loads(file.read())
        file.close()
        for guild in self.client.guilds:
            if settings['Guilds'][guild.name]['Settings']['Stars']['All Stars'] is False or settings['Guilds'][guild.name]['Settings']['Stars']['Weekly Stars'] is False:
                continue
            else:
                sent = stars["Guilds"][guild.name]["Sent"]
            if (day == "Monday" and time.hour == 15) and sent is False:
                number_of_stars = []
                members_list = []
                for member in guild.members:
                    if member.bot is True:
                        continue
                    # Checks if the member has weekly stars then resets it
                    week_stars = stars["Guilds"][guild.name]["Members"][member.name]
                    if week_stars == 0:
                        continue
                    else:
                        number_of_stars.append(stars["Guilds"][guild.name]["Members"][member.name]["Weekly Stars"])
                        members_list.append(member.name)
                        stars["Guilds"][guild.name]["Members"][member.name]["Weekly Stars"] = 0
                if len(number_of_stars) > 0:
                    pref_channel = settings['Guilds'][guild.name]['Settings']['Pref Channel']
                    channel = discord.utils.get(guild.text_channels, name= pref_channel)
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
            voice_state["Guilds"][guild.name] = {"Members":{}}
        try:
            file = open('./settings/stars.txt', "r")
            stars = json.loads(file.read())
            file.close()
            async for guild in self.client.fetch_guilds():
                async for member in guild.fetch_members():
                    if member.bot is True:
                        continue
                    if 'Weekly Stars' not in stars['Guilds'][guild.name]['Members'][member.name].keys():
                        stars["Guilds"][guild.name]["Members"][member.name]['Weekly Stars'] = 0
                    stars["Guilds"][guild.name]["Members"][member.name]['Daily'] = 0
            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(stars, indent = 4))
            file.close()
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
        if datetime.now().hour == 0:
            stars['Guilds'][guild.name]['Members'][name]['Daily'] = 0
        if name in stars["Guilds"][guild.name]["Members"]:
            stars['Guilds'][guild.name]['Members'][name]['Daily'] -= rand_num
            stars['Guilds'][guild.name]['Members'][name]['Weekly Stars'] -= rand_num
            stars['Guilds'][guild.name]['Members'][name]['Stars'] -= rand_num
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
        time = datetime.now()
        if datetime.now().hour == 0:
            stars['Guilds'][guild.name]['Members'][name]['Daily'] = 0
        daily_cap = settings['Guilds'][guild.name]['Settings']['Stars']['Daily Cap']
        if name in stars["Guilds"][guild.name]["Members"]:
            if daily_cap == None:
                stars['Guilds'][guild.name]['Members'][name]['Daily'] += rand_num
                stars['Guilds'][guild.name]['Members'][name]['Weekly Stars'] += rand_num
                stars['Guilds'][guild.name]['Members'][name]['Stars'] += rand_num
            else:
                if stars['Guilds'][guild.name]['Members'][name]['Daily'] >= daily_cap:
                    stars['Guilds'][guild.name]['Members'][name]['Daily'] = daily_cap
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
        rand_num = randint(1, 30)
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
            bad_rand = randint(1, 30)
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
        elif message_count % 500 == 0:
            rand_chance_stars = randint(1000, 6000)
            # spam.send()
            star_update = self.remove(msg.author,-rand_chance_stars, reason =" bc fuck you thats why")
            self.data_gatherer(msg, "Bad RNG", True ,-rand_chance_stars)
        elif count > 8:
            spam_rand = randint(10, 40)
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
            no_trigger = randint(40, 90)
            star_update = self.add_stars(msg.author, no_trigger)
            # await spam.send()
            rules_followed["Guilds"][guild.name]["Members"][msg.author.name] = 0
            self.data_gatherer(msg, "Didn't trigger an if statement", True, no_trigger)
        elif any(word in msg.content.casefold() for word in good_words):
            nice_rand = randint(5,15)
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
        if payload.member == self.client.user:
            return
        elif settings['Guilds'][guild.name]['Settings']['Stars']['All Stars'] is False:
            return
        elif settings['Guilds'][guild.name]['Settings']['Stars']['Emote Stars'] is False:
            return
        # Bonk Emoji
        if payload.emoji.id == 797305732063297536 and msg.author.bot is False:
            # Checks if person who reacted has reacted before
            if payload.member.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[payload.member.name], 5)
                if dif is True:
                    # Removes stars from the person who sent the message
                    star_update = self.remove_stars(msg.author, bonked, reason = f" for being bonked by {payload.member.name}")
                    timer.update({payload.member.name:datetime.now()})
                    self.data_gatherer(msg, "got bonked", False, -bonked)
                else:
                    star_update = self.remove_stars(msg.author, bonked, reason = f" for being bonked by {payload.member.name}")
                    # Adds person to the timer dictionary
                    timer.update({payload.member.name:datetime.now()})
                    self.data_gatherer(msg, "got bonked", False, -bonked)
        # Any other emoji
        else:
            if payload.member.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[payload.member.name], 20)
                if dif:
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
        stars["Guilds"][member.guild.name]["Members"][member.name] = {
        "Stars":0,
        'Weekly Stars' : 0,
        'Daily' : 0,
        }
        file = open('./settings/stars.txt', "w+")
        file.write(json.dumps(stars, indent = 4))
        file.close()
        # print(member.name, sep = " ")
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        stars["Guilds"][member.guild.name]["Members"].pop(member.name)
        file = open('./settings/stars.txt', "w+")
        file.write(json.dumps(stars, indent = 4))
        file.close()

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.bot or after.bot:
            return
        if before.name != after.name:
            async for guild in self.client.fetch_guilds():
                for member in guild.fetch_members():
                    if before.name in stars['Guilds'][guild.name]["Members"].keys():
                        temp_stars = stars['Guilds'][guild.name]["Members"][before.name]["Stars"]
                        stars["Guilds"][member.guild.name]["Members"].pop(before.name)
                        stars["Guilds"][member.guild.name]["Members"][after.name] = {'Stars':temp_stars}
            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(stars, indent = 4))
            file.close()
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
        guild = ctx.message.guild
        if len(ctx.message.mentions) == 1:
            member = ctx.message.mentions[0]
            if member.bot is True:
                return
            member_name = member.name
            if member_name in stars["Guilds"][guild.name]["Members"]:
                user_stars = stars["Guilds"][guild.name]["Members"][member.name]["Stars"]
                daily = stars["Guilds"][guild.name]["Members"][member.name]["Daily"]
                await ctx.send(f'{member_name} has {user_stars} and also got {daily} today')
            else:
                await ctx.send(f'Something went wrong, could not find {member_name} on the good noodle board, maybe they are not on the board?')
        elif len(ctx.message.mentions) > 1:
            await ctx.send("Too many members in the command")
        elif len(ctx.message.mentions) == 0:
            if name in stars["Guilds"][guild.name]["Members"]:
                user_stars = stars["Guilds"][guild.name]["Members"][name]["Stars"]
                daily = stars["Guilds"][guild.name]["Members"][name]["Daily"]
                await ctx.send(f'{name} has {user_stars} and also got {daily} today')
            else:
                await ctx.send(f'Something went wrong, could not find you on the good noodle board, maybe you are not on the board?')




def setup(client):
    client.add_cog(Stars(client))
