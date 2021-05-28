import os
import discord
from datetime import datetime
from replit import db
from discord import Embed
from discord.ext import commands


class Events(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_member_join(self, member):
    await member.send('Welcome 👋')
    role = discord.utils.get(member.guild.roles, name='Lv.0')
    await member.add_roles(role)
    print(f"{member} has joined a server!")
    embed = Embed(title=f"Welcome!", description=f"{member.mention} A warm welcome to you to join us!", colour=0xFF8000, timestamp=datetime.utcnow())
    embed.set_thumbnail(url=member.avatar_url)
    channel = self.client.get_channel(int(db['WELCOME']))
    await channel.send(embed=embed)

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    print(f"{member} has left a server!")



def setup(client):
  client.add_cog(Events(client))