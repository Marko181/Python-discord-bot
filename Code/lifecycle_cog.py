# lifecycle_cog.py

import os
import sys
import logging
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

#from menza_cog import send_menza_message
from meme_cog import send_random_image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Classified')))
from classified import BotConfig

# Keep your version string here (or move into classified.py if you prefer)

ERROR_FILE_PATH = "./errorReport.txt"
BOT_VERSION_PATH = "./version.txt"
with open(BOT_VERSION_PATH, 'r') as file:
    bot_version = file.read().strip()

class LifecycleCog(commands.Cog):
    """Cog for handling bot startup, status message and scheduled jobs."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()

    @commands.Cog.listener()
    async def on_ready(self):
        """Runs once when the bot is ready: sends a startup message, checks for errors, and schedules jobs."""
        try:
            # 1) Send “alive” message in the playground channel
            channel = self.bot.get_channel(BotConfig.CHANNEL_ID_BOTPLAYGROUND)
            if channel:
                await channel.send(f"Alive and ready! v{bot_version}")

                # 2) If there’s an existing error report, send it
                if os.path.exists(ERROR_FILE_PATH):
                    with open(ERROR_FILE_PATH, "r") as f:
                        content = f.read().strip()
                    
                    # Suppress specific message
                    if len(content) > 220:
                        if len(content) >= 2000:
                            content = content[:1980] + "..."
                        await channel.send(f"Error Report Found:\n```\n{content}\n```")
            else:
                logging.warning("LifecycleCog: BotPlayground channel not found.")

            logging.info(f"Logged in as {self.bot.user}")

            # 3) Schedule your two daily tasks at 10:00 Mon–Fri, Jan–May & Oct–Dec
            # self.scheduler.add_job(
            #     send_menza_message,
            #     trigger="cron",
            #     day_of_week="mon-fri",
            #     hour=10,
            #     minute=0,
            #     month="1-5,10-12",
            #     args=[self.bot],
            # )
            self.scheduler.add_job(
                send_random_image,
                trigger="cron",
                day_of_week="mon-fri",
                hour=10,
                minute=0,
                month="1-12",
                args=[self.bot],
            )
            self.scheduler.start()

        except Exception as e:
            # Catch-all: truncate if too long and try to report back
            error_msg = f"An error occurred on startup: {e}"
            if len(error_msg) >= 2000:
                error_msg = error_msg[:1980] + "..."
            try:
                err_chan = self.bot.get_channel(BotConfig.CHANNEL_ID_BOTPLAYGROUND)
                if err_chan:
                    await err_chan.send(error_msg)
                else:
                    logging.error(error_msg)
            except Exception:
                logging.exception("Failed to send startup error message:")

    @commands.Cog.listener()
    async def on_message(self, message):
        # only for testing, ignore the bot itself
        if message.author == self.bot.user:
            return

        # simple ping→pong check
        if message.content.lower() == "ping":
            await message.channel.send("pong")

        if message.content.lower() == "pong":
            await message.channel.send("ping")
    
