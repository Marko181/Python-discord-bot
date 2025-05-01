# hrana_cog.py

import sys
import os
import logging
import discord
from discord.ext import commands

# Ensure Classified is on the path so we can import BotConfig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Classified')))
from classified import BotConfig

# Import your hrana logic
from hrana import main_restaurant


class HranaCog(commands.Cog):
    """
    Cog for handling 'hrana' commands:
    - hrana <restaurant_name>
    - hrana random
    - hrana pun
    - hrana fact
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        content = message.content
        if content.lower().startswith('hrana'):
            # Extract the argument (after 'hrana ')
            restaurant_name = content[len('hrana'):].strip()
            try:
                # Fetch the menu or fact/pun
                menu = main_restaurant(restaurant_name)
                if len(menu) >= 4000:
                    menu = menu[:3980] + "..."
                await message.channel.send(menu)
            except Exception as e:
                err = f"Error in hrana command: {e}"
                # Truncate to avoid Discord's 2000-char limit
                if len(err) >= 2000:
                    err = err[:3980] + "..."
                logging.exception("HranaCog failed:")
                await message.channel.send(err)


def setup(bot: commands.Bot):
    """discord.py extension hook."""
    bot.add_cog(HranaCog(bot))
