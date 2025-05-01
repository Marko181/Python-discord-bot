# main.py

"""
Project organisation:

Classified/
└── classified.py <- bot key, user ids, channel ids
Code/
├── main.py
├── lifecycle_cog.py        # on_ready + scheduler setup
├── help_cog.py             # the bot_help() listener
├── menza_cog.py            # send_menza_message() + menza keyword
├── hrana_cog.py            # all “hrana”-related listeners
├── meme_cog.py             # random, specific, list, upload, delete, dump memes
├── llm_cog.py              # /tone and resources listeners
└── admin_cog.py            # BotUpdateNow, BotRebootNow, status, BotInfo
files/
├── meme1.png
├── meme2.jpg
├── meme3.jpeg
└── meme4.gif
"""

import sys
import os
import discord
from discord.ext import commands
import logging

from lifecycle_cog import LifecycleCog
from help_cog import HelpCog
from menza_cog import MenzaCog
from hrana_cog import HranaCog
from meme_cog import MemeCog
from llm_cog import LLMCog
from admin_cog import AdminCog

logging.info("Starting main.py")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Classified')))
from classified import BotConfig
BOT_VERSION_PATH = "./version.txt"
with open(BOT_VERSION_PATH, 'r') as file:
    bot_version = file.read().strip()
    
logging.info("Imported classified")
logging.info(f"Bot version v {bot_version}")

# Path to the folder where memes and images are stored
MEME_FOLDER: str = './files/memes/'

# Configure intents
intents = discord.Intents.default() # intents = discord.Intents.all()
intents.message_content = True

# Instantiate the bot (we're not using any prefix-based commands,
# just raw on_message listeners in our Cogs)
bot = commands.Bot(command_prefix="\x00", intents=intents)

# Register all Cogs
bot.add_cog(LifecycleCog(bot))
bot.add_cog(HelpCog(bot))
bot.add_cog(MenzaCog(bot))
bot.add_cog(HranaCog(bot))
bot.add_cog(MemeCog(bot))
bot.add_cog(LLMCog(bot))
bot.add_cog(AdminCog(bot))

if __name__ == "__main__":
    # Run the bot with the token from classified.py
    logging.info("Starting bot")
    bot.run(BotConfig.BOT_KEY)
    logging.info("Bot running")
