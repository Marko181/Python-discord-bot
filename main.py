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

bot_version = " v: 2.1.3" 
# Channel ID v ločeni datoteki
channelID = 0
channelID_BP = 0
# User ID v ločeni datoteki
user_ids = [0,0,0,0,0]
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

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
    pomoc = 'Ukazi, ki so na voljo:\n   menza - si lačn in na FE-ju\n    whois - izpiše IRL ime uporabnika\n    hrana x - izpis menija restavracije na bone (x - ustavi ime restavracije)\n  hrana random - ko res neveš kaj bi jedu\n   hrana pun - yes that\n  hrana fact - fun fact o hrani\n  ...in še in še samo se nam ni dalo pisat\n'
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
        
        # GIF - Perš (CEF - Tyson)
        if 'cef' in message.content.lower():
            gif_path = './files/cef.gif'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # GIF - DarkMode (Dark mode)
        if 'dark mode' in message.content.lower():
            gif_path = './files/DarkMode.jpg'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # GIF - Koporec (koporec)
        if 'koporec' in message.content.lower():
            gif_path = './files/koporec_meme.jpg'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # MEME - Mare (SkillIssue)
        if 'skill issue' in message.content.lower():
            gif_path = './files/SkillIssue.png'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # Matlab - index (MatlabIndex)
        if 'matlab' in message.content.lower():
            gif_path = './files/MatlabIndex.png'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # Izpis imen
        if 'whois' in message.content.lower():
            await message.channel.send(whois_table())
        
        # Spam tag
        if 'spam' in message.content.lower():
            # Extract everything after 'spam ' to get the user name
            nameTag = message.content[len('spam '):].strip()
            await message.delete()
            # Send name tag spam
            for i in range(10):
                await message.channel.send(nameTag)
                time.sleep(1)
        
        # Ke Tip
        if 'ke tip' in message.content.lower():
            try:
                await message.delete()  # Deletes the message
                gif_path = './files/ke_tip.png'
                file = discord.File(gif_path)  # Loads the file
                await message.channel.send(file=file)  # Sends the file
            except FileNotFoundError:
                await message.channel.send("Error: File not found.")
            except discord.Forbidden:
                await message.channel.send("Error: Missing permissions to delete messages.")


        # Minijon
        if 'jon' in message.content.lower():
            gif_path = './files/minijon.gif'
            file = discord.File(gif_path)
            await message.channel.send(file=file)

        # JOOOOOOJ
        if 'joo' in message.content.lower() or 'joj' in message.content.lower():
            gif_path = './files/jernej.jpg'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # Zipam ti mamo
        if 'zip' in message.content.lower():
            await message.channel.send('MA ZIPAM TI MAMO')

        # Specific meme
        if message.content.startswith('meme'):
            file_name = message.content[len('meme '):].strip()
            await message.delete()
            if file_name:
                file_path = os.path.join("./files/", file_name)
                file = discord.File(file_path)
                await message.channel.send(file=file)
            else:
                await message.channel.send("Nism najdu mema :(")


        # Meme list
        if 'list meme' in message.content.lower():
            files = [f for f in os.listdir("./files") if os.path.isfile(os.path.join("./files", f)) and not f.endswith(".txt")]
            if files:
                file_list = "\n".join(files)  # Join file names with a newline for better formatting
                await message.channel.send(f"Files:\n{file_list}")
            else:
                await message.channel.send("No files found.")


        # Random meme iz mape "files"
        if 'random meme' in message.content.lower() or 'jazjaz' in message.content.lower(): 
            files = [f for f in os.listdir("./files") if os.path.isfile(os.path.join("./files", f)) and not f.endswith(".txt")]
            
            # Check if there are any valid files to choose from
            if files:
                file_path = os.path.join("./files", random.choice(files))
                file = discord.File(file_path)
                await message.channel.send(file=file)
            else:
                await message.channel.send("Nism najdu mema :(")

        
        # Hrana na bone
        if message.content.startswith('hrana'):
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

    # BotKey v ločeni mapi
    keypath = "./Classified/BotKey.txt"
    with open(keypath, 'r') as file:
        key = file.readline().strip()

    client.run(key)
