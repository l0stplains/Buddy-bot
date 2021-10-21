import discord
import requests

from discord.ext import commands

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

  @commands.command(brief="reddit")
  async def reddit(self, ctx, args='funny'):
    await ctx.send(get_reddit(args))

  @commands.command(brief="Dank Science Memes (5Head)", aliases = ['science', '5headmemes', 'sc'])
  async def sciencememes(self, ctx):
    await ctx.send(get_reddit('DankScienceMemes'))

def get_reddit(r='dankmemes'):
  """
  Get a meme url from a subreddit using meme api (github.com/D3vd/Meme_Api)
  """
  
  response = requests.get(f"https://meme-api.herokuapp.com/gimme/{r}/1")
  image = response.json();
  if 'code' not in image.keys():
    if image['memes'][0]['nsfw'] == True:
      return f"|| {image['memes'][0]['url']} ||\nNSFW CONTENT!"
    return image['memes'][0]['url']
  else:
    return "ERROR\nMake sure you pass a real subreddit (r/...)"


def setup(client):
  client.add_cog(Reddit(client))