# llm_cog.py

import subprocess
import asyncio
import discord
from discord.ext import commands

# Import your local LLM functions
from llm import local_llm, get_resource_stats, rag_llm


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
            use_rag = '--rag' in input_text
            try:
                if use_rag:
                    generated = await asyncio.to_thread(rag_llm, input_text)
                else:
                    generated = await asyncio.to_thread(local_llm, input_text)
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

        

        elif lower.startswith('update_rag_db'):
            await message.channel.send("Starting RAG pipeline update. This may take a while...")
            try:
                script_path = # TODO: set the correct path to the automated_RAG_pipeline script "/Users/lukamelinc/Desktop/Programiranje/Python-discord-bot/Code/LLM_finetune/data_scraping/automated_RAG_pipeline.py"
                # Run the script and capture output
                result = subprocess.run(
                    ["python", script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                # Truncate output if too long for Discord
                output = result.stdout + "\n" + result.stderr
                if len(output) > 3900:
                    output = output[:3900] + "\n...[truncated]"
                await message.channel.send(f"RAG pipeline update finished.\nOutput:\n```{output}```")
            except Exception as e:
                err = f"Error running RAG pipeline: {e}"
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
