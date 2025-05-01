# llm_cog.py

import asyncio
import discord
from discord.ext import commands

# Import your local LLM functions
from llm import local_llm, get_resource_stats


class LLMCog(commands.Cog):
    """
    Cog for handling local LLM interactions:
    - /tone <text>       → reformats input text via the local LLM
    - resources          → shows current resource usage stats
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from ourselves
        if message.author == self.bot.user:
            return

        content = message.content
        lower = content.lower()

        # Handle /tone command
        if lower.startswith('/tone'):
            # Extract everything after "/tone"
            input_text = content[len('/tone'):].strip()
            try:
                # Run the (potentially blocking) LLM call in a thread
                generated = await asyncio.to_thread(local_llm, input_text)
                if len(generated) >= 4000:
                    generated = generated[:3980] + "..."
                await message.channel.send(generated)
            except Exception as e:
                err = f"Error in /tone command: {e}"
                if len(err) >= 4000:
                    err = err[:3980] + "..."
                await message.channel.send(err)

        # Handle resources command
        elif lower.startswith('resources'):
            try:
                stats = get_resource_stats()
                await message.channel.send(stats)
            except Exception as e:
                err = f"Error in resources command: {e}"
                if len(err) >= 4000:
                    err = err[:3980] + "..."
                await message.channel.send(err)


def setup(bot: commands.Bot):
    """discord.py extension hook."""
    bot.add_cog(LLMCog(bot))
