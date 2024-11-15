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

bot_version = " v: 2.1.0" 
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
        elif message.content.startswith('menza') or message.content.startswith('Menza'):
            await message.channel.send(main_menza())
        
        # GIF - Perš (Kinder jajček)
        elif 'kinder jajček' in message.content.lower():
            await message.channel.send('https://media1.tenor.com/m/OD84C08uSMAAAAAd/world-war-z-chomp.gif')
        
        # GIF - Perš (CEF - Tyson)
        elif 'cef' in message.content.lower():
            gif_path = './files/cef.gif'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # GIF - DarkMode (Dark mode)
        elif 'dark mode' in message.content.lower():
            gif_path = './files/DarkMode.jpg'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # GIF - Koporec (koporec)
        elif 'koporec' in message.content.lower():
            gif_path = './files/koporec_meme.jpg'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # MEME - Mare (SkillIssue)
        elif 'skill issue' in message.content.lower():
            gif_path = './files/SkillIssue.png'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # Matlab - index (MatlabIndex)
        elif 'matlab' in message.content.lower():
            gif_path = './files/MatlabIndex.png'
            file = discord.File(gif_path)
            await message.channel.send(file=file)
        
        # Izpis imen
        elif 'whois' in message.content.lower():
            await message.channel.send(whois_table())
        
        # Spam tag
        elif 'spam' in message.content.lower():
            if message.author.id == user_ids[4]:
                gif_path = './files/ke_tip.png'
                file = discord.File(gif_path)
                await message.channel.send(file=file)
            else:
                # Extract everything after 'spam ' to get the user name
                nameTag = message.content[len('spam '):].strip()
                # Send name tag spam
                for i in range(10):
                    await message.channel.send(nameTag)
                    time.sleep(1)
        
        # Zipam ti mamo
        elif 'zip' in message.content.lower():
            await message.channel.send('MA ZIPAM TI MAMO')

        # Random meme iz mape "files"
        elif 'meme' in message.content.lower() or 'jazjaz' in message.content.lower(): 
            files = [f for f in os.listdir("./files") if os.path.isfile(os.path.join("./files", f)) and not f.endswith(".txt")]
            
            # Check if there are any valid files to choose from
            if files:
                file_path = os.path.join("./files", random.choice(files))
                file = discord.File(file_path)
                await message.channel.send(file=file)
            else:
                await message.channel.send("Nism najdu mema :(")

        
        # Hrana na bone
        elif message.content.startswith('hrana'):
            # Extract everything after 'hrana ' to get the restaurant name
            restaurant_name = message.content[len('hrana '):].strip()
            # Call your get_menu function with the extracted restaurant name
            menu = main_restaurant(restaurant_name)
            # Send the resulting menu back to the channel
            await message.channel.send(menu)
        
        ######### !!! DANGEROUS ZONE - Update !!! #########
        elif message.content.startswith('BotUpdateNow'):
            if message.author.id == user_ids[0] or message.author.id == user_ids[1] or message.author.id == user_ids[2] or message.author.id == user_ids[3] or message.author.id == user_ids[4]:
                update.bot_git_update()
            else:
                await message.channel.send('Ja ne nč ne bo')
            
        
        # Status sporočilo
        elif 'status' in message.content.lower():
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
