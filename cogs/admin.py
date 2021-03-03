import discord
import json
from discord.ext import commands
file = open("./settings/good_noodle.txt")
data = file.read()
stars = json.loads(data)
file.close()
class Admin(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def stars(self, ctx):
        global stars
        author = ctx.author
        permission = False
        print(author)
        # for roles in author.roles:
        #     if "Mod" in roles.name or "Owner" in roles.name:
        #         permission = True
        # if permission is False:
        #     ctx.send("User does not have the role to execute command")
        #     return
        if len(ctx.message.mentions) == 1:
            member = ctx.message.mentions[0]
            name = member.name
            nick = member.nick
            for index in range(len(stars["Members"])):
                if name in stars["Members"][index]:
                    await ctx.send("{} has {} good noodle stars".format(nick, stars["Members"][index]["Stars"]))
                    return
                elif author.id in stars["Members"][index]:
                    await ctx.send("{} has {} good noodle stars".format(nick, stars["Members"][index]["Stars"]))
                    return
            else:
                await ctx.send("Could not find you on the good noodle star board.")
                return
        elif len(ctx.message.mentions) > 1:
            await ctx.send("Too many members in the command")
        elif len(ctx.message.mentions) == 0:
            await ctx.send("You have to mention someone to see their good noodle stars")

    @commands.command()
    async def add(self,ctx, *args):
        global stars
        author = ctx.author
        added_stars = 1
        if len(args) == 2:
            try:
                added_stars = int(args[1])
            except:
                added_stars = 1
        else:
            added_stars = 1
        for roles in author.roles:
            if "Mod" in roles.name or "Owner" in roles.name:
                permission = True
        if permission is False:
            await ctx.send("User does not have the role to execute command")
            return
        if len(ctx.message.mentions) == 1:
            member = ctx.message.mentions[0]
            name = member.nick
            for index in range(len(stars["Members"])):
                if name in stars["Members"][index]:
                    new_stars = stars["Members"][index]["Stars"] + added_stars
                    stars["Members"][index].update({"Stars": new_stars})
                    file = open("./settings/good_noodle.txt", "w")
                    file.write(json.dumps(stars))
                    file.close()
                    await ctx.send("{} now has {} good noodle stars".format(nick, stars["Members"][index]["Stars"]))
                    return
                elif author.id in stars["Members"][index]:
                    new_stars = stars["Members"][index]["Stars"] + added_stars
                    stars["Members"][index].update({"Stars": new_stars})
                    file = open("./settings/good_noodle.txt", "w")
                    file.write(json.dumps(stars))
                    file.close()
                    await ctx.send("{} has {} now has good noodle stars".format(nick, stars["Members"][index]["Stars"]))
                    return
            else:
                await ctx.send("{} does not have the permissions to execute command".format(ctx.author.nick))
                return
        elif len(ctx.message.mentions) > 1:
            await ctx.send("Too many members in the command")
        elif len(ctx.message.mentions) == 0:
            await ctx.send("You have to mention someone to see their good noodle stars")
    @commands.command()
    async def remove(self,ctx, *args):
        global stars
        author = ctx.author
        added_stars = 1
        print(type(-1))
        print(args)
        if len(args) == 2:
            try:
                added_stars = int(args[1])
            except:
                added_stars = 1
        else:
            added_stars = 1
        permission = False
        for roles in author.roles:
            if "Mod" in roles.name or "Owner" in roles.name:
                permission = True
        if permission is False:
            await ctx.send("{} does not have the permissions to execute command".format(ctx.author.nick))
            return
        if len(ctx.message.mentions) == 1:
            member = ctx.message.mentions[0]
            name = member.nick
            for index in range(len(stars["Members"])):
                if name in stars["Members"][index]:
                    new_stars = stars["Members"][index]["Stars"] - added_stars
                    stars["Members"][index].update({"Stars": new_stars})
                    file = open("./settings/good_noodle.txt", "w")
                    file.write(json.dumps(stars))
                    file.close()
                    await ctx.send("{} now has {} good noodle stars".format(nick, stars["Members"][index]["Stars"]))
                    return
                elif author.id in stars["Members"][index]:
                    new_stars = stars["Members"][index]["Stars"] - added_stars
                    stars["Members"][index].update({"Stars": new_stars})
                    file = open("./settings/good_noodle.txt", "w")
                    file.write(json.dumps(stars))
                    file.close()
                    await ctx.send("{} has {} now has good noodle stars".format(nick, stars["Members"][index]["Stars"]))
                    return
            else:
                await ctx.send("Could not find you on the good noodle star board.")
                return
        elif len(ctx.message.mentions) > 1:
            await ctx.send("Too many members in the command")
        elif len(ctx.message.mentions) == 0:
            await ctx.send("You have to mention someone to see their good noodle stars")
def setup(client):
    client.add_cog(Admin(client))
