import discord
import requests
from discord.ext import commands

def get_reddit(r='dankmemes'):
  response = requests.get(f"https://meme-api.herokuapp.com/gimme/{r}/1")
  image = response.json();
  return image['memes'][0]['url']

class Reddit(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(brief="POGCHAMP!")
  async def pog(self,ctx):
    await ctx.send("POG!")

  @commands.command(brief="SHEESH")
  async def sheesh(self, ctx):
    await ctx.send("SHEESH :cold_face:")
  
  @commands.command(brief="MEME")
  async def meme(self, ctx):
    await ctx.send(get_reddit())

  @commands.command(brief="69?420?HAHAHA", aliases=['420','69','69420'])
  async def _69(self, ctx):
    await ctx.send("Nice!")

  @commands.command(brief="Just animals...maybe", aliases=['animal'])
  async def animals(self, ctx):
    await ctx.send(get_reddit('cute_animals'))

def setup(client):
  client.add_cog(Reddit(client))