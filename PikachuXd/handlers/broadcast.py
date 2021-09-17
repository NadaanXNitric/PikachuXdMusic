# Copyright (C) 2021 By SankiProject
# Originally written by nitric on github
# Broadcast function


import asyncio

from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant

from callsmusic.callsmusic import client as veez
from config import SUDO_USERS

@Client.on_message(filters.command(["gcast"]))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("`Pɪᴋᴀ Pɪᴋᴀ, Sᴛᴀʀᴛᴇᴅ Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ...`")
        if not message.reply_to_message:
            await wtf.edit("Pɪᴋᴀ Pɪᴋᴀ, Pʟᴇᴀsᴇ Rᴇᴘʟʏ Tᴏ A Mᴇssᴀɢᴇ Tᴏ Sᴛᴀʀᴛ Bʀᴏᴀᴅᴄᴀsᴛ.")
            return
        lmao = message.reply_to_message.text
        async for dialog in veez.iter_dialogs():
            try:
                await veez.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"`Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴘʟᴢ ᴡᴀɪᴛ...` \n\n**Sᴇɴᴛ Tᴏ :** `{sent}` Cʜᴀᴛs. \n**Fᴀɪʟᴇᴅ Iɴ :** {failed} Cʜᴀᴛs.")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await message.reply_text(f"`Pɪᴋᴀ Pɪᴋᴀ, Gᴄᴀsᴛ Sᴜᴄᴄᴇsғᴜʟʟʏ` \n\n**Sᴇɴᴛ Tᴏ :** `{sent}` Cʜᴀᴛs. \n**Fᴀɪʟᴇᴅ Iɴ :** {failed} Cʜᴀᴛs.")
