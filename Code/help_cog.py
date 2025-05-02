# help_cog.py

import difflib
import discord
from discord.ext import commands

# List every command/keyword you want to suggest for:
ORIGINAL_COMMANDS = [
    "help",
    "menza",
    "whois",
    "hrana",
    "hrana random",
    "hrana pun",
    "hrana fact",
    "ls memes",
    "rnd meme",
    "dump memez",
    "meme",          # for raw "meme foo"
    "/meme",         # your slash
    "/tone",
    "resources",
    "status",
    "BotInfo",
    "BotUpdateNow",
    "BotRebootNow",
]

# build a lowercase→original map
COMMAND_MAP = {cmd.lower(): cmd for cmd in ORIGINAL_COMMANDS}
LOWER_COMMANDS = list(COMMAND_MAP.keys())

class HelpCog(commands.Cog):
    """
    Cog for responding to 'help' requests.
    Listens for messages that start with 'help' and replies with a list of commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.help_text = (
            "Ukazi, ki so na voljo:\n"
                " - menza: Si lačn in na FE-ju\n"
                " - hrana <x>: Izpiše meni restavracije <x>\n"
                " - hrana random: Ko res neveš kaj bi jedu\n"
                " - hrana pun: Yes that\n"
                " - hrana fact: Fun fact o hrani\n"
                " - ls memes: Seznam memov\n"
                " - /meme x: Specifičn meme\n"
                " - dump memez: Vsi memeji naenkrat\n"
                " - rnd meme: Random meme\n"
                " - /tone <x>: Lokalni LLM ki ti odgovori na <x>\n"
                " - resources: Obremenitev strežnika ki poganja bota\n"
                " - ping: pong\n"
                " - pong: ping\n"
                "...in še in še samo se nam ni dalo pisat\n"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from ourselves
        if message.author == self.bot.user:
            return

        content = message.content.strip()
        lower = content.lower()

        # 1) If they asked for help exactly, show help
        if lower == "help":
            return await message.channel.send(self.help_text)

        # 2) Otherwise see if they tried one of our known triggers
        for cmd in LOWER_COMMANDS:
            # simple startswith check; adjust as needed
            if lower.startswith(cmd):
                return  # let the other Cog handle it

        # 3) If it’s a single word (or at least first token), try a typo fix
        first = lower.split()[0]
        suggestions = difflib.get_close_matches(first, LOWER_COMMANDS, n=2, cutoff=0.75)
        if suggestions:
            # only suggest if the “distance” isn’t too big
            pretty = [COMMAND_MAP[m] for m in suggestions]
            note = ", ".join(f"`{p}`" for p in pretty)
            await message.channel.send(f"Did you mean: {note}")
        # else: ignore completely

        # # If the message starts with "help", send the help text
        # if message.content.lower().startswith("help"):
        #     await message.channel.send(self.help_text)


def setup(bot: commands.Bot):
    """Required for discord.py extension loading."""
    bot.add_cog(HelpCog(bot))
