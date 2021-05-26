import discord
from discord.ext import commands

class Pog(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(brief="POGCHAMP!")
  async def pog(self,ctx):
    await ctx.send("POG!")

  @commands.command(brief="SHEEESH")
  async def sheesh(self, ctx):
    await ctx.send("SHEESH :cold_face:")
  

def setup(client):
  client.add_cog(Pog(client))