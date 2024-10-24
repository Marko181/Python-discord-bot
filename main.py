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

#print(main_menza())
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

async def send_menza_message():
    channel = client.get_channel(YOUR_CHANNEL_ID)
    if channel:
        await channel.send(main_menza())
    else:
        print("Channel not found")

def bot_help():
    pomoc = 'Ukazi, ki so na voljo:\n   menza - si lačn in na FE-ju\n    whois - izpiše IRL ime uporabnika\n    hrana x - izpis menija restavracije na bone (x - ustavi ime restavracije)\n  hrana random - ko res neveš kaj bi jedu\n   hrana pun - yes that\n  hrana fact - fun fact o hrani\n  ...in še in še samo se nam ni dalo pisat\n'
    return pomoc

# Se proži ob zagonu da se logina v server
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# PRoženje ob določeni uri
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Schedule the task
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_menza_message, 'cron', day_of_week='mon-fri', hour=10, minute=0, month='1-5,10-12')
    #scheduler.add_job(send_menza_message, 'interval', minutes=3)
    scheduler.start()

# Proženje ob pingu
@client.event
async def on_message(message):

    ### Filter its own message ###
    if message.author.name == 'FeBot':
        print('Message by:', message.author.name, 'restricted!')
        return

    ### Help ###
    elif message.content.startswith('help'):
        await message.channel.send(bot_help())

    ### Menza ###
    elif message.content.startswith('menza') or message.content.startswith('Menza'):
        await message.channel.send(main_menza())

    ### GIF - Perš (Kinder jajček) ###
    elif 'kinder jajček' in message.content.lower():
        await message.channel.send('https://media1.tenor.com/m/OD84C08uSMAAAAAd/world-war-z-chomp.gif')

    ### GIF - Perš (CEF - Tyson) ###
    elif 'cef' in message.content.lower():
        gif_path = './files/cef.gif'
        file = discord.File(gif_path)
        await message.channel.send(file=file)

    ### GIF - DarkMode (Dark mode) ###
    elif 'dark mode' in message.content.lower():
        gif_path = './DarkMode.jpg'
        file = discord.File(gif_path)
        await message.channel.send(file=file)

    ### GIF - Koporec (koporec) ###
    elif 'koporec' in message.content.lower():
        gif_path = './files/koporec_meme.jpg'
        file = discord.File(gif_path)
        await message.channel.send(file=file)

    ### MEME - Mare (SkillIssue) ###
    elif 'skill issue' in message.content.lower():
        gif_path = './files/SkillIssue.png'
        file = discord.File(gif_path)
        await message.channel.send(file=file)

    ### Matlab - index (MatlabIndex) ###
    elif 'matlab' in message.content.lower():
        gif_path = './files/MatlabIndex.png'
        file = discord.File(gif_path)
        await message.channel.send(file=file)

    ### Izpis imen ###
    elif 'whois' in message.content.lower():
        await message.channel.send(whois_table())

    ### Spam tag ###
    elif 'spam' in message.content.lower():
        # Extract everything after 'spam ' to get the user name
        nameTag = message.content[len('spam '):].strip()
        # Send name tag spam
        for i in range(10):
            await message.channel.send(nameTag)
            time.sleep(1)
        
    ### Hrana na bone ###
    elif message.content.startswith('hrana'):
        # Extract everything after 'hrana ' to get the restaurant name
        restaurant_name = message.content[len('hrana '):].strip()
        # Call your get_menu function with the extracted restaurant name
        menu = main_restaurant(restaurant_name)
        # Send the resulting menu back to the channel
        await message.channel.send(menu)

    ######### !!! DANGEROUS ZONE - Update !!! #########
    elif message.content.startswith('BotUpdateNow'):
        update.bot_git_update()
        #await message.channel.send("Updating...")

    elif 'status' in message.content.lower():
        response = "Awake and alive!"
        await message.channel.send(response)


    message.content = ""

# BotKey v ločeni mapi
keypath = "./BotKey.txt"
with open(keypath, 'r') as file:
    key = file.readline().strip()

# Channel ID v ločeni mapi
keypath = "./ChannelID.txt"
with open(keypath, 'r') as file:
    YOUR_CHANNEL_ID = file.readline().strip()

client.run(key)
