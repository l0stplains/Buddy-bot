import os
import discord
import requests
import json
import random
import copy
from replit import db
from discord import Embed
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix='!', intents=intents)

sad_words = ["sad", "depressed", "sedih", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
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
async def clear(ctx, amount=4):
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

keep_alive()
client.run(os.environ['TOKEN'])