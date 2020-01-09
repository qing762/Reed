import discord
import os
import datetime
import asyncio
import itertools
import copy
import unicodedata
import inspect
from collections import Counter, deque, OrderedDict
from discord.ext import commands, tasks
from itertools import cycle

TOKEN = ''

client = commands.Bot(command_prefix = '^')
status = cycle(['Im stupid', 'Prefix is not working in other servers', 'Please wait']) 

@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.dnd)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command are used. Please try again')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms.')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(aliases=['purge', 'delete'])
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount +1)
    await ctx.send(f'Successfully purged {amount} messages.')
    await asyncio.sleep(3.0)
    await ctx.channel.purge(limit=1)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please give an amount messages to be cleared')

@client.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member  : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Successfully kicked {member.mention}.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please give a user to be kicked')

@client.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member  : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Successfully banned {member.mention}.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please give a user to be banned')

@client.command(aliases=['ub'])
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users: 
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Successfully unbanned {user.mention}.')
            return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please give a user to be unbanned')

@client.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Successfully loaded {extension}.')

@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please select a category to be loaded')

@client.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Successfully unloaded {extension}.')

@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please select a category to be unloaded')

@client.command()
@commands.has_permissions(administrator = True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Successfully reloaded {extension}.')

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please select a category to be reloaded')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

def is_it_me(ctx):
    return ctx.author.id == 635765555277725696

@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'Hi. I am {ctx.author}.')

@client.command()
async def join(ctx):
    await ctx.send('https://discordapp.com/oauth2/authorize?client_id=637534965529182218&scope=bot&permissions=268823638')

@client.command()
async def invite(ctx):
    await ctx.send('https://discord.gg/mqcJygz')

@client.command()
async def guess(ctx):
        await ctx.send('Guess a number between 1 and 10.')

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            guess = await client.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.send('Sorry, you took too long it was {}.'.format(answer))

        if int(guess.content) == answer:
            await ctx.send('You are right!')
        else:
            await ctx.send('Oops. You are wrong. It is actually {}.'.format(answer))

@client.command(aliases=['edit'])
async def editme(ctx):
    msg = await ctx.send('This is you')
    await asyncio.sleep(3.0)
    await msg.edit (content='This is me')

@client.command(aliases=['del'])
async def deleteme(ctx):
        await ctx.send('Say goodbye to this message within 10 seconds.', delete_after=10.0)

@client.group()
async def cool(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    await ctx.send('Yes, the bot is cool.')

@client.command()
async def say(ctx, *, message):
    await ctx.send(f"{ctx.author} wants to say : {message}")
    
@client.command(aliases=['cs'])
async def client_secret(ctx):
    await ctx.send('https://media.discordapp.net/attachments/381963689470984203/514834919021740076/no_client_secret.jpg\nOriginal picture by @R.Danny#6348')

client.run(TOKEN)