"""
Author: Bc. Simon Youssef
Coppyright 2022 All Rights Reserved.
Discord bot for showing sourcebans on discord.
"""

import datetime
import json
import urllib.request
import keep_alive
import discord
from steam import steamid
from steamid_converter import Converter


client = discord.Client()


class Ban(object):
    """The Ban class."""

    def __init__(self):
        """"The constructor for Ban class."""

        self.name = str()
        self.reason = str()
        self.admin = str()
        self.steamID = str()
        self.length = int()
        self.date = int()


@client.event
async def on_ready():
    """The event to check if the bot is logged in."""

    print("Working {0.user}".format(client))


@client.event
async def on_message(message):
    """The event to chat command detection and reply."""

    user_message = str(message.content)

    if message.author == client.user:
        return
    embed = discord.Embed()
    embed.description = ""
    line = user_message.split(' ')
    ban_info = Ban()

    if line[0].lower() == '!getban' and len(line) == 2:
        steamID = convert_steamid(line[1])
        ban = await get_json(
            f"{WEBSITE}?steamId={steamID}",
            message, embed)

        if not ban:
            return

        await get_data(ban, ban_info)
        embed.description += get_message(ban_info)
        await message.channel.send(embed=embed)

    elif line[0].lower() == '!getbanip' and len(line) == 2:
        ip = line[1]
        bans = await get_json(
            f"{WEBSITE}?ip={ip}",
            message, embed)

        if not bans:
            return

        for ban in bans:
            await get_data(ban, ban_info)
            embed.description += get_message(ban_info)
        await message.channel.send(embed=embed)

    elif line[0].lower() == '!steamid' and len(line) == 2:
        steamID = get_steamid(line[1])
        if (steamID):
            steamID = convert_steamid(steamID)
            embed.description += (f'**SteamID:** {steamID}')
        else:
            embed.description += (f'**SteamID not Found**')
        await message.channel.send(embed=embed)

    return


async def get_json(link, message, embed):
    """The function to get json from website."""

    try:
        with urllib.request.urlopen(link) as url:
            try:
                bans = json.loads(url.read().decode())
            except json.decoder.JSONDecodeError:
                embed.description += "**Ban not found**"
                await message.channel.send(embed=embed)
                return

    except urllib.error.HTTPError as err:
        if err.code == 404:
            embed.description += "**Ban not found**"
            await message.channel.send(embed=embed)
            return
        return

    return bans


async def get_data(data, ban_info):
    """The function to get information about ban from data."""

    ban_info.name = str(data["name"])
    ban_info.reason = str(data["reason"])
    ban_info.admin = str(data["user"])
    ban_info.steamID = str(data["authid"])
    ban_info.length = int(data["length"])
    ban_info.date = get_human_time(data["created"])
    return ban_info


def get_message(ban_info):
    """"The function to get message about ban."""

    mess = (
        f' [View on Sourcebans]({SOURCEBANS}{ban_info.steamID})\n'
        f'**Name:** {ban_info.name}\n'
        f'**Reason:** {ban_info.reason}\n'
        f'**Admin:** {ban_info.admin}\n'
        f'**SteamID:** {ban_info.steamID}\n'
        '**Lenght:** {len}'.format(
            len="Perma ban" if ban_info.length == 0 else convert_time(
                ban_info.length)))
    mess += (
        f'\n**Invoked on:** {ban_info.date}'
        f'\n**Steam Profile:** [Link](https://steamcommunity.com/profiles/{Converter.to_steamID3(ban_info.steamID)})'
        f'\n\n\n')
    return mess


def get_human_time(unix_time):
    """"The function for converting unix time to human datetime."""

    return datetime.datetime.fromtimestamp(int(unix_time)).strftime(
        '%d-%m-%Y %H:%M:%S')


def convert_time(time):
    """"The function for converting seconds to datetime."""

    return str(datetime.timedelta(seconds=time))


def get_steamid(user_link):
    """"The function for converting steam profile link to steamID."""

    steamID64 = steamid.steam64_from_url(f'{user_link}')
    if (steamID64):
        return Converter.to_steamID(steamID64)
    return


def convert_steamid(steamID):
    """"The function for converting steamID to correct form."""

    return steamID.replace("STEAM_0", "STEAM_1")


TOKEN = 'YOUR DISCORD BOT TOKEN'
SOURCEBANS = 'YOUR SOURCEBANS WEBSITE'
WEBSITE = 'YOUR REST API WEBSITE'
keep_alive.keep_alive()
client.run(TOKEN)
