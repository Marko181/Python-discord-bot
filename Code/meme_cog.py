# meme_cog.py

import sys
import os
import random
import asyncio
import aiohttp
import logging

import discord
from discord.ext import commands

# Ensure we can import BotConfig
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Classified')))

CLASSIFIED_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "Classified")
)
sys.path.insert(0, CLASSIFIED_PATH)
from classified import BotConfig


# Scheduled task: send a random meme/image
async def send_random_image(bot: commands.Bot):
    """
    Scheduled job: pick a random image from the meme folder
    and post it in the class memes channel.
    """
    channel = bot.get_channel(BotConfig.CHANNEL_ID_CLASSMEMES)
    if not channel:
        logging.warning("send_random_image: channel not found")
        return

    try:
        files = [
            f for f in os.listdir(BotConfig.MEME_FOLDER)
            if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))
        ]
        if not files:
            await channel.send("No images found in the folder.")
            return

        choice = random.choice(files)
        path = os.path.join(BotConfig.MEME_FOLDER, choice)
        await channel.send(file=discord.File(path))

    except Exception as e:
        logging.exception("Error in send_random_image")
        err = f"Error occurred in send_random_image: {e}"
        if len(err) >= 2000:
            err = err[:1996] + "..."
        await channel.send(err)


class MemeCog(commands.Cog):
    """
    Cog for all meme-related listeners:
      - keyword GIFs and images
      - spam tag
      - meme <name>
      - ls, rnd meme, dump memez
      - saving uploaded memes
      - deleting memes
      - fun one-off keywords (cef, skill issue, matlab, koporec, jon, joo/joj)
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore the bot's own messages
        if message.author == self.bot.user:
            return

        content = message.content
        lower = content.lower()

        # Kinder jajček GIF
        if 'kinder jajček' in lower and random.random() < 0.1:
            return await message.channel.send('https://media1.tenor.com/m/OD84C08uSMAAAAAd/world-war-z-chomp.gif')

        # LaTeX suggestion
        # if ' latex' in lower:
        #     return await message.channel.send(r'Ste morda mislisi "/latex \LaTeX"?')

        # Spam tag: repeat the tag 10× with 1s delay
        if lower.startswith('spam '):
            name_tag = content[len('spam '):].strip()
            try:
                await message.delete()
            except Exception:
                pass
            for _ in range(10):
                await message.channel.send(name_tag)
                await asyncio.sleep(1)
            return

        # Ke Tip meme
        if 'ke tip' in lower:
            try:
                await message.delete()
            except discord.Forbidden:
                pass
            path = os.path.join(BotConfig.MEME_FOLDER, 'ke_tip.png')
            if os.path.exists(path):
                return await message.channel.send(file=discord.File(path))
            else:
                return await message.channel.send("Error: File not found.")

        # Zipam ti mamo (10% chance)
        if 'zip' in lower and random.random() < 0.1:
            return await message.channel.send('MA ZIPAM TI MAMO')

        # Specific meme: "meme <name>"
        if lower.startswith('meme '):
            # e.g. "meme foo" → "foo.png"/jpg/gif
            file_key = content[len('meme '):].strip()
            try:
                await message.delete()
            except Exception:
                pass

            for ext in ('.png', '.jpg', '.jpeg', '.gif'):
                candidate = os.path.join(BotConfig.MEME_FOLDER, file_key + ext)
                if os.path.exists(candidate):
                    return await message.channel.send(file=discord.File(candidate))
            return await message.channel.send("Nism najdu mema :(")

        # One-off keyword memes
        if 'cef' in lower:
            return await message.channel.send(file=discord.File(os.path.join(BotConfig.MEME_FOLDER, 'cef.gif')))
        if 'skill issue' in lower:
            return await message.channel.send(file=discord.File(os.path.join(BotConfig.MEME_FOLDER, 'SkillIssue.png')))
        if 'matlab' in lower and random.random() < 0.1:
            return await message.channel.send(file=discord.File(os.path.join(BotConfig.MEME_FOLDER, 'MatlabIndex.png')))
        if ('koporc' in lower or 'koporec' in lower) and random.random() < 0.1:
            return await message.channel.send(file=discord.File(os.path.join(BotConfig.MEME_FOLDER, 'koporec_meme.jpg')))
        if 'jon' in lower and random.random() < 0.1:
            return await message.channel.send(file=discord.File(os.path.join(BotConfig.MEME_FOLDER, 'minijon.gif')))
        if 'joo' in lower or 'joj' in lower:
            return await message.channel.send(file=discord.File(os.path.join(BotConfig.MEME_FOLDER, 'jooj.jpg')))

        # List available memes
        if lower.startswith('ls'):
            files = [
                os.path.splitext(f)[0]
                for f in os.listdir(BotConfig.MEME_FOLDER)
                if os.path.isfile(os.path.join(BotConfig.MEME_FOLDER, f))
            ]
            if files:
                await message.channel.send("Memes available just for you:\n" + "\n".join(files))
            else:
                await message.channel.send("No files found.")
            return

        # Random meme on demand
        if 'rnd meme' in lower or 'jazjaz' in lower:
            images = [
                f for f in os.listdir(BotConfig.MEME_FOLDER)
                if os.path.isfile(os.path.join(BotConfig.MEME_FOLDER, f))
                   and f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))
            ]
            if images:
                choice = random.choice(images)
                return await message.channel.send(file=discord.File(os.path.join(BotConfig.MEME_FOLDER, choice)))
            else:
                return await message.channel.send("Nism najdu mema :(")

        # Dump all memes
        if 'dump memez' in lower:
            chan = message.channel
            if chan.id == BotConfig.CHANNEL_ID_CLASSMEMES:
                images = [
                    f for f in os.listdir(BotConfig.MEME_FOLDER)
                    if os.path.isfile(os.path.join(BotConfig.MEME_FOLDER, f))
                       and f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))
                ]
                for img in images:
                    await chan.send(file=discord.File(os.path.join(BotConfig.MEME_FOLDER, img)))
                    await asyncio.sleep(1)
            else:
                mention = f"<#{BotConfig.CHANNEL_ID_CLASSMEMES}>"
                await chan.send(f"Ne bo šlo, probej v {mention}")
            return

        # Save new memes when attached
        if message.attachments and message.channel.id == BotConfig.CHANNEL_ID_CLASSMEMES:
            for attachment in message.attachments:
                if attachment.content_type and attachment.content_type.startswith('image/'):
                    fname = attachment.filename
                    dest = os.listdir(BotConfig.MEME_FOLDER)
                    if fname not in dest:
                        await message.channel.send(
                            "Ta meme še ni shranjen, ga želiš shraniti? (ja, ja ime_slike, ne)"
                        )

                        def check(resp: discord.Message):
                            ok = resp.author == message.author and resp.channel == message.channel
                            return ok and (
                                resp.content.lower() == "ne" or
                                resp.content.lower().startswith("ja")
                            )

                        try:
                            resp = await self.bot.wait_for("message", check=check, timeout=30)
                            text = resp.content.lower()
                            if text.startswith("ja"):
                                # custom name after "ja "
                                custom = resp.content[3:].strip()
                                base, ext = os.path.splitext(attachment.filename)
                                new_name = (custom + ext) if custom else attachment.filename
                                path = os.path.join(BotConfig.MEME_FOLDER, new_name)
                                # download
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(attachment.url) as r:
                                        if r.status == 200:
                                            data = await r.read()
                                            with open(path, "wb") as f:
                                                f.write(data)
                                await message.channel.send(f"Saved {new_name} to {BotConfig.MEME_FOLDER}!")
                            else:
                                await message.channel.send("Ne bom shranil slike.")
                        except asyncio.TimeoutError:
                            await message.channel.send("Čas je potekel, slika ne bo shranjena.")
            return

        # Delete existing meme
        if lower.startswith('delete meme '):
            if message.author.id in BotConfig.USER_IDS:
                key = content[len('delete meme '):].strip()
                matches = [
                    f for f in os.listdir(BotConfig.MEME_FOLDER)
                    if os.path.isfile(os.path.join(BotConfig.MEME_FOLDER, f))
                       and os.path.splitext(f)[0] == key
                ]
                if matches:
                    path = os.path.join(BotConfig.MEME_FOLDER, matches[0])
                    try:
                        os.remove(path)
                        await message.channel.send(f"Meme {key} deleted!")
                    except Exception as e:
                        logging.exception("Failed to delete meme")
                        await message.channel.send(f"Error deleting {key}: {e}")
                else:
                    await message.channel.send(f"Meme {key} not found in {BotConfig.MEME_FOLDER}.")
            else:
                await message.channel.send("Ja ne nč ne bo")
            return


def setup(bot: commands.Bot):
    """discord.py extension hook."""
    bot.add_cog(MemeCog(bot))
