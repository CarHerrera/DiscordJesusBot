import discord
from discord.ext import commands
from datetime import datetime
from random import seed
from random import randint
class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self,ctx):
        # print(ctx)
        """Test command that only says 'Hello World!'"""
        await ctx.send('Hello world!')
    @commands.command()
    async def choose(self,ctx, *args):
        """Chooses an option out of those provided"""
        rand_num = randint(0, len(args) -1)
        await ctx.send('Hmmmmmmm, I choose {}'.format(args[rand_num]))
    @commands.command()
    async def flip(self, ctx):
        """This command flips a coin"""
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
def setup(client):
    client.add_cog(Commands(client))
