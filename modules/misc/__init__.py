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

import discord
from discord.ext import commands

class Misc():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="credits")
    async def _credits(self, ctx):
        """Some informations about the bot"""
        embed = discord.Embed(color=0xFFD00D)
        embed.add_field(name="About the bot", value="Rebot is a bot for all the mobile user needs. It's main goal to provide the desktop client's benefits for everyone.", inline=False)
        embed.add_field(name="Bot pfp", value="Icon made by [Freepik](https://www.flaticon.com/authors/freepik) from www.flaticon.com", inline=False)
        embed.add_field(name="Third-party libs", value="```• discord.py - MIT license\n• jishaku - MIT license\n• aiohttp - Apache License 2.0\n• ujson - BSD license```", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def _ping(self, ctx):
        """Pong! Shows you the bot websocket latency"""
        await ctx.send(f"Pong! That took `{round(self.bot.latency * 1000, 2)}` ms.")

def setup(bot):
    bot.add_cog(Misc(bot))
