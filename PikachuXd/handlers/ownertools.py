import sys
import os
import time
import traceback
import asyncio
import shutil
import psutil

from pyrogram import Client, filters
from pyrogram.types import Message, Dialog, Chat
from pyrogram.errors import UserAlreadyParticipant
from datetime import datetime
from functools import wraps
from os import environ, execle, path, remove

from PikachuXd.callsmusic.callsmusic import client as pakaya
from PikachuXd.helpers.database import db
from PikachuXd.helpers.dbtools import main_broadcast_handler
from PikachuXd.helpers.decorators import sudo_users_only
from PikachuXd.handlers.song import humanbytes, get_text
from PikachuXd.config import BOT_USERNAME, OWNER_ID, SUDO_USERS, GROUP_SUPPORT


# Stats Of Your Bot
@Client.on_message(filters.command("stats"))
@sudo_users_only
async def botstats(_, message: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await message.reply_text(
        text=f"**📊 Sᴛᴀᴛs Oғ @{BOT_USERNAME}**. \n\n**🤖 Bᴏᴛ Vᴇʀsɪᴏɴ :** `v3.0` \n\n**🙎🏼 Usᴇʀs :** \n » **Usᴇʀs Oɴ PM :** `{total_users}` \n\n**💾 Dɪsᴋ Usᴀɢᴇ** \n » **Dɪsᴋ Sᴘᴀᴄᴇ :** `{total}` \n » **Usᴇᴅ :** `{used}({disk_usage}%)` \n » **Fʀᴇᴇ :** `{free}` \n\n**🎛 Hᴀʀᴅᴡᴀʀᴇ Usᴀɢᴇ** \n » **CPU Usᴀɢᴇ :** `{cpu_usage}%` \n » **RAM Usᴀɢᴇ :** `{ram_usage}%`",
        parse_mode="Markdown",
        quote=True
    )



@Client.on_message(filters.private & filters.command("broadcast") & filters.user(OWNER_ID) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)


# Ban User
@Client.on_message(filters.private & filters.command("block") & filters.user(OWNER_ID))
async def ban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Pɪᴋᴀ Pɪᴋᴀ, Tʜɪs Cᴏᴍᴍᴀɴᴅ Fᴏʀ Bᴀɴ Usᴇʀ, Rᴇᴀᴅ /help Fᴏʀ Mᴏʀᴇ Iɴғᴏ!",
            quote=True
        )
        return
    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"`Pɪᴋᴀ Pɪᴋᴀ, Bᴀɴɴɪɴɢ Usᴇʀ...` \n\nUsᴇʀ ID : `{user_id}` \nDᴜʀᴀᴛɪᴏɴ : `{ban_duration}` \nRᴇᴀsᴏɴ : `{ban_reason}`"
        try:
            await c.send_message(
                user_id,
                f"Pɪᴋᴀ Pɪᴋᴀ, Sᴏʀʀʏ, Yᴏᴜ'ʀᴇ Bᴀɴɴᴇᴅ !!** \n\nRᴇᴀsᴏɴ : `{ban_reason}` \nDᴜʀᴀᴛɪᴏɴ : `{ban_duration}` ᴅᴀʏ's. \n\n**💬 Mᴇssᴀɢᴇ Fʀᴏᴍ Oᴡɴᴇʀ: Asᴋ Iɴ @{GROUP_SUPPORT} Iғ Yᴏᴜ Tʜɪɴᴋ Tʜɪs Wᴀs Aɴ Mɪsᴛᴀᴋᴇ."
            )
            ban_log_text += '\n\n✅ Pɪᴋᴀ Pɪᴋᴀ, Tʜɪs Nᴏᴛɪғɪᴄᴀᴛɪᴏɴ Wᴀs Sᴇɴᴛ Tᴏ Tʜᴀᴛ Usᴇʀ'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\n❌ Pɪᴋᴀ Pɪᴋᴀ, **Fᴀɪʟᴇᴅ Sᴇɴᴛ Tʜɪs Nᴏᴛɪғɪᴄᴀᴛɪᴏɴ Tᴏ Tʜᴀᴛ Usᴇʀ** \n\n`{traceback.format_exc()}`"
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"❌ Pɪᴋᴀ Pɪᴋᴀ, Aɴ Eʀʀᴏʀ Oᴄᴄᴏᴜʀᴇᴅ!, Tʀᴀᴄᴇʙᴀᴄᴋ Is Gɪᴠᴇɴ Bᴇʟᴏᴡ\n\n`{traceback.format_exc()}`",
            quote=True
        )


# Unban User
@Client.on_message(filters.private & filters.command("unblock") & filters.user(OWNER_ID))
async def unban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Pɪᴋᴀ Pɪᴋᴀ, Tʜɪs Cᴏᴍᴍᴀɴᴅ Fᴏʀ Uɴʙᴀɴ Usᴇʀ, Rᴇᴀᴅ /help Fᴏʀ Mᴏʀᴇ Iɴғᴏ!",
            quote=True
        )
        return
    try:
        user_id = int(m.command[1])
        unban_log_text = f"`Pɪᴋᴀ Pɪᴋᴀ, Uɴʙᴀɴɴɪɴɢ Usᴇʀ` \n**Usᴇʀ ID :**{user_id}"
        try:
            await c.send_message(
                user_id,
                f"🎊 Pɪᴋᴀ Pɪᴋᴀ, Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs, Yᴏᴜ Wᴀs Uɴʙᴀɴɴᴇᴅ!"
            )
            unban_log_text += '\n\n✅ Pɪᴋᴀ Pɪᴋᴀ, Tʜɪs Nᴏᴛɪғɪᴄᴀᴛɪᴏɴ Wᴀs Sᴇɴᴛ Tᴏ Tʜᴀᴛ Usᴇʀ'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\n❌ **Pɪᴋᴀ Pɪᴋᴀ, **Fᴀɪʟᴇᴅ Sᴇɴᴛ Tʜɪs Nᴏᴛɪғɪᴄᴀᴛɪᴏɴ Tᴏ Tʜᴀᴛ Usᴇʀ**\n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"❌ Pɪᴋᴀ Pɪᴋᴀ, Aɴ Eʀʀᴏʀ Oᴄᴄᴏᴜʀᴇᴅ!, Tʀᴀᴄᴇʙᴀᴄᴋ Is Gɪᴠᴇɴ Bᴇʟᴏᴡ\n\n`{traceback.format_exc()}`",
            quote=True
        )


# Banned User List
@Client.on_message(filters.private & filters.command("blocklist") & filters.user(OWNER_ID))
async def _banned_usrs(_, m: Message):
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"⫸ **Usᴇʀ ID **: `{user_id}`\n⫸ **Bᴀɴ Dᴜʀᴀᴛɪᴏɴ **: `{ban_duration}`\n⫸ **Bᴀɴɴᴇᴅ Dᴀᴛᴇ **: `{banned_on}`\n⫸ **Bᴀɴ Rᴇᴀsᴏɴ **: `{ban_reason}`\n\n"
    reply_text = f"⫸ **Tᴏᴛᴀʟ Bᴀɴɴᴇᴅ :** `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-user-list.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-user-list.txt', True)
        os.remove('banned-user-list.txt')
        return
    await m.reply_text(reply_text, True)
