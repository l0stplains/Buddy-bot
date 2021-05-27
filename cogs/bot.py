import discord
import requests
import random
from replit import db
from discord.ext import commands

class Bots(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def ping(self, ctx):
    await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

  @commands.command()
  async def copy_me(self, ctx,*,args="I can't copy something that didn't exist!"):
    await ctx.send(args)

  @commands.command(aliases=['8ball','?'])
  async def _8ball(self, ctx, *, question="Do you think i need to pass in some question for this command?"):
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(db['quest_responses'])}")

  @commands.command()
  async def embed(self, ctx):
    embed = Embed(title="Hello", description="This is an embed message", colour=0xFF0000)
    await ctx.send(embed=embed)

  @commands.command(aliases=['hi','HELLO', 'HI'])
  async def hello(self, ctx):
    await ctx.send("Hello there!")

  @commands.command()
  async def echo(self, ctx, *, msg="o0OoO0OoO0oOoo echo nothing"):
    await ctx.send(msg)

def setup(client):
  client.add_cog(Bots(client))