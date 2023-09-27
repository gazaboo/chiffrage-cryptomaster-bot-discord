import discord
import os
from dotenv import load_dotenv
from utils import (sayHello, sendUserInfo,
                   cesar, vigenere,
                   DH_clientHello, DH_decodeMsg,
                   proveIdentity)

load_dotenv()
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(discord_msg):
    if discord_msg.author == client.user:
        return

    if discord_msg.content.startswith('$crypto'):
        cmd = discord_msg.content.split(" - ")[1:]
        fun = ""
        if len(cmd) == 0:
            await discord_msg.reply("Tu m'as parlé ? J'ai pas compris la question...")

        elif len(cmd) == 1:
            fun = cmd[0]

        else:
            fun, params = cmd[0], cmd[1:]

        if fun == 'sayHello':
            await sayHello(discord_msg)

        if fun == 'infos':
            await sendUserInfo(discord_msg)

        if fun == 'decodeCesar':
            await cesar(discord_msg, params, encode=-1)

        if fun == 'encodeCesar':
            await cesar(discord_msg, params, encode=1)

        if fun == 'encodeVigenere':
            await vigenere(discord_msg, params, encode=1)

        if fun == 'decodeVigenere':
            await vigenere(discord_msg, params, encode=-1)

        if fun == 'DH_clientHello':
            await DH_clientHello(discord_msg, params)

        if fun == 'DH_decodeMsg':
            await DH_decodeMsg(discord_msg, params)

        if fun == 'proveIdentity':
            await proveIdentity(discord_msg)

    return


client.run(os.getenv('TOKEN'))
