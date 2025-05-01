# menza_cog.py

import sys
import os
import discord
from discord.ext import commands

# Ensure we can import BotConfig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Classified')))
from classified import BotConfig

# Import your menza logic
from menza import main_menza

async def send_menza_message(bot: commands.Bot):
    """
    Scheduled job: fetch today's menza menu and post it
    into the configured channel.
    """
    channel = None
    try:
        channel = bot.get_channel(BotConfig.CHANNEL_ID_HRANA)
        if not channel:
            print("Menza channel not found")
            return

        await channel.send(main_menza())

    except Exception as e:
        # Truncate to avoid Discord limit
        err = f"Error occurred in send_menza_message: {e}"
        if len(err) >= 4000:
            err = err[:3996] + "..."
        if channel:
            await channel.send(err)
        else:
            print(err)


class MenzaCog(commands.Cog):
    """Cog for on-demand menza menu requests."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        # Trigger on "menza"
        if message.content.lower().startswith('menza'):
            try:
                await message.channel.send(main_menza())
            except Exception as e:
                err = f"Error in menza command: {e}"
                if len(err) >= 4000:
                    err = err[:3996] + "..."
                await message.channel.send(err)


def setup(bot: commands.Bot):
    """discord.py extension hook."""
    bot.add_cog(MenzaCog(bot))
