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

from discord.ext import commands

class Owner():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["die"], hidden=True)
    async def logout(self, ctx):
        """[OWNER] Kills the bot"""
        await ctx.send("Bye cruel world!")
        await self.bot.logout()

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

def setup(bot):
    bot.add_cog(Owner(bot))
