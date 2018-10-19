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

import asyncio
from random import choice
import discord
from discord.ext import commands
from websockets.exceptions import ConnectionClosed

class Events():
    def __init__(self, bot):
        self.bot = bot
        self.status_updates = bot.loop.create_task(self.status_updater()) # Initiate the status updates and save it for the further close

    async def status_updater(self):
        while not self.bot.is_ready():
            await asyncio.sleep(3) # loop until the bot is ready to have a populated cache

        while not self.bot.is_closed() and not self.status_updates.cancelled():
            try:
                # don't question any of these
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=choice(("machine", "the Discord latency", "watches",
                 "the sunshine", "Discord tokens 😈", "annoying unicode nicknames", "your weeb avy", "what you eat", "my weight"))))
                await asyncio.sleep(60)
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=choice(("your input", "your neighbours", \
                 "you, I promise", "fighting chipmunks"))))
                await asyncio.sleep(60)
                await self.bot.change_presence(activity=discord.Streaming(name=choice(("and screaming", "and shouting", "silence", "chill")), url="https://twitch.tv/#"))
                await asyncio.sleep(60)
                await self.bot.change_presence(activity=discord.Game(name=choice(("your life", "basketball", "TicTacToe instead working", \
                 "by the rules make everybody else happy.", "for peanuts", "jokes", "in time", "spin the bottle", "attention", "our rules", "an old movie"))))
                await asyncio.sleep(60)
            except ConnectionClosed:
                pass

    def __unload(self):
        self.status_updates.cancel() # Cancel the status updates on unload

def setup(bot):
    bot.add_cog(Events(bot))
