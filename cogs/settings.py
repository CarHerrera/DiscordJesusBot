import discord
from discord.ext import tasks, commands
from datetime import datetime
import json
class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.settings = dict()

    def check_for_owner_of_bot(self, ctx):
        return ctx.message.author.id == 263054069885566977

    def check_if_mod(self, ctx):
        return ctx.message.author.guild_permissions.administrator

    @commands.Cog.listener()
    async def on_connect(self):
        await self.client.wait_until_ready()
        try:
            print('Opening already existed setting file')
            file = open("./private/server_settings.txt","r")
            self.settings = json.loads(file.read())
            file.close()
        except Exception:
            print(f'{datetime.now()}: In Exception')
            self.settings.update({"Guilds":{}})
            for guild in self.client.guilds:
                self.settings["Guilds"][guild.name] = {"Settings":{}}
                if guild.id == 751678259657441339:
                    self.settings["Guilds"][guild.name]["Settings"]["Pref Channel"] = 'bot-spam'
                else:
                    self.settings["Guilds"][guild.name]["Settings"]["Pref Channel"] = None
                    system_channel = guild.system_channel
                    await system_channel.send('Hello! You\'re preferred channel is not set. Make sure you set this with "%change pref_channel {channel_name}" to set it')
                self.settings["Guilds"][guild.name]["Settings"]["Stars"] = {
                    'All Stars': True,
                    'Weekly Stars' : True,
                    'Mod Checks' : True,
                    'Emote Stars': True,
                    'MSG Stars': True,
                    'VC Stars':True,
                    'Daily Cap': None,
                    'Star Updates': True
                }
            file = open("./private/server_settings.txt", "w+")
            file.write(json.dumps(self.settings, indent = 4))
            file.close()
            print('Created bot settings file')
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.name != after.name:
            stars["Guilds"][after.name] = stars["Guilds"][before.name]
            del stars["Guilds"][before.name]
            file = open('./settings/stars.txt', "w+")
            file.write(json.dumps(stars, indent = 4))
            file.close()

    @commands.group(invoke_without_command = True)
    async def change(self, ctx, *args):
        if self.check_if_mod(ctx):
            prefix = ctx.prefix + 'change'
            mod_changes = discord.Embed(title = 'Discord Jesus Bot General Settings')
            mod_changes.set_thumbnail(url = 'https://i.imgur.com/GbDdMj2.png')
            mod_changes.add_field(name = 'Bot Settings', value = 'All commands that allow you to modify bot')
            mod_changes.add_field(name = f'{prefix} pref_channel', value = 'Changes where the bot sends alll the star messages')
            mod_changes.add_field(name = f'{prefix} weekly_msg', value = 'Enables/Disables the weekly star ranking message')
            mod_changes.add_field(name = f'{prefix} daily_cap', value = 'Makes the bot cap the number of stars one can get in a day.')
            mod_changes.add_field(name = f'{prefix} reaction', value = 'Enables/Disables getting stars from reactions')
            mod_changes.add_field(name = f'{prefix} msg_stars', value = 'Enables/Disables getting stars from messages')
            mod_changes.add_field(name = f'{prefix} updates', value = 'Enables/Disables sending messages whenever someone gets stars')
            mod_changes.add_field(name = "Notes", value = 'Will be adding/removing features as I come up with more ideas')
            await ctx.send(embed = mod_changes)
        else:
            await ctx.send('You do not have the permissions to use this command')

    @change.command(name = 'pref_channel')
    async def change_channel(self, ctx, *args):
        """Changes the preferred channel via text commands"""
        if self.check_if_mod(ctx):
            channels = ctx.guild.text_channels
            names = [chan.name for chan in channels]
            if len(args) != 1:
                await ctx.send('Too many/too little arguments')
            else:
                if args[0] in names:
                    self.settings['Guilds'][ctx.guild.name]["Settings"]["Pref Channel"] = args[0]
                    pref_channel = discord.utils.get(ctx.guild.text_channels, name=args[0])
                    await pref_channel.send(f'{args[0]} is now the preferred messaging channel')
                    file = open("./private/server_settings.txt", "w+")
                    file.write(json.dumps(self.settings, indent = 4))
                    file.close()
        else:
            await ctx.send('You do not have the permissions to use this command')

    @change.command(name ='weekly_msg')
    async def change_stars(self, ctx, *args):
        if self.check_if_mod(ctx):
            guild = ctx.guild
            if 'weekly' in args[0]:
                if "on" in args[1] :
                    self.settings["Guilds"][guild.name]['Settings']['Stars']['Weekly Stars'] = True
                    await ctx.send('Weekly Stars are now enabled')
                elif "off" in args[1]:
                    self.settings["Guilds"][guild.name]['Settings']['Stars']['Weekly Stars'] = False
                    await ctx.send('Weekly Stars are no longer enabled')
                else:
                    await ctx.send('Input not recognized, settings remain unchanged')
            file = open("./private/server_settings.txt", "w+")
            file.write(json.dumps(self.settings, indent = 4))
            file.close()
        else:
            await ctx.send('You do not have the permissions to use this command')

    @change.command(name = 'daily_cap')
    async def change_daily_cap(self, ctx, *args):
        if self.check_if_mod(ctx):
            guild = ctx.guild
            if len(args) == 0:
                limit = self.settings['Guilds'][guild.name]['Settings']["Stars"]['Daily Cap']
                if limit == 0:
                    await ctx.send('There is currently no limit on how many stars one can get in one day')
                else:
                    await ctx.send(f'One can only get {limit} numbers of stars daily')
            else:
                if len(args) == 1:
                    try:
                        cap = int(args[0])
                        if cap < 0:
                            await ctx.send(f'Daily limit cannot be negative')
                            return
                        elif cap == 0:
                            self.settings['Guilds'][guild.name]['Settings']["Stars"]['Daily Cap'] = None
                            await ctx.send(f'Daily limit is now unlimited')
                        else:
                            self.settings['Guilds'][guild.name]['Settings']["Stars"]['Daily Cap'] = cap
                            await ctx.send(f'Daily limit is now set at {cap}')
                        file = open("./private/server_settings.txt", "w+")
                        file.write(json.dumps(self.settings, indent = 4))
                        file.close()
                    except:
                        await ctx.send(f'A number was not entered')
                else:
                    await ctx.send(f'Too many arguments')
            print(args)

    @change.command(name = 'reaction')
    async def reactions(self, ctx, *args):
        if self.check_if_mod(ctx):
            guild = ctx.guild
            if len(args) == 1:
                if 'on' == args[0]:
                    self.settings['Guilds'][guild.name]['Settings']["Stars"]['Emote Stars'] = True
                    await ctx.send('Stars from reactions are now enabled')
                elif 'off' == args[0]:
                    self.settings['Guilds'][guild.name]['Settings']["Stars"]['Emote Stars'] = False
                    await ctx.send('Stars from reactions are no longer enabled')
                else:
                    await ctx.send('Neither on or off was entered')
                file = open("./private/server_settings.txt", "w+")
                file.write(json.dumps(self.settings, indent = 4))
                file.close()
            else:
                await ctx.send('Too many or too little arguments were entered')
        else:
            await ctx.send('Only administrators are allowed to use this command')

    @change.command(name = 'msg_stars')
    async def msg_stars(self, ctx, *args):
        if self.check_if_mod(ctx):
            guild = ctx.guild
            if len(args) == 1:
                if 'on' == args[0]:
                    self.settings['Guilds'][guild.name]['Settings']["Stars"]['MSG Stars'] = True
                    await ctx.send('Stars from messaging are now enabled')
                elif 'off' == args[0]:
                    self.settings['Guilds'][guild.name]['Settings']["Stars"]['MSG Stars'] = False
                    await ctx.send('Stars from messaging are no longer enabled')
                else:
                    await ctx.send('Neither on or off was entered')
                file = open("./private/server_settings.txt", "w+")
                file.write(json.dumps(self.settings, indent = 4))
                file.close()
            else:
                await ctx.send('Too many or too little arguments were entered')
        else:
            await ctx.send('Only administrators are allowed to use this command')

    @change.command(name = 'updates')
    async def updates(self,ctx,*args):
        if self.check_if_mod(ctx):
            guild = ctx.guild
            if len(args) == 1:
                if 'on' == args[0]:
                    self.settings['Guilds'][guild.name]['Settings']["Stars"]['Star Updates'] = True
                    await ctx.send('Stars from messaging are now enabled')
                elif 'off' == args[0]:
                    self.settings['Guilds'][guild.name]['Settings']["Stars"]['Star Updates'] = False
                    await ctx.send('Stars from messaging are no longer enabled')
                else:
                    await ctx.send('Neither on or off was entered')
                file = open("./private/server_settings.txt", "w+")
                file.write(json.dumps(self.settings, indent = 4))
                file.close()
            else:
                await ctx.send('Too many or too little arguments were entered')
        else:
            await ctx.send('Only administrators are allowed to use this command')
    # @change.command(name = 'mod_checks')
    # async def checks_and_balances(self, ctx, *args):
    #     if self.check_if_mod(ctx):
    #         guild = ctx.guild
    #         if len(args) == 1:
    #             if 'on' == args[0]:
    #                 self.settings['Guilds'][guild.name]['Settings']["Stars"]['Mod Checks'] = True
    #                 await ctx.send('Stars from deafening/muting are now enabled')
    #             elif 'off' == args[0]:
    #                 self.settings['Guilds'][guild.name]['Settings']["Stars"]['Mod Checks'] = False
    #                 await ctx.send('Stars from deafening/muting are no longer enabled')
    #             else:
    #                 await ctx.send('Neither on or off was entered')
    #             file = open("./private/server_settings.txt", "w+")
    #             file.write(json.dumps(self.settings, indent = 4))
    #             file.close()
    #         else:
    #             await ctx.send('Too many or too little arguments were entered')
    #     else:
    #         await ctx.send('Only administrators are allowed to use this command')
    @commands.command()
    async def add(self, ctx, *args):
        if self.check_for_owner_of_bot(ctx):
            if "stars" in ctx.message.content.casefold():
                for guild in self.client.guilds:
                    self.settings['Guilds'][guild.name]['Settings']['Stars'][args[1]] = bool(args[2])
            else:
                for guild in self.client.guilds:
                    self.settings['Guilds'][guild.name]['Settings'][args[0]] = bool(args[1])
            file = open("./private/server_settings.txt", "w+")
            file.write(json.dumps(self.settings, indent = 4))
            file.close()
        else:
            print('Not an Owner')

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """In case the Administrators of the guilds update the name, settings will change as well"""
        if before.name != after.name:
            self.settings["Guilds"][after.name] = self.settings['Guilds'][before.name]
            del self.settings['Guilds'][before.name]
            file = open("./private/server_settings.txt", "w+")
            file.write(json.dumps(self.settings, indent = 4))
            file.close()

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        """Appends the server that it just joined into the settings file"""
        self.settings["Guilds"][guild.name] = {"Settings":{}}
        self.settings["Guilds"][guild.name]["Settings"]["Pref Channel"] = None
        system_channel = guild.system_channel
        await system_channel.send('Hello! You\'re preferred channel is not set. Make sure you set this with "%change pref_channel {channel_name}" to set it')
        self.settings["Guilds"][guild.name]["Settings"]["Stars"] = {
            'All Stars': True,
            'Weekly Stars' : True,
            'Mod Checks' : True,
            'Emote Stars': True,
            'MSG Stars': True,
            'VC Stars':True,
            'Daily Cap': None
        }
        file = open("./private/server_settings.txt", "w+")
        file.write(json.dumps(self.settings, indent = 4))
        file.close()

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        """Removes the guild it was removed from from the settings file."""
        del self.settings['Guilds'][guild.name]
        file = open("./private/server_settings.txt", "w+")
        file.write(json.dumps(self.settings, indent = 4))
        file.close()

    @commands.Cog.listener()
    async def on_guild_channel_delete(self,channel):
        print('In listner')
        print(channel.name)
        guild = channel.guild
        if self.settings['Guilds'][guild.name]['Settings']['Pref Channel'] == channel.name:
            self.settings['Guilds'][guild.name]['Settings']['Pref Channel'] = None
            system_channel = guild.system_channel
            await system_channel.send('Hello! You\'re preferred channel is not set. Make sure you set this with "%change pref_channel {channel_name}" to set it')
            file = open("./private/server_settings.txt", "w+")
            file.write(json.dumps(self.settings, indent = 4))
            file.close()

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if type(before) == discord.TextChannel:
            print(f'Before {before.name}, after: {after.name}')
            self.settings['Guilds'][before.guild.name]['Settings']['Pref Channel'] = after.name
            file = open("./private/server_settings.txt", "w+")
            file.write(json.dumps(self.settings, indent = 4))
            file.close()
def setup(client):
    client.add_cog(Settings(client))
