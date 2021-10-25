import discord
import requests
import os
from replit import db
from discord.ext import commands


class Manager(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if permission(ctx, "ban_members") and permission(ctx, "kick_members"):
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} kicked")
        else:
            await ctx.send("Sorry you don't have permission to do that.")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if permission(ctx, "ban_members") and permission(ctx, "kick_members"):
            await member.ban(reason=reason)
            await ctx.send(f"Banned {member.mention}")
        else:
            await ctx.send("Sorry you don't have permission to do that.")

    @commands.command()
    async def unban(self, ctx, *, member):
        if permission(ctx, "ban_members") and permission(ctx, "kick_members"):
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")

            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (
                    member_name,
                    member_discriminator,
                ):
                    await ctx.guild.unban(user)
                    await ctx.send(f"Unbanned {user.mention}")
                    return
        else:
            await ctx.send("Sorry you don't have permission to do that.")

    @commands.command(brief="list of banned IDs")
    async def banned_list(self, ctx):
        if ctx.channel.id == int(os.environ["BOSS"]):
            banned_users = await ctx.guild.bans()
            await ctx.send("Banned users list:")
            user_list = ""
            if banned_users == []:
                user_list = "Nothing"
            for banned in banned_users:
                user = banned.user
                user_list += (
                    f"Name: {user.name}#{user.discriminator}\nUser ID: {user.id}\n\n"
                )
            await ctx.send(user_list)

    @commands.command(brief="clear messages")
    async def clear(self, ctx, amount: int):
        if permission(ctx, "manage_messages"):
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"{amount} messages cleared by-<@{ctx.author.id}>.")
        else:
            await ctx.send("Sorry you don't have permission to clear messages.")

    @commands.command(brief="Change servers' bot prefix *need restart")
    async def prefix(self, ctx, prefix: str):
        prefix_list = ["!", "/", "?", ">", "<", "$", "&", "*", "%", "-", "~"]
        if permission(ctx, "manage_messages"):
            if prefix in prefix_list:
                db["PREFIX"] = prefix
                await ctx.send(
                    f"Server prefix has changed to {db['PREFIX']}\nPlease restart the bot."
                )
            else:
                await ctx.send(
                    f"Please use one of these to use as a prefix\n{prefix_list}"
                )
        else:
            await ctx.send("Sorry you don't have permission to clear messages.")

    @commands.command(brief="Get servers' bot prefix")
    async def get_prefix(self, ctx):
        await ctx.send(db["PREFIX"])


def permission(ctx, arg: str):
    if arg == "ban_members":
        return ctx.message.author.guild_permissions.ban_members
    if arg == "kick_members":
        return ctx.message.author.guild_permissions.kick_members
    if arg == "manage_messages":
        return ctx.message.author.guild_permissions.manage_messages
    return False


def setup(client):
    client.add_cog(Manager(client))
