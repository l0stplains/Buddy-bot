import discord
import requests
from discord.ext import commands

def get_meme():
  response = requests.get("https://meme-api.herokuapp.com/gimme/1")
  meme = response.json();
  return meme['memes'][0]['url']

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
    await ctx.send(get_meme())

def setup(client):
  client.add_cog(Reddit(client))