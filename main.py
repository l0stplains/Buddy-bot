import os
import discord
import requests
import random
import copy
from replit import db
from discord import Embed
from discord.ext import commands, tasks
from keep_alive import keep_alive
from itertools import cycle

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix='!', intents=intents)

sad_words = ["sad", "depressed", "sedih", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"]

status_all = cycle(['Sleepy', 'Malding', 'Hungry'])

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = response.json()
  quote = f"“{json_data[0]['q']}” -{json_data[0]['a']}"
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index and index >= 0:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")
  channel = client.get_channel(int(os.environ['GENERAL']))
  change_status.start()
  embed = Embed(title="Hello world!", description="I'm online!", colour=0x7CFC00)
  await channel.send(embed=embed)

@client.event
async def on_member_join(member):
  print(f"{member} has joined a server!")
  role = discord.utils.get(member.guild.roles, name='Lv.0')
  await member.add_roles(role)

@client.event
async def on_member_remove(member):
  print(f"{member} has left a server!")

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please pass in all required arguments.")
  elif isinstance(error, commands.CommandNotFound):
    await ctx.send("Invalid command!")
  else:
    print(f"ERROR: {error}\n On {ctx.channel} channel")

@client.event
async def on_message(message):
  author = message.author
  content = message.content

  if author == client.user:
    return

  if db["responding"]:
    options = copy.copy(starter_encouragements)
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

    if any(word in content.lower() for word in sad_words):
      await message.channel.send(f"<@{author.id}>\n{random.choice(options)}")
  
  await client.process_commands(message)

@client.event
async def on_message_delete(message):
  author = message.author
  content = message.content
  channel = message.channel
  channel = client.get_channel(int(os.environ['TEST_BOT']))
  await channel.send(f"{author}: {content}")

@client.command()
async def ping(ctx):
  await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
async def copy_me(ctx,*,args="I can't copy something that didn't exist!"):
  await ctx.send(args)

@client.command()
async def clear(ctx, amount : int):
  if ctx.message.author.guild_permissions.manage_messages:
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"{amount} messages cleared by-<@{ctx.author.id}>.")
  else:
    await ctx.send("Sorry you don't have permission to clear messages.")

@client.command(aliases=['8ball','?'])
async def _8ball(ctx, *, question="Do you think i need to pass in some question for this command?"):
  await ctx.send(f"Question: {question}\nAnswer: {random.choice(db['quest_responses'])}")

@client.command()
async def embed(ctx):
  embed = Embed(title="Hello", description="This is an embed message", colour=0xFF0000)
  await ctx.send(embed=embed)

@client.command(aliases=['hi','HELLO', 'HI'])
async def hello(ctx):
  await ctx.send("Hello there!")

@client.command()
async def list_encourage(ctx):
  encouragements = []
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
  await ctx.send(f"{encouragements}")

@client.command()
async def echo(ctx, *, msg="o0OoO0OoO0oOoo echo nothing"):
  await ctx.send(msg)

@client.command(aliases=['del-encourage'])
async def delete_encourage(ctx, *, args="1000"):
  encouragements = []
  if "encouragements" in db.keys():
    index = int(args.split(" ")[0])
    delete_encouragements(index)
    encouragements = db["encouragements"]
  await ctx.send(f"{encouragements}")

@client.command(aliases=['new-encourage'])
async def new_encourage(ctx, *, args="nothing"):
  if args != 'nothing':
    encouraging_message = args
    update_encouragements(encouraging_message)
    await ctx.send("New encouraging message added.")

@client.command(aliases=['quote','naufal','nopal'])
async def quotes(ctx):
  quote = get_quote()
  await ctx.send(quote)

@client.command()
async def responding(ctx, *, args="nothing"):
  value = args.lower()
  if value == "true" or value == "on":
    db["responding"] = True
    await ctx.send("Responding is on")
  elif value == "false" or value == "off":
    db["responding"] = False
    await ctx.send("Responding is off")
    
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
  if ctx.message.author.guild_permissions.ban_members and ctx.message.author.guild_permissions.kick_members:
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} kicked")
  else:
    await ctx.send("Sorry you don't have permission to do that.")

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
  if ctx.message.author.guild_permissions.ban_members and ctx.message.author.guild_permissions.kick_members:
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")
  else:
    await ctx.send("Sorry you don't have permission to do that.")

@client.command()
async def unban(ctx, *, member):
  if ctx.message.author.guild_permissions.ban_members and ctx.message.author.guild_permissions.kick_members:
    banned_users =  await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
      user = ban_entry.user
      if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"Unbanned {user.mention}")
        return
  else:
    await ctx.send("Sorry you don't have permission to do that.")

@client.command()
async def banned_list(ctx):
  if ctx.channel.id == int(os.environ['BOSS']):
    banned_users = await ctx.guild.bans()
    await ctx.send("Banned users list:")
    user_list = ""
    if banned_users == []: user_list = "Nothing"
    for banned in banned_users:
      user = banned.user
      user_list += f"Name: {user.name}#{user.discriminator}\nUser ID: {user.id}\n\n"
    await ctx.send(user_list)
    
@client.command()
async def load(ctx, extension):
  client.load_extension(f"cogs.{extension}")  

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f"cogs.{extension}") 

@client.command(aliases=['update'])
async def reload(ctx, extension):
  client.unload_extension(f"cogs.{extension}") 
  client.load_extension(f"cogs.{extension}") 

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

@tasks.loop(minutes=1)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status_all)))



keep_alive()
client.run(os.environ['TOKEN'])