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

# main.py

import sys, os, logging, asyncio
import discord
from discord.ext import commands

# configure logging…
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

# tell Python where to find Classified/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Classified')))
from classified import BotConfig

# import your Cog classes
from lifecycle_cog import LifecycleCog
from help_cog      import HelpCog
from menza_cog     import MenzaCog
from hrana_cog     import HranaCog
from meme_cog      import MemeCog
from llm_cog       import LLMCog
from admin_cog     import AdminCog
from voice_cog     import VoiceCog

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=discord.Intents.all())
        self.intents.message_content = True

    async def setup_hook(self):
        # this is run *once*, before login
        await self.add_cog(HelpCog(self))
        await self.add_cog(MenzaCog(self))
        await self.add_cog(HranaCog(self))
        await self.add_cog(MemeCog(self))
        await self.add_cog(LLMCog(self))
        await self.add_cog(AdminCog(self))
        await self.add_cog(VoiceCog(self))
        await self.add_cog(LifecycleCog(self))

async def main():
    bot = MyBot()
    logging.info("Starting bot")
    await bot.start(BotConfig.BOT_KEY)

if __name__ == "__main__":
    asyncio.run(main())
