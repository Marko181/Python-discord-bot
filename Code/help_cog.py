# help_cog.py

import discord
from discord.ext import commands

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
                " - ls: Seznam memov\n"
                " - meme x: Specifičn meme\n"
                " - dump memez: Vsi memeji naenkrat\n"
                " - rndmeme: Random meme\n"
                " - tone <x>: Lokalni LLM ki ti odgovori na <x>\n"
                " - resources: Obremenitev strežnika ki poganja bota"
                "...in še in še samo se nam ni dalo pisat\n"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from ourselves
        if message.author == self.bot.user:
            return

        # If the message starts with "help", send the help text
        if message.content.lower().startswith("help"):
            await message.channel.send(self.help_text)


def setup(bot: commands.Bot):
    """Required for discord.py extension loading."""
    bot.add_cog(HelpCog(bot))
