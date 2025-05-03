# voice_cog.py
import sys
import os
import asyncio
import logging
import aiohttp

import discord
from discord import app_commands
from discord.ext import commands

# Bring in BotConfig (if you need permissions or channel IDs later)
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "Classified"))
)
from classified import BotConfig  # noqa: F401

# Where your MP3s live
MUSIC_FOLDER = "./Music"


async def ensure_music_folder():
    os.makedirs(MUSIC_FOLDER, exist_ok=True)


class VoiceCog(commands.Cog):
    """Cog for voice playback, uploading, and deleting MP3s."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        content = message.content.strip()
        lower = content.lower()

        # 1) Delete an audio file (admin users only)
        if lower.startswith("delete audio "):
            if message.author.id in BotConfig.USER_IDS:
                key = content[len("delete audio "):].strip()
                if not key.lower().endswith(".mp3"):
                    key += ".mp3"
                path = os.path.join(MUSIC_FOLDER, key)
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                        await message.channel.send(f"Audio `{key}` deleted!")
                    except Exception as e:
                        logging.exception("Failed to delete audio")
                        await message.channel.send(f"Error deleting `{key}`: {e}")
                else:
                    await message.channel.send(f"Audio `{key}` not found in `{MUSIC_FOLDER}`.")
            else:
                await message.channel.send("Ja ne nč ne bo")
            return

        # 2) Save uploaded MP3s
        if message.attachments:
            mp3_attachments = [
                att for att in message.attachments
                if att.filename.lower().endswith(".mp3")
            ]
            if mp3_attachments:
                await ensure_music_folder()
                for attachment in mp3_attachments:
                    filename = attachment.filename
                    dest_path = os.path.join(MUSIC_FOLDER, filename)
                    if os.path.exists(dest_path):
                        await message.channel.send(f"`{filename}` is already saved.")
                        continue

                    await message.channel.send(
                        f"This audio (`{filename}`) isn’t saved – save it? (yes, yes new_name, no)"
                    )

                    def check(resp: discord.Message):
                        return (
                            resp.author == message.author
                            and resp.channel == message.channel
                            and (
                                resp.content.lower() == "no"
                                or resp.content.lower().startswith("yes")
                            )
                        )

                    try:
                        resp = await self.bot.wait_for("message", check=check, timeout=30)
                    except asyncio.TimeoutError:
                        await message.channel.send("Timed out – audio not saved.")
                        continue

                    text = resp.content.strip()
                    if text.lower() == "no":
                        await message.channel.send("Okay, not saving.")
                        continue

                    # text starts with "yes"
                    custom = text[3:].strip()  # may be empty
                    save_name = custom + ".mp3" if custom else filename
                    save_path = os.path.join(MUSIC_FOLDER, save_name)

                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as r:
                                r.raise_for_status()
                                data = await r.read()
                        with open(save_path, "wb") as f:
                            f.write(data)
                        await message.channel.send(f"Saved `{save_name}` in `{MUSIC_FOLDER}`.")
                    except Exception as e:
                        logging.exception("Failed to save uploaded MP3")
                        await message.channel.send(f"Could not save `{save_name}`: {e}")
                return

    #
    # 3) /play slash command
    #
    @app_commands.command(
        name="play",
        description="Play an MP3 file from the music folder"
    )
    @app_commands.describe(
        file_name="Name of the MP3 (include the .mp3 extension)"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        file_name: str
    ):
        # Ensure the user is in a voice channel
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(
                "You must be in a voice channel to use this command.",
                ephemeral=True
            )
            return

        # Build the path and check existence
        file_path = os.path.join(MUSIC_FOLDER, file_name)
        if not os.path.isfile(file_path):
            await interaction.response.send_message(
                f"File `{file_name}` not found in `{MUSIC_FOLDER}`.",
                ephemeral=True
            )
            return

        # Connect or move
        voice_channel = interaction.user.voice.channel
        vc: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=interaction.guild
        )
        if not vc:
            vc = await voice_channel.connect()
        elif vc.channel.id != voice_channel.id:
            await vc.move_to(voice_channel)

        # Play
        try:
            source = discord.FFmpegPCMAudio(file_path)
            vc.play(source, after=lambda err: asyncio.create_task(self._after_play(err, vc)))
        except Exception as e:
            logging.exception("Error starting playback")
            await interaction.response.send_message(
                f"Error playing `{file_name}`: {e}", ephemeral=True
            )
            return

        await interaction.response.send_message(f"▶️ Now playing `{file_name}`")

    @play.autocomplete("file_name")
    async def play_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete MP3 filenames in the music folder."""
        choices = []
        try:
            await ensure_music_folder()
            for fname in os.listdir(MUSIC_FOLDER):
                if fname.lower().endswith(".mp3") and fname.lower().startswith(current.lower()):
                    choices.append(app_commands.Choice(name=fname, value=fname))
                    if len(choices) >= 25:
                        break
        except Exception:
            logging.exception("Error during play_autocomplete")
        return choices

    #
    # 4) /stop slash command
    #
    @app_commands.command(
        name="stop",
        description="Stop playback and leave the voice channel"
    )
    async def stop(self, interaction: discord.Interaction):
        vc = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not vc or not vc.is_playing():
            await interaction.response.send_message(
                "No audio is playing right now.", ephemeral=True
            )
            return

        vc.stop()
        try:
            await vc.disconnect()
        except Exception:
            logging.exception("Failed to disconnect after stop")
        await interaction.response.send_message("Stopped playback and left voice channel.")

    async def _after_play(self, error, vc: discord.VoiceClient):
        """Disconnect after playback finishes or on error."""
        if error:
            logging.exception("Playback error", exc_info=error)
        try:
            await vc.disconnect()
        except Exception:
            logging.exception("Failed to disconnect after playback")


def setup(bot: commands.Bot):
    bot.add_cog(VoiceCog(bot))
