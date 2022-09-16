import os
import discord
from discord.ext import commands

from db import SqliteContext
from parse import GrowthClass, GrowthUnit

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="gr>", intents=intents)

def grab_item(ctx, name, table):
    with SqliteContext() as sq:
        classes = sq.execute(f"SELECT * FROM {table} WHERE id LIKE ?", (f"{str(ctx.author.id)}-{name}%",)).fetchall()
        if len(classes) == 0:
            classes = sq.execute(f"SELECT * FROM {table} WHERE id LIKE ?", (f"%-{name}%",)).fetchall()
        if len(classes) == 0:
            raise ValueError("no classes found")
    found_class = classes[0]
    return found_class

@bot.command()
async def addclass(ctx: commands.Context, hp: int, _str: int, mag: int, dex: int, spd: int, lck: int, _def: int, res: int, *rest):
    if len(rest) == 0:
        raise commands.ArgumentParsingError("rest error")
    if any(x < 0 or x > 100 for x in (hp,_str,mag,dex,spd,lck,_def,res)):
        raise ValueError("range error")
        
    class_name = f"{ctx.author.id}-{' '.join(rest)}"
    if ":" in class_name:
        raise commands.ArgumentParsingError("rest error")

    with SqliteContext() as sq:
        sq.execute("INSERT OR REPLACE INTO Classes (id,hp,str,mag,dex,spd,lck,def,res) VALUES (?,?,?,?,?,?,?,?,?)", (class_name,hp,_str,mag,dex,spd,lck,_def,res))

    await ctx.message.add_reaction(U"✅")


@addclass.error
async def addclass_error(ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, ValueError): # conversion fail
        await ctx.send("The first eight arguments must be integers from 0 to 100!")
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send("You must supply a name for your new class!")
    else:
        await ctx.send(f"An unknown error occured....um ```{error}```")

@bot.command()
async def addunit(ctx: commands.Context, hp: int, _str: int, mag: int, dex: int, spd: int, lck: int, _def: int, res: int, *rest):
    if len(rest) == 0:
        raise commands.ArgumentParsingError("rest error")
    if any(x < 0 or x > 100 for x in (hp,_str,mag,dex,spd,lck,_def,res)):
        raise ValueError("range error")

    combo = " ".join(rest)
    if ":" not in combo:
        raise commands.ArgumentParsingError("bad input")
    char_name, class_name = combo.split(": ",1)
    char_name = f"{ctx.author.id}-{char_name}"

    class_check = grab_item(ctx, class_name, "Classes")

    with SqliteContext() as sq:
        sq.execute("INSERT OR REPLACE INTO Units (id,class,hp,str,mag,dex,spd,lck,def,res) VALUES (?,?,?,?,?,?,?,?,?,?)", (char_name,class_name,hp,_str,mag,dex,spd,lck,_def,res))

    await ctx.message.add_reaction(U"✅")

@addunit.error
async def addunit_error(ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, ValueError): # conversion fail
        await ctx.send("The first eight arguments must be integers from 0 to 100!")
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send("You must supply both a name and class for your unit, separated by a colon (:)!")
    else:
        await ctx.send(f"An unknown error occured....um ```{error}```")

@bot.command()
async def simulate(ctx, level: int, *, unit):
    if level < 1:
        raise ValueError("range error")
    unit = GrowthUnit(*grab_item(ctx, unit, "Units"))
    cl = GrowthClass(*grab_item(ctx, unit._class, "Classes"))
    for _ in range(level-1):
        unit.level_up(cl)
    await ctx.send(embed=unit.embed)

@simulate.error
async def simulate_error(ctx, error):
    await ctx.send("You can't simulate a level below 1!")


@bot.command()
async def classes(ctx, *, member: discord.Member = None):
    member = member if not member is None else ctx.author
    with SqliteContext() as sq:
        mems = sq.execute("SELECT * FROM Classes WHERE id LIKE ?", (f"{str(member.id)}%",)).fetchall()
    await ctx.send([str(GrowthClass(*x)) for x in mems])


@bot.command()
async def classinfo(ctx, *, name):
    await ctx.send(embed=GrowthClass(*grab_item(ctx, name, "Classes")).embed)

@classinfo.error
async def classinfo_error(ctx, error):
    await ctx.send("I couldn't find any classes by that name!")
        

@bot.command()
async def report(ctx):
    with SqliteContext(True) as sq:
        sq.execute("SELECT * FROM Classes")
        await ctx.send(sq.fetchall())
        sq.execute("SELECT * FROM Units")
        await ctx.send(sq.fetchall())

bot.run(os.environ.get("DISCORD_TOKEN"))