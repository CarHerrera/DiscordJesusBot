import discord
import json
from random import randint
from discord.ext import commands
from datetime import datetime
from main import timeChecker
file = open("./settings/good_noodle.txt")
data = file.read()
stars = json.loads(data)
file.close()
file = open("./private/swearWords.txt")
bad_words = file.read().split()
file.close()
timer = {}
class Admin(commands.Cog):
    def __init__(self,client):
        self.client = client
    def remove_stars(self, user, rand_num):
        """This function removes stars"""
        global stars
        member = user
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
                current_stars=stars["Guilds"][GuildIndex]["Members"][index]["Stars"]
                stars["Guilds"][GuildIndex]["Members"][index]["Stars"] = current_stars - rand_num
        file = open("./settings/good_noodle.txt", "w")
        file.write(json.dumps(stars, indent = 4))
        file.close()
    def add_stars(self, user, message, rand_num):
        """This function adds stars"""
        global stars
        member = user
        name = member.name
        guild = message.guild
        working_stars = None
        GuildIndex = None
        for index in range(len(stars["Guilds"])):
            if guild.name in stars["Guilds"][index]:
                GuildIndex = index
        for index in range(len(stars["Guilds"][GuildIndex]["Members"])):
            if name in stars["Guilds"][GuildIndex]["Members"][index]:
                current_stars=stars["Guilds"][GuildIndex]["Members"][index]["Stars"]
                stars["Guilds"][GuildIndex]["Members"][index]["Stars"] = current_stars + rand_num
        file = open("./settings/good_noodle.txt", "w")
        file.write(json.dumps(stars, indent = 4))
        file.close()
    @commands.Cog.listener('on_message')
    async def star_message(self, msg):
        if msg.author == self.client.user:
            return
        elif msg.author.bot == True:
            return
        rand_num = randint(1, 30)
        channel = msg.channel
        count = 1
        async for message in channel.history(limit = 5):
            if message.author == msg.author:
                count+= 1
        if any(word in msg.content.casefold() for word in bad_words):
            await msg.channel.send(f"{msg.author.mention} loses {rand_num} good noodle star(s)")
            self.remove_stars(msg.author, rand_num)
            return
        elif len(msg.content) > 150:
            await msg.channel.send(f"{msg.author.mention} loses {rand_num} good noodle star(s) for sending a message thats too long to read.")
            self.remove_stars(msg.author, rand_num)
            return
        elif msg.content.isupper():
            await msg.channel.send(f"{msg.author.mention} loses {rand_num} good noodle star(s) for being aggressive")
            self.remove_stars(msg.author, rand_num)
            return
        elif count > 3:
            await msg.channel.send(f"{msg.author.mention} loses {rand_num} good noodle star(s) being a dickhead")
            self.remove_stars(msg.author, rand_num)
            return
        elif message.channel.id == 751679824942202960 and len(message.attachments) > 0:
            await msg.channel.send(f"{msg.author.mention} loses {rand_num} good noodle star(s) for whatever that thing is.")
            self.remove_stars(msg.author, rand_num)
            return
        elif "bot" in msg.content.casefold() and "poppin" in msg.content.casefold():
            await msg.channel.send(f"{msg.author.mention} gets {rand_num} good noodle stars. Thanks bb")
            self.add_stars(msg.author, rand_num)
    @commands.Cog.listener('on_raw_reaction_add')
    async def check_reaction(self, payload):
        global stars
        channel = await self.client.fetch_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        rand_num = randint(1, 30)
        if payload.member == self.client.user:
            return
        if payload.emoji.id == 797305732063297536:
            if payload.member.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[payload.member.name], 5)
                if dif is True:
                    await channel.send(f"{msg.author.mention} loses {rand_num} good noodle star(s)")
                    self.remove_stars(msg.author, rand_num)
                    timer.update({payload.member.name:datetime.now()})
                    return
            else:
                await channel.send(f"{msg.author.mention} loses {rand_num} good noodle star(s)")
                self.remove_stars(msg.author, rand_num)
                timer.update({payload.member.name:datetime.now()})
                return
        else:
            if payload.member.name in timer.keys():
                dif = timeChecker(datetime.now(), timer[payload.member.name], 5)
                if dif:
                    await channel.send(f"{msg.author.mention} gets {rand_num} good noodle star(s) for emoting")
                    self.add_stars(msg.author, msg, rand_num)
                    timer.update({payload.member.name:datetime.now()})
                    print(timer)
                    return
            else:
                await channel.send(f"{msg.author.mention} gets {rand_num} good noodle star(s) for emoting")
                self.add_stars(msg.author, msg, rand_num)
                timer.update({payload.member.name:datetime.now()})
                print(timer)
                return
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = self.client.get_guild(member.guild.id)
        channel = guild.system_channel
        # print(after.deaf)
        # print(after.mute)
        rand_num = randint(1, 15)
        audit_logs = guild.audit_logs(limit = 5)
        if after.deaf or after.mute:
            counter = 1
            async for thing in audit_logs:
                if thing.action == discord.AuditLogAction.member_update:
                    await channel.send(f"{thing.user} loses {rand_num} good noodle star(s) for muting/deafining {member.name}")
                    self.remove_stars(thing.user, rand_num)
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
                if name in working_stars["Members"][_]:
                    await ctx.send("{} has {} good noodle stars".format(member_name, working_stars["Members"][_]["Stars"]))
                    return
                elif author.id in working_stars["Members"][_].values():
                    await ctx.send("{} has {} good noodle stars".format(member_name, working_stars["Members"][_]["Stars"]))
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
                    return
                elif author.id in working_stars["Members"][_].values():
                    await ctx.send("{} has {} good noodle stars".format(name, working_stars["Members"][_]["Stars"]))
                    return
            else:
                await ctx.send(f'Something went wrong, could not find you on the good noodle board, maybe you are not on the board?')
    @commands.command()
    async def reset(self,ctx):
        if ctx.author.id == 263054069885566977:
            global stars
            member= ctx.mssage.mentions[0]
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
                    current_stars=stars["Guilds"][GuildIndex]["Members"][index]["Stars"]
                    stars["Guilds"][GuildIndex]["Members"][index]["Stars"] = 0
            file = open("./settings/good_noodle.txt", "w")
            file.write(json.dumps(stars, indent = 4))
            file.close()
    # @commands.command()
    # async def add(self,ctx, *args):
    #     global stars
    #     author = ctx.author
    #     added_stars = 1
    #     if len(args) == 2:
    #         try:
    #             added_stars = int(args[1])
    #         except:
    #             added_stars = 1
    #     else:
    #         added_stars = 1
    #     for roles in author.roles:
    #         if "Mod" in roles.name or "Owner" in roles.name:
    #             permission = True
    #     if permission is False:
    #         ctx.send("User does not have the role to execute command")
    #         return
    #     if len(ctx.message.mentions) == 1:
    #         member = ctx.message.mentions[0]
    #         name = member.name
    #         for _ in range(len(stars["Members"])):
    #             if name in stars["Members"][_]:
    #                 new_stars = stars["Members"][_]["Stars"] + added_stars
    #                 stars["Members"][_].update({"Stars": new_stars})
    #                 file = open("./settings/good_noodle.txt", "w")
    #                 file.write(json.dumps(stars))
    #                 file.close()
    #                 await ctx.send("{} now has {} good noodle stars".format(name, stars["Members"][_]["Stars"]))
    #                 return
    #             elif author.id in stars["Members"][_]:
    #                 new_stars = stars["Members"][_]["Stars"] + added_stars
    #                 stars["Members"][_].update({"Stars": new_stars})
    #                 file = open("./settings/good_noodle.txt", "w")
    #                 file.write(json.dumps(stars))
    #                 file.close()
    #                 await ctx.send("{} has {} now has good noodle stars".format(name, stars["Members"][_]["Stars"]))
    #                 return
    #         else:
    #             await ctx.send("Could not find you on the good noodle star board.")
    #             return
    #     elif len(ctx.message.mentions) > 1:
    #         await ctx.send("Too many members in the command")
    #     elif len(ctx.message.mentions) == 0:
    #         await ctx.send("You have to mention someone to see their good noodle stars")


def setup(client):
    client.add_cog(Admin(client))
