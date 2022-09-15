import os
import discord
from discord.ext import commands

from db import SqliteContext

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="gr>", intents=intents)

@bot.command()
async def simulate(ctx):
    await ctx.send("Hello, world!")

@bot.command()
async def addclass(ctx, hp: int, _str: int, mag: int, dex: int, spd: int, lck: int, _def: int, res: int, *rest):
    if len(rest) == 0:
        raise commands.ArgumentParsingError("rest error")
    if any(x < 0 or x > 100 for x in (hp,_str,mag,dex,spd,lck,_def,res)):
        raise ValueError("range error")
        
    class_name = f"{ctx.author.id}-{' '.join(rest)}"
    # TODO: populate the database with the new class values

    await ctx.send(class_name)

@addclass.error
async def addclass_error(ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, ValueError): # conversion fail
        await ctx.send("The first eight arguments must be integers from 0 to 100!")
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send("You must supply a name for your new class!")
    else:
        await ctx.send("An unknown error occured....um")

@bot.command()
async def report(ctx):
    with SqliteContext(True) as sq:
        sq.execute("SELECT * FROM Classes")
        await ctx.send(sq.fetchall())

bot.run(os.environ.get("DISCORD_TOKEN"))