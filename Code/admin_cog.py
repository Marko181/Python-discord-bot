# admin_cog.py

import sys
import os
import textwrap
import logging
import discord
from discord.ext import commands

# Ensure Classified is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Classified')))
from classified import BotConfig

import update

# Keep your version string here (or move into classified.py if you prefer)
BOT_VERSION_PATH = "./version.txt"
with open(BOT_VERSION_PATH, 'r') as file:
    bot_version = file.read().strip()

class AdminCog(commands.Cog):
    """
    Cog for admin-only commands:
      - BotUpdateNow [--branch BRANCH]
      - BotRebootNow
      - status
      - BotInfo
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        content = message.content

        # -------- BotUpdateNow --------
        if content.lower().startswith('botupdatenow'):
            if message.author.id in BotConfig.USER_IDS:
                parts = content.split()
                branch = "main"
                if "--branch" in parts:
                    idx = parts.index("--branch") + 1
                    if idx < len(parts):
                        branch = parts[idx]
                    else:
                        await message.channel.send("Napaka: manjka ime branch-a.")
                        return

                await message.channel.send(f"Clonam branch: `{branch}` ...")
                try:
                    update.bot_git_update(branch)
                except Exception as e:
                    err = f"Error running bot_git_update: {e}"
                    logging.exception(err)
                    await message.channel.send(err)
            else:
                await message.channel.send("Ja ne, nič ne bo.")

        # -------- BotRebootNow --------
        elif content.lower().startswith('botrebootnow'):
            if message.author.id in BotConfig.USER_IDS:
                await message.channel.send("Rebootam bota...")
                try:
                    update.bot_reboot()
                except Exception as e:
                    err = f"Error running bot_reboot: {e}"
                    logging.exception(err)
                    await message.channel.send(err)
            else:
                await message.channel.send("Noup, nič ne bo.")

        # -------- status --------
        elif content.lower().startswith('status'):
            await message.channel.send(f"Awake and alive! v{bot_version}")

        # -------- BotInfo --------
        elif content.lower().startswith('botinfo'):
            # Credit line
            await message.channel.send(
                "Bot writen by: Marko K., Tilen T., Jakob K., Vitan K. and Luka M."
            )

            # ASCII art
            ascii_art = textwrap.dedent("""
                /$$$$$$$$        /$$$$$$$              /$$    
                | $$_____/       | $$__  $$            | $$    
                | $$     /$$$$$$ | $$  \\ $$  /$$$$$$  /$$$$$$  
                | $$$$$ /$$__  $$| $$$$$$$  /$$__  $$|_  $$_/  
                | $$__/| $$$$$$$$| $$__  $$| $$  \\ $$  | $$    
                | $$   | $$_____/| $$  \\ $$| $$  | $$  | $$ /$$
                | $$   |  $$$$$$$| $$$$$$$/|  $$$$$$/  |  $$$$/ 
                |__/    \\_______/|_______/  \\______/    \\___/  
            """)
            await message.channel.send(f"\n```\n{ascii_art}\n```")


def setup(bot: commands.Bot):
    """discord.py extension hook."""
    bot.add_cog(AdminCog(bot))
