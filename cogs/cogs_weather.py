import discord
import os
import requests

from discord.ext import commands, tasks
from discord import Embed
from datetime import datetime

class Weather(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.send_weather.start()

  @commands.command(brief="Get current weather.")
  async def weather(self, ctx, args="Cianjur"):
    args = args.lower()
    args = args.capitalize()

    await ctx.send(embed=get_weather(args))

  @tasks.loop(minutes=60)
  async def send_weather(self):
    """
    Sends Indonesia weather report.
    """
    channel = self.client.get_channel(int(os.environ['WEATHER_UPDATE']))
    if channel != None:
      await channel.send(embed=get_weather('Indonesia'))


def get_weather(city):
  '''
  API call to OpenWeatherMap
  '''
  
  responses = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ['WEATHER']}&units=metric")
  weather = responses.json();
  if weather['cod'] == 200:
    status = weather['weather'][0]['main']
    status, color = get_icon(status)
    
    text = f"""
    Temperature: {weather['main']['temp']} °C
    Humidity: {weather['main']['humidity']}%
    Wind Speed: {weather['wind']['speed']} km/h
    
    """
    embed = Embed(title=f"{city} Weather Report!\n\n{status}", description=text, colour=color, timestamp=datetime.utcnow())
    
    return embed

  else:
    return Embed(title="ERROR", description="\nMake sure you pass a real city name!")

def get_icon(status):
  if status == "Clouds":
    return ("Status: Cloudy :cloud:", 0xC2C2C2)
  elif status == "Haze":
    return ("Status: Haze :cloud: :cloud: :cloud: :mask:", 0x81B594)
  elif status == "Rain":
    return ("Status: Rainy :cloud_rain: :umbrella: ", 0x76C9DE)
  elif status == "Clear":
    return ("Status: Clear :partly_sunny: :sunglasses: ", 0xFF8000)
  return (":cloud:", 0xCFCFCF)

def setup(client):
  client.add_cog(Weather(client))