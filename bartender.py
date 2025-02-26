import random
import time

import discord.utils
from discord.ext import commands


GUILD_ID = 981968227288633375


def is_guild_member(user):
    guild = bot.get_guild(GUILD_ID)
    return discord.utils.get(guild.members, id=user.id) is not None


def get_joke():
    jokes = []
    with open("jokes", errors="replace") as joke_file:
        raw_jokes = joke_file.read().replace("\r", "").split("\n\n")
    for joke in raw_jokes:
        jokes.append(joke.split("\n"))

    return random.choice(jokes)


with open("key") as _key_file:
    _key = _key_file.read().strip()

intents = discord.Intents(bans=True,
                          guilds=True,
                          invites=True,
                          members=True,
                          messages=True)

greeting = "What can I get ya?"

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'),
                   intents=intents,
                   case_insensitive=True,
                   description=greeting)


@bot.event
async def on_ready():
    print('We have logged in as {0}'.format(bot.user))


@bot.command(name="welcome", hidden=True)
async def test_welcome_message(ctx):
    with open("welcome", errors="replace") as welcome_file:
        welcome = welcome_file.read().format(ctx.message.author.name,
                                             "\n".join(get_joke()))
    if ctx.guild is None:
        await ctx.send(welcome)
    else:
        await ctx.message.delete()
        await ctx.message.author.send(welcome)


@bot.event
async def on_member_join(member):
    member_role = discord.utils.get(member.guild.roles, name="Member")
    await member.add_roles(member_role)
    with open("welcome", errors="replace") as welcome_file:
        welcome = welcome_file.read().format(member.name,
                                             "\n".join(get_joke()))
    await member.send(welcome)


@bot.command(name="joke", brief="Tell a nerdy dad joke")
async def tell_joke(ctx):
    joke = get_joke()
    await ctx.send(joke[0])
    time.sleep(2)
    await ctx.send(joke[1])


@bot.command(name="invite", brief="Create a single-use invite")
async def create_invite(ctx):
    message_lines = [
        "Here's a one time use invite that is valid for 24 hours.",
        "Please only invite people you know and trust.",
        "Invite creation and acceptance are logged."
    ]
    message = "\n".join(message_lines)

    if ctx.guild is None:
        if not is_guild_member(ctx.message.author):
            return
    else:
        await ctx.message.delete()
    guild = bot.get_guild(GUILD_ID)
    reason = "Requested by {}".format(ctx.message.author.name)
    channel = discord.utils.get(guild.channels,
                                name="announcements")
    invite = await channel.create_invite(max_uses=1,
                                         max_age=1440,
                                         reason=reason)
    await ctx.message.author.send("{}\n{}".format(message,
                                                  invite))

bot.run(_key)
