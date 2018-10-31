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

from traceback import print_exc
import aiohttp
import discord
from discord.ext import commands

import config

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(config.prefix))
bot.config = config

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | {len(bot.guilds)} guilds | {len(bot.users)} users | {len(list(bot.get_all_channels()))} channels")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="it all load"), status=discord.Status.dnd)

@bot.event
async def on_message(message):
    if not message.guild or message.author.bot:
        # we don't wanna respond to DMs and bot messages
        return
    await bot.process_commands(message)

async def init_coros():
    bot.session = aiohttp.ClientSession()
    async with bot.session.get(f"https://api.tenor.com/v1/anonid?key={bot.config.tenor_key}") as r:
        bot.anon_id = (await r.json())["anon_id"]

if __name__ == "__main__":
    bot.loop.create_task(init_coros())
    bot.load_extension("jishaku") # optional, but recommended
    for module in bot.config.initial_modules:
        try:
            bot.load_extension(f"modules.{module}")
        except Exception:
            print_exc()
    bot.run(bot.config.token)
