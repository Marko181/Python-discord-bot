import discord
import os
import numpy as np
from menza import * 
from whois import *
from hrana import *
import update
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
import subprocess
import random
import aiohttp
import asyncio

# Version control naj bi bil avtomatski
bot_version = " v: 2.3.15" 
# Channel ID v ločeni datoteki
channelID, channelID_BP, channelID_CM = 0, 0, 0
# User ID v ločeni datoteki
user_ids = [0,0,0,0,0]
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

meme_folder = './files/memes/'

# Funkcija za pošiljanje sporočila z menzami
async def send_menza_message():
    try:
        channel = client.get_channel(channelID)
        if channel:
            await channel.send(main_menza())
        else:
            print("Channel not found")
    except Exception as e:
        await channel.send(f"Error occurred in send_menza_message: {e}")

# Funkcija za pomoč z ukazi
def bot_help():
    pomoc = 'Ukazi, ki so na voljo:\n   menza - si lačn in na FE-ju\n    whois - izpiše IRL ime uporabnika\n    hrana x - izpis menija restavracije na bone (x - ustavi ime restavracije)\n  hrana random - ko res neveš kaj bi jedu\n   hrana pun - yes that\n  hrana fact - fun fact o hrani\n ls - seznam memov\n meme x - specifičn meme\n dump memez - vsi memeji naenkrat\n  ...in še in še samo se nam ni dalo pisat\n'
    return pomoc

# Se proži ob zagonu da se logina v server
@client.event
async def on_ready():
    try:
        # Get the channel
        channel = client.get_channel(channelID_BP)
        
        # Check if the channel exists and send a startup message
        if channel:
            msg = "Alive and ready!" + bot_version
            await channel.send(msg)

            # Check for errorReport.txt
            error_file_path = "./errorReport.txt"  # Adjust the path if needed
            if os.path.exists(error_file_path):
                with open(error_file_path, 'r') as error_file:
                    error_content = error_file.read().strip()  # Read file content and strip any trailing whitespace
                    
                # Suppress specific message
                if len(error_content) > 220:
                    # Send the contents of the error report
                    await channel.send(f"Error Report Found:\n```\n{error_content}\n```")
        else:
            print("Target channel not found")

        print(f'Logged in as {client.user}')
        # Proženje ob določeni uri
        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_menza_message, 'cron', day_of_week='mon-fri', hour=10, minute=0, month='1-5,10-12')
        scheduler.start()

    except Exception as e:
        await channel.send(f"An error occurred: {e}")

# Proženje ob pingu
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        # Ukaz za pomoč
        if message.content.startswith('help'):
            await message.channel.send(bot_help())
        
        # Menza
        if message.content.startswith('menza') or message.content.startswith('Menza'):
            await message.channel.send(main_menza())
        
        # GIF - Perš (Kinder jajček)
        if 'kinder jajček' in message.content.lower():
            await message.channel.send('https://media1.tenor.com/m/OD84C08uSMAAAAAd/world-war-z-chomp.gif')
                # LaTeX reply
        elif ' latex' in message.content.lower():
            await message.channel.send(r'Ste morda mislisi "/latex \LaTeX"?')

        # Izpis imen
        if 'whois' in message.content.lower():
            await message.channel.send(whois_table())
        
        # Spam tag
        if message.content.lower().startswith('spam'):
            # Extract everything after 'spam ' to get the user name
            nameTag = message.content[len('spam '):].strip()
            await message.delete()
            # Send name tag spam
            for i in range(10):
                await message.channel.send(nameTag)
                time.sleep(1)
        
        # Hello
        if 'hello bot' in message.content.lower() or 'helo bot' in message.content.lower():
            await message.channel.send(f"Hello {message.author.mention}")
        
        # Ke Tip
        if 'ke tip' in message.content.lower():
            try:
                await message.delete()  # Deletes the message
                gif_path = meme_folder + 'ke_tip.png'
                file = discord.File(gif_path)  # Loads the file
                await message.channel.send(file=file)  # Sends the file
            except FileNotFoundError:
                await message.channel.send("Error: File not found.")
            except discord.Forbidden:
                await message.channel.send("Error: Missing permissions to delete messages.")
        
        # Zipam ti mamo
        if 'zip' in message.content.lower():
            if random.random() < 0.1:
                await message.channel.send('MA ZIPAM TI MAMO')

        # Specific meme
        if message.content.lower().startswith('meme'):
            file_name = message.content[len('meme '):].strip()
            await message.delete()
            
            if file_name:
                # List of allowed extensions
                allowed_extensions = ['.png', '.jpg', '.gif']
                file_path = None
                
                # Check for the file with any of the allowed extensions
                for ext in allowed_extensions:
                    potential_path = os.path.join(meme_folder, file_name + ext)
                    if os.path.exists(potential_path):
                        file_path = potential_path
                        break
                
                if file_path:
                    file = discord.File(file_path)
                    await message.channel.send(file=file)
                else:
                    await message.channel.send("Nism najdu mema :(")
            else:
                await message.channel.send("Nism najdu mema :(")

        # GIF - Perš (CEF - Tyson)
        elif 'cef' in message.content.lower():
            gif_path = meme_folder + 'cef.gif'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # MEME - Mare (SkillIssue)
        elif 'skill issue' in message.content.lower():
            gif_path = meme_folder + 'SkillIssue.png'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # Matlab - index (MatlabIndex)
        elif 'matlab' in message.content.lower():
            gif_path = meme_folder + 'MatlabIndex.png'
            file = discord.File(gif_path)
            await message.channel.send(file=file)

        elif 'koporc' in message.content.lower() or 'koporec' in message.content.lower():
            gif_path = meme_folder + 'koporec_meme.jpg'
            file = discord.File(gif_path)
            await message.channel.send(file=file)

        # Minijon
        elif 'jon' in message.content.lower():
            gif_path = meme_folder + 'minijon.gif'
            file = discord.File(gif_path)
            await message.channel.send(file=file)

        # JOOOOOOJ
        elif 'joo' in message.content.lower() or 'joj' in message.content.lower():
            gif_path = meme_folder + 'jooj.jpg'
            file = discord.File(gif_path)
            await message.channel.send(file=file)

        # Meme list
        if message.content.lower().startswith('ls'):
            files = [
                os.path.splitext(f)[0]  # Remove the extension from the file name
                for f in os.listdir(meme_folder)
                if os.path.isfile(os.path.join(meme_folder, f))
            ]
            if files:
                file_list = "\n".join(files)  # Join file names with a newline for better formatting
                await message.channel.send(f"Memes available just for you:\n{file_list}")
            else:
                await message.channel.send("No files found.")

        # Random meme iz mape "files"
        if 'rnd meme' in message.content.lower() or 'jazjaz' in message.content.lower(): 
            files = [f for f in os.listdir(meme_folder) if os.path.isfile(os.path.join("./files", f)) and not f.endswith(".txt")]
            
            # Check if there are any valid files to choose from
            if files:
                file_path = os.path.join(meme_folder, random.choice(files))
                file = discord.File(file_path)
                await message.channel.send(file=file)
            else:
                await message.channel.send("Nism najdu mema :(")

        # Send all them memez
        if 'dump memez' in message.content.lower():
            if message.channel.id == channelID_CM:
                files = [
                    os.path.join(meme_folder, f)  # Full path to the file
                    for f in os.listdir(meme_folder)
                    if os.path.isfile(os.path.join(meme_folder, f)) and not f.endswith(".txt")
                ]
                
                if files:
                    for file_path in files:
                        # Send each file one by one
                        file = discord.File(file_path)
                        await message.channel.send(file=file)
                        time.sleep(1)
                else:
                    await message.channel.send("No files found.")
            else:
                channel_mention = f"<#{channelID_CM}>"
                await message.channel.send(f"Ne bo šlo, probej v {channel_mention}")
        
        # Save new meme
        # Check if the message has attachments (e.g., uploaded images)
        if message.attachments:
            if message.channel.id == channelID_CM:
                for attachment in message.attachments:
                    if attachment.content_type and attachment.content_type.startswith('image/'):
                        # Check if the file already exists
                        sent_file_name = attachment.filename
                        is_existing = sent_file_name in os.listdir(meme_folder)

                        if not is_existing:
                            await message.channel.send(f"Ta meme še ni shranjen, ga želiš shraniti? (ja, ja ime_slike, ne)")

                        def check(msg):
                            return (
                                msg.author == message.author
                                and msg.channel == message.channel
                                and (msg.content.lower() == "ja" or msg.content.lower().startswith("ja ") or msg.content.lower() == "ne")
                            )

                        try:
                            response = await client.wait_for("message", check=check, timeout=30)  # Wait for 30 seconds
                            if response.content.lower().startswith("ja"):
                                # Check if a custom name is provided
                                custom_name = response.content[3:].strip()  # Extract everything after "ja "
                                if custom_name:
                                    # Get the file extension from the original filename
                                    _, file_extension = os.path.splitext(attachment.filename)
                                    file_name = f"{custom_name}{file_extension}"  # Combine custom name and extension
                                else:
                                    # Use the original filename
                                    file_name = attachment.filename

                                # Construct the file path
                                file_path = os.path.join(meme_folder, file_name)

                                # Download and save the image
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(attachment.url) as response:
                                        if response.status == 200:
                                            with open(file_path, 'wb') as f:
                                                f.write(await response.read())

                                await message.channel.send(f"Saved {file_name} to {meme_folder}!")
                            else:
                                await message.channel.send("Ne bom shranil slike.")
                        except asyncio.TimeoutError:
                            await message.channel.send("Čas je potekel, slika ne bo shranjena.")

                
        # Delete existing meme
        if 'delete meme ' in message.content.lower():
            if message.author.id == user_ids[0] or message.author.id == user_ids[1] or message.author.id == user_ids[2] or message.author.id == user_ids[3] or message.author.id == user_ids[4]:
                # Extract the file name after "delete meme "
                meme_name = message.content[len('delete meme '):].strip()
                
                # Look for the file in the folder
                files = [
                    f for f in os.listdir(meme_folder)
                    if os.path.isfile(os.path.join(meme_folder, f)) and os.path.splitext(f)[0] == meme_name
                ]
                
                if files:
                    # Get the full path of the file
                    file_to_delete = os.path.join(meme_folder, files[0])
                    
                    # Delete the file
                    os.remove(file_to_delete)
                    
                    # Send confirmation to the Discord channel
                    await message.channel.send(f"Meme {meme_name} deleted!")
                else:
                    # If the file was not found
                    await message.channel.send(f"Meme {meme_name} not found in {meme_folder}.")
            else:
                await message.channel.send('Ja ne nč ne bo')
  
        # Hrana na bone
        if message.content.lower().startswith('hrana'):
            # Extract everything after 'hrana ' to get the restaurant name
            restaurant_name = message.content[len('hrana '):].strip()
            # Call your get_menu function with the extracted restaurant name
            menu = main_restaurant(restaurant_name)
            # Send the resulting menu back to the channel
            await message.channel.send(menu)
        
        ######### !!! DANGEROUS ZONE - Update !!! #########
        if message.content.startswith('BotUpdateNow'):
            if message.author.id == user_ids[0] or message.author.id == user_ids[1] or message.author.id == user_ids[2] or message.author.id == user_ids[3] or message.author.id == user_ids[4]:
                update.bot_git_update()
            else:
                await message.channel.send('Ja ne nč ne bo')
            
        
        # Status sporočilo
        if 'status' in message.content.lower():
            response = "Awake and alive!" + bot_version
            await message.channel.send(response)

    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")

############ START BOT ############
if __name__ == "__main__":
    # Channel ID v ločeni mapi
    id_path1 = "./Classified/ChannelID.txt"
    with open(id_path1, 'r') as file:
        channelID = int(file.readline().strip())
        print(channelID)

    id_path2 = "./Classified/ChannelID_BP.txt"
    with open(id_path2, 'r') as file:
        channelID_BP = int(file.readline().strip())
        print(channelID_BP)

    id_path3 = "./Classified/sudo_users.txt"
    with open(id_path3, 'r') as file:
        user_ids = [int(line.strip()) for line in file.readlines()]
        print(user_ids)

    id_path4 = "./Classified/ChannelID_CM.txt"
    with open(id_path4, 'r') as file:
        channelID_CM = int(file.readline().strip())
        print(channelID_BP)

    # BotKey v ločeni mapi
    keypath = "./Classified/BotKey.txt"
    with open(keypath, 'r') as file:
        key = file.readline().strip()

    client.run(key)
