import discord
import os
import requests

from discord.ext import commands, tasks
from discord import Embed
from datetime import datetime
from replit import db


class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.send_weather.start()

    @commands.command(brief="Get current weather from a location.")
    async def weather(self, ctx, *, args="Indonesia"):
        await ctx.send(embed=get_weather(args))

    @tasks.loop(minutes=60)
    async def send_weather(self):
        """
        Sends a weather report from a location.
        """
        channel = self.client.get_channel(int(os.environ["WEATHER_UPDATE"]))
        if channel != None:
            if db["COUNTER"] >= 24:
                await channel.purge(limit=db["COUNTER"])
                db["COUNTER"] = 0
            await channel.send(embed=get_weather(db["WEATHER_LOCATION"]))
            db["COUNTER"] += 1

    @commands.command(brief="Change weather location for the hourly report.")
    async def weather_location(self, ctx, *, args="Indonesia"):
        db["WEATHER_LOCATION"] = args
        await ctx.send(
            f"Weather location has changed to {args}.\nMake sure you pass a real location otherwise it won't send a report."
        )


def get_weather(loc):
    """
    API call to OpenWeatherMap
    """
    loc = loc.title()  # Format location name.

    responses = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={loc}&appid={os.environ['WEATHER']}&units=metric"
    )
    weather = responses.json()
    if weather["cod"] == 200:
        status = weather["weather"][0]["main"]
        description = weather["weather"][0]["description"].capitalize()
        icon_id = weather["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/w/{icon_id}.png"
        status, color = get_icon(status)

        temperature_desc = f"""
    Feels like: {weather['main']['feels_like']} °C
    Temp min: {weather['main']['temp_min']} °C
    Temp max: {weather['main']['temp_max']} °C
    
    """
        embed = Embed(
            title=f"{loc} Weather Report!",
            colour=color,
            timestamp=datetime.utcnow(),
        )
        embed.add_field(
            name=f"ㅤ\nStatus: {status}", value=f"Description: {description}", inline=False
        )
        embed.add_field(
            name=f"ㅤ\nTemperature: {weather['main']['temp']} °C", value=temperature_desc, inline=True
        )
        embed.add_field(
            name=f"ㅤ\nWind Speed: {weather['wind']['speed']} km/h",
            value=f"Direction: {weather['wind']['deg']} °",
            inline=True,
        )
        embed.add_field(
            name=f"ㅤ\nHumidity: {weather['main']['humidity']}%",
            value=f"Pressure: {weather['main']['pressure']} mb",
            inline=True,
        )
        embed.set_thumbnail(url=icon_url)

        return embed

    else:
        return Embed(
            title="ERROR",
            description="\nMake sure you pass a real location name!",
            colour=0xFF0000,
        )


def get_icon(status):
    if status == "Clouds":
        return ("Cloudy :cloud:", 0x9E9E9E)
    elif status == "Haze":
        return ("Haze :cloud: :cloud: :cloud: :mask:", 0x81B594)
    elif status == "Rain":
        return ("Rainy :cloud_rain: :umbrella: ", 0x00CCFF)
    elif status == "Clear":
        return ("Clear :partly_sunny: :sunglasses: ", 0xFF8000)
    elif status == "Thunderstorm":
        return("Thunderstorm! :cloud_lightning: ", 0x413DFF)
    return (":cloud:", 0xCFCFCF)


def setup(client):
    client.add_cog(Weather(client))
