import os
import discord
import random
from replit import db
from discord import Embed
from discord.ext import commands, tasks
from keep_alive import keep_alive
from itertools import cycle

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix='!', intents=intents)

if "responding" not in db.keys():
  db["responding"] = True

status_all = cycle(['You', 'Your future', 'Darkness'])

@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")
  channel = client.get_channel(int(os.environ['GENERAL']))
  change_status.start()
  embed = Embed(title="Hello world!", description="I'm online!", colour=0x7CFC00)
  await channel.send(embed=embed)

@client.event
async def on_message(message):
  author = message.author
  content = message.content

  if author == client.user:
    return

  if db["responding"]:
    if any(word in content.lower() for word in db['sad_words']):
      await message.channel.send(f"<@{author.id}>\n{random.choice(db['encouragements'])}")
  
  await client.process_commands(message)

@client.event
async def on_message_delete(message):
  author = message.author
  content = message.content
  channel = message.channel
  channel = client.get_channel(int(os.environ['TEST_BOT']))
  await channel.send(f"{author}: {content}")

@client.command()
async def responding(ctx, *, args="nothing"):
  value = args.lower()
  if value == "true" or value == "on":
    db["responding"] = True
    await ctx.send("Responding is on")
  elif value == "false" or value == "off":
    db["responding"] = False
    await ctx.send("Responding is off")

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please pass in all required arguments.")
  elif isinstance(error, commands.CommandNotFound):
    await ctx.send("Invalid command!")
  elif isinstance(error, commands.ExtensionAlreadyLoaded):
    print("ExtensionAlreadyLoaded")
  else:
    print(f"ERROR: {error}\n On {ctx.channel} channel")
    
@client.command()
async def load(ctx, extension):
  extension = extension.lower()
  client.load_extension(f"cogs.{extension}")  

@client.command()
async def unload(ctx, extension):
  extension = extension.lower()
  client.unload_extension(f"cogs.{extension}") 

@client.command(brief='extension(feature) update', aliases=['reload'])
async def update(ctx, extension):
  extension = extension.lower()
  if extension == 'server':
    for file in db['COGS']:
      _reload(ctx, file)
  else:
      _reload(ctx, extension)

@client.command(brief='list of extensions', aliases=['extensions_list'])
async def extension_list(ctx):
  info = ''
  for ext in db['COGS']:
    info += (ext) + '\n'
  embed = Embed(title='Extensions list:', description=info, colour=0x0000FF)
  embed.set_footer(text="type !help for more information")
  await ctx.send(embed=embed)

def _reload(ctx, extension):
  extension = extension.lower()
  client.unload_extension(f"cogs.{extension}") 
  client.load_extension(f"cogs.{extension}")

files = []
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    files.append(filename[:-3])
    client.load_extension(f'cogs.{filename[:-3]}')
  db['COGS'] = files


@tasks.loop(minutes=1)
async def change_status():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status_all)))



keep_alive()
client.run(os.environ['TOKEN'])