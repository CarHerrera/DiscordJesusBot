from datetime import datetime
import discord
from discord.ext import commands, tasks
import aiohttp, aiofiles
import sys
from bs4 import BeautifulSoup
file = open('./settings/hltvlinks.txt')
settings = open('./settings/hltvlinks.txt').read().split()
working_url = settings[0]
partial = "https://www.hltv.org/ranking/teams/"
sent = bool(int(settings[1]))
class Hltv(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.weekly_ranking.start()
    @tasks.loop(minutes = 1.0)
    async def weekly_ranking(self):
        global sent, partial, working_url
        current_time = datetime.now()
        guild = self.client.get_guild(751678259657441339)
        cs_channel = discord.utils.find(lambda c: c.name == 'csgo', guild.channels)
        if current_time.strftime('%A') == 'Monday' and sent is False:
            pot_partial = partial + str(current_time.year) + "/" + current_time.strftime('%B').casefold()+ "/" + str(current_time.day)
            print(pot_partial)
            async with aiohttp.ClientSession() as session:
                async with session.get(pot_partial) as r:
                    if r.status == 200:
                        url = open('./settings/hltvlinks.txt', "w")
                        url.write(pot_partial)
                        url.write("\n1")
                        url.close()
                        data = open('./settings/hltvlinks.txt').read().split()
                        working_url = data[0]
                        sent = bool(int(data[1]))
                        test = discord.Embed(title = "Top 20 teams in the world", type = 'rich')
                        text = await r.text()
                        soup = BeautifulSoup(text, "lxml")
                        rankings = []
                        team = []
                        points = []
                        team_name = []
                        count = 1
                        for tag in soup.find_all("div", "ranking"):
                            for name in tag.find_all("span"):
                                try:
                                    if 'name' in name['class']:
                                        team_name.append(name.string)
                                    elif 'points' in name['class']:
                                        points.append(name.string)
                                    elif "position" in name['class']:
                                        rankings.append(name.string)
                                except:
                                    team.append(name.string)
                            for i in range(0,20):
                                head = rankings[i] + " " + team_name[i] + " " + points[i]
                                pl_index = i*5
                                players = " ".join(team[pl_index:pl_index+5])
                                test.add_field(name = head , value = players, inline = True)
                            else:
                                await cs_channel.send(embed = test)
                                await cs_channel.send(f"Src: {working_url}")
        elif current_time.strftime('%A') != "Monday":
            url = open('./settings/hltvlinks.txt', "w")
            url.write(working_url)
            url.write("\n0")
            url.close()

    @weekly_ranking.before_loop
    async def before_check(self):
        await self.client.wait_until_ready()
    @commands.command()
    async def topten(self, ctx):
        """Returns the top 20 teams of csgo in the world"""
        test = discord.Embed(title = "Top 20 teams in the world", type = 'rich')
        async with aiohttp.ClientSession() as session:
            async with session.get(working_url) as r:
                text = await r.text()
                soup = BeautifulSoup(text, "lxml")
                rankings = []
                team = []
                points = []
                team_name = []
                count = 1
                for tag in soup.find_all("div", "ranking"):
                    for name in tag.find_all("span"):
                        try:
                            if 'name' in name['class']:
                                team_name.append(name.string)
                            elif 'points' in name['class']:
                                points.append(name.string)
                            elif "position" in name['class']:
                                rankings.append(name.string)
                        except:
                            team.append(name.string)
            for i in range(0,20):
                head = rankings[i] + " " + team_name[i] + " " + points[i]
                pl_index = i*5
                players = " ".join(team[pl_index:pl_index+5])
                test.add_field(name = head , value = players, inline = True)
            else:
                await ctx.send(embed = test)
    @commands.command()
    async def games(self,ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.hltv.org/matches?predefinedFilter=top_tier") as r:
                text = await r.text()
                soup = BeautifulSoup(text, "lxml")
                matches = {}
                match = soup.find("div", 'upcomingMatchesSection')
                page = "https://www.hltv.org"
                links = []
                for a in match.find_all('a'):
                    try:
                        if 'a-reset' in a['class']:
                            links.append(page+ a.get('href'))
                    except KeyError:
                        pass
                _list = match.text.splitlines()
                # Removes all the whitespaces in the list
                for i in range(len(_list) - 1, 0, -1):
                    if _list[i] == '':
                        _list.pop(i)
                    else:
                        pass
                games = 1
                for i in range(1, len(_list), 6):
                    time = _list[i].split(':')
                    matches.update({f'Game {games}': {'Time': str(int(time[0]) - 5) + f":{time[1]}",
                    'Format': _list[i + 1],
                    'Teams': f'{_list[i + 2]} vs {_list[i + 3]}',
                    'Event': f'{_list[i + 4]}',
                    'Link' : f'{links[games-1]}'}})
                    games += 1
                game_embed = discord.Embed(title = _list[0])
                for keys in matches:
                    match = matches[keys]['Event'] + " " + matches[keys]['Time']
                    teams = matches[keys]['Teams'] + f"\n{matches[keys]['Link']}"
                    game_embed.add_field(name = match, value = teams, inline = True)
                await ctx.send(embed = game_embed)
def setup(client):
    client.add_cog(Hltv(client))
