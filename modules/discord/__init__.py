"""
    Rebot - A random Discord bot that helps mobile users to use desktop client built-in commands
    Copyright (C) 2018  Diniboy1123 <diniboy [at] protonmail [dot] com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

try:
    from ujson import loads # faster but external
except ImportError:
    from json import loads
import discord
import secrets # maximum random gifs

from discord.ext import commands

from utils import remove_mentions

class Discord():
    def __init__(self, bot):
        self.bot = bot
        self.xivdb_result_limit = 10
        self.flips = {
            "tableflip": "(╯°□°）╯︵ ┻━┻",
            "shrug": "¯\_(ツ)_/¯",
            "unflip": "┬─┬ ノ( ゜-゜ノ)"
        }
        async with bot.session.get(f"https://api.tenor.com/v1/anonid?key={bot.config.tenor_key}") as r:
            self.anon_id = loads(await r.text())["anon_id"]

    @commands.command(name="tts")
    async def _tts(self, ctx, *, shout: commands.clean_content):
        """Text to speech

        Pretty annoying isn't it?
        """
        if not ctx.channel.permissions_for(ctx.guild.me).send_tts_messages and not ctx.channel.permissions_for(ctx.guild.me).manage_webhooks:
            return await ctx.send("The bot doesn't have TTS rights.")
        if not ctx.channel.permissions_for(ctx.author).send_tts_messages:
            await ctx.send(f"{remove_mentions(ctx.author.name)} you don't have send TTS permissions.", delete_after=10)
        if len(shout) > 1900:
            return await ctx.send("Too much text to convert.", delete_after=10)
        if not ctx.channel.permissions_for(ctx.guild.me).manage_webhooks:
            return await ctx.send(f"{remove_mentions(ctx.author.display_name)} said: {shout}", tts=True)
        try:
            webhooks = await ctx.channel.webhooks()
            if webhooks:
                webhook = webhooks[0]
            else:
                webhook = await ctx.channel.create_webhook(name="Rebot Hook")
            await webhook.send(shout, username=ctx.author.display_name, avatar_url=ctx.author.avatar_url_as(format="png"), tts=True)
        except (discord.Forbidden, discord.HTTPException):
            return await ctx.send(f"{remove_mentions(ctx.author.display_name)} said: {shout}", tts=True)

    @commands.command(name="me")
    async def _me(self, ctx, *, shout: commands.clean_content):
        """Displays text with emphasis"""
        if len(shout) > 1900:
            return await ctx.send("Too much text to send.", delete_after=10)
        if not ctx.channel.permissions_for(ctx.guild.me).manage_webhooks:
            return await ctx.send(f"{remove_mentions(ctx.author.display_name)} said: _{shout}_")
        try:
            webhooks = await ctx.channel.webhooks()
            if webhooks:
                webhook = webhooks[0]
            else:
                webhook = await ctx.channel.create_webhook(name="Rebot Hook")
            await webhook.send(f"_{shout}_", username=ctx.author.display_name, avatar_url=ctx.author.avatar_url_as(format="png"))
        except (discord.Forbidden, discord.HTTPException):
            return await ctx.send(f"{remove_mentions(ctx.author.display_name)} said: _{shout}_")

    @commands.command(name="tableflip", aliases=["shrug", "unflip"])
    async def _flips(self, ctx, *, message: commands.clean_content=None):
        """Appends things to your message"""
        response = self.flips[ctx.invoked_with]
        if message and len(message) > 1900:
            return await ctx.send("Too much text to send.", delete_after=10)
        elif not message:
            message = ""
        if not ctx.channel.permissions_for(ctx.guild.me).manage_webhooks:
            return await ctx.send(f"{remove_mentions(ctx.author.display_name)} said: {message} {response}")
        try:
            webhooks = await ctx.channel.webhooks()
            if webhooks:
                webhook = webhooks[0]
            else:
                webhook = await ctx.channel.create_webhook(name="Rebot Hook")
            await webhook.send(f"{message} {response}", username=ctx.author.display_name, avatar_url=ctx.author.avatar_url_as(format="png"))
        except (discord.Forbidden, discord.HTTPException):
            return await ctx.send(f"{remove_mentions(ctx.author.display_name)} said: {message} {response}")

    @commands.has_permissions(change_nickname=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.command(name="nick")
    async def _nick(self, ctx, *, nick: str):
        """Sets your nick on the server"""
        if len(nick) > 32:
            return await ctx.send("Choose a shorter nickname than 32 characters!", delete_after=10)
        try:
            await ctx.author.edit(nick=nick)
        except discord.Forbidden:
            await ctx.send("Couldn't update your nickname because your are on a higher place on the role hierachy list than me.", delete_after=10)

    @commands.command(name="giphy")
    async def _giphy(self, ctx, *, query: str):
        """Search animated GIFs on the web"""
        params = {
            "api_key": self.bot.config.giphy_key,
            "q": query,
            "limit": 1,
        }
        async with self.bot.session.get("https://api.giphy.com/v1/gifs/search", params=params) as req:
            if req.status != 200:
                return await ctx.send(f"Error! The server returned a `{req.status}` code.")
            response = loads(await req.text())
        if not response.get("data") or not response["data"][0].get("url"):
            return await ctx.send("No results", delete_after=10)
        await ctx.send(response["data"][0]["url"])

    @commands.command(name="tenor")
    async def _tenor(self, ctx, *, query: str):
        """Search more animated GIFs on the web"""
        params = {
            "key": self.bot.config.tenor_key,
            "q": query,
            "anon_id": self.anon_id,
            "limit": 50, # we wanna get the maximum tenor results to choose a random one
        }
        async with self.bot.session.get(f"https://api.tenor.com/v1/search", params=params) as req:
            if req.status != 200:
                return await ctx.send(f"Error! The server returned a `{req.status}` code.")
            response = loads(await req.text())
        results = response.get("results")
        if not results: # list has length of 0 or is not even in the json
            return await ctx.send("No results", delete_after=10)
        await ctx.send(secrets.choice(results)["url"]) # get a truly randomly chosen gif

    @commands.command(name="xivdb")
    async def _xivdb(self, ctx, *, query: str):
        """Search in the XIVDB database"""
        if not 2 < len(query) < 16:
            return await ctx.send("Your query must be longer than 2 characters and shorter than 16!", delete_after=10)
        params = {
            "string": query,
            "limit": 1
        }
        async with self.bot.session.get("https://api.xivdb.com/search", params=params) as req:
            if req.status != 200:
                return await ctx.send(f"Error! The server returned a `{req.status}` code.")
            response = loads(await req.text())
        items = []
        for content_type, _results in response.items():
            if _results.get("total") == 0:
                continue
            result = _results["results"][0]
            items.append(f"• {result.get('url_type', 'Unknown type').title()} - [{result.get('name')}]({result.get('url_xivdb')})")
        if not items:
            return await ctx.send("No results!")
        await ctx.send(embed=discord.Embed(title="Results", description="\n".join(items[:self.xivdb_result_limit])))

def setup(bot):
    bot.add_cog(Discord(bot))
