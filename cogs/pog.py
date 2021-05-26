import discord
from discord.ext import commands

class Pog(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(brief="POGCHAMP!")
  async def pog(self,ctx):
    await ctx.send("POG!")

def setup(client):
  client.add_cog(Pog(client))