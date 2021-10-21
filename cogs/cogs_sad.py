import discord
import requests
from replit import db
from discord.ext import commands

class Sad(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['list-encourage', 'list_encourage'])
  async def encourage_list(self, ctx):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await ctx.send(f"{encouragements}")

  @commands.command(aliases=['del-encourage'])
  async def delete_encourage(self, ctx, *, args="1000"):
    encouragements = []
    if ctx.message.author.guild_permissions.manage_messages:
      if "encouragements" in db.keys():
        index = int(args.split(" ")[0])
        delete_encouragements(index)
        encouragements = db["encouragements"]
      await ctx.send(f"{encouragements}")
    else:
      await ctx.send("Sorry you don't have permission to delete_encourage.")

  @commands.command(aliases=['new-encourage'])
  async def new_encourage(self, ctx, *, args="nothing"):
    if ctx.message.author.guild_permissions.manage_messages:
      if args != 'nothing':
        encouraging_message = args
        update_encouragements(encouraging_message)
        await ctx.send("New encouraging message added.")
    else:
      await ctx.send("Sorry you don't have permission to new_encourage.")

  @commands.command(aliases=['quote','naufal','nopal'])
  async def quotes(self, ctx):
    quote = get_quote()
    await ctx.send(quote)
    
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

def setup(client):
  client.add_cog(Sad(client))