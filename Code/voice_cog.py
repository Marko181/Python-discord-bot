# voice_cog.py

import sys
import os
import asyncio
import logging

import discord
from discord import app_commands
from discord.ext import commands

# Bring in BotConfig (if you later want channels, etc.)
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "Classified"))
)
from classified import BotConfig  # noqa: F401

# Where your MP3s live
MUSIC_FOLDER = "./music"


class VoiceCog(commands.Cog):
    """Cog for voice-channel playback commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
                "❌ You must be in a voice channel to use this command.",
                ephemeral=True
            )
            return

        # Build the path and check existence
        file_path = os.path.join(MUSIC_FOLDER, file_name)
        if not os.path.isfile(file_path):
            await interaction.response.send_message(
                f"❌ File `{file_name}` not found in `{MUSIC_FOLDER}`.",
                ephemeral=True
            )
            return

        # Connect (or move) the bot to the user's channel
        voice_channel = interaction.user.voice.channel
        vc: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=interaction.guild
        )
        if not vc:
            vc = await voice_channel.connect()
        elif vc.channel.id != voice_channel.id:
            await vc.move_to(voice_channel)

        # Play the audio
        try:
            source = discord.FFmpegPCMAudio(file_path)
            vc.play(source, after=lambda err: asyncio.create_task(self._after_play(err, vc)))
        except Exception as e:
            logging.exception("Error starting playback")
            await interaction.response.send_message(
                f"❌ Error playing `{file_name}`: {e}", ephemeral=True
            )
            return

        # Acknowledge the slash command
        await interaction.response.send_message(f"▶️ Now playing `{file_name}`")

    async def _after_play(self, error, vc: discord.VoiceClient):
        """Disconnect after playback finishes (or on error)."""
        if error:
            logging.exception("Playback error", exc_info=error)
        try:
            await vc.disconnect()
        except Exception:
            logging.exception("Failed to disconnect after playback")

    @play.autocomplete("file_name")
    async def play_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete MP3 filenames in the music folder."""
        choices = []
        try:
            for fname in os.listdir(MUSIC_FOLDER):
                if fname.lower().endswith(".mp3") and fname.lower().startswith(current.lower()):
                    choices.append(app_commands.Choice(name=fname, value=fname))
                    if len(choices) >= 25:
                        break
        except Exception:
            logging.exception("Error during play_autocomplete")
        return choices


def setup(bot: commands.Bot):
    """discord.py extension hook."""
    bot.add_cog(VoiceCog(bot))
