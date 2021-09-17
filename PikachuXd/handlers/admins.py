# Copyright (C) 2021 PikachuXdBot

import traceback
import asyncio
from asyncio import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery, ChatPermissions

from PikachuXd.cache.admins import set
from PikachuXd.helpers.channelmusic import get_chat_id
from PikachuXd.helpers.decorators import authorized_users_only, errors
from PikachuXd.handlers.play import cb_admin_check
from PikachuXd.helpers.filters import command, other_filters
from PikachuXd.callsmusic import callsmusic
from PikachuXd.callsmusic.queues import queues
from PikachuXd.config import LOG_CHANNEL, OWNER_ID, BOT_USERNAME, COMMAND_PREFIXES
from PikachuXd.helpers.database import db, dcmdb, Database
from PikachuXd.helpers.dbtools import handle_user_status, delcmd_is_on, delcmd_on, delcmd_off
from PikachuXd.helpers.helper_functions.admin_check import admin_check
from PikachuXd.helpers.helper_functions.extract_user import extract_user
from PikachuXd.helpers.helper_functions.string_handling import extract_time


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

# Back Button
BACK_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 go back", callback_data="cbback")]])

@Client.on_message(filters.text & ~filters.private)
async def delcmd(_, message: Message):
    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!"):
        await message.delete()
    await message.continue_propagation()


@Client.on_message(filters.command("reload"))
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text("✅ Pɪᴋᴀ Pɪᴋᴀ, Bᴏᴛ **Rᴇʟᴏᴀᴅᴇᴅ Cᴏʀʀᴇᴄᴛʟʏ !**\n✅ **Aᴅᴍɪɴ Lɪsᴛ** Hᴀs Bᴇᴇɴ **Uᴘᴅᴀᴛᴇᴅ !**")


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}", "p"]))
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "**💡 Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Oᴘᴇɴᴇᴅ Mᴜsɪᴄ Pʟᴀʏᴇʀ Cᴏɴᴛʀᴏʟ Mᴇɴᴜ!**\n\n**💭 Yᴏᴜ Cᴀɴ Cᴏɴᴛʀᴏʟ Tʜᴇ Mᴜsɪᴄ Pʟᴀʏᴇʀ Jᴜsᴛ Bʏ Pʀᴇssɪɴɢ Oɴᴇ Oғ Tʜᴇ Bᴜᴛᴛᴏɴs Bᴇʟᴏᴡ**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ Pᴀᴜsᴇ", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "▶️ Rᴇsᴜᴍᴇ", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏩ Sᴋɪᴘ", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "⏹ Eɴᴅ", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⛔ Aɴᴛɪ Cᴍᴅ", callback_data="cbdelcmds"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🛄 Gʀᴏᴜᴘ Tᴏᴏʟs", callback_data="cbgtools"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Cʟᴏsᴇ", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Sᴛʀᴇᴀᴍɪɴɢ!")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pᴀᴜsᴇᴅ!")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Pᴀᴜsᴇᴅ!")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Rᴇsᴜᴍᴇᴅ!")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Sᴛʀᴇᴀᴍɪɴɢ!")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏹ Pɪᴋᴀ Pɪᴋᴀ, Sᴛʀᴇᴀᴍɪɴɢ Eɴᴅᴇᴅ!")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Sᴛʀᴇᴀᴍɪɴɢ!")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"⫸ Sᴋɪᴘᴘᴇᴅ : **{skip[0]}**.\n⫸ Nᴏᴡ Pʟᴀʏɪɴɢ : **{qeue[0][0]}**.")


@Client.on_message(command("auth") & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        await message.reply("❗Pɪᴋᴀ Pɪᴋᴀ, Rᴇᴘʟʏ Tᴏ Mᴇssᴀɢᴇ Tᴏ Aᴜᴛʜᴏʀɪᴢᴇ Usᴇʀ!")
        return
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply("🟢 Pɪᴋᴀ Pɪᴋᴀ, Usᴇʀ Aᴜᴛʜᴏʀɪᴢᴇᴅ.\n\nFʀᴏᴍ Nᴏᴡ Oɴ, Tʜᴀᴛ's Usᴇʀ Cᴀɴ Usᴇ Tʜᴇ Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs.")
    else:
        await message.reply("✅ Pɪᴋᴀ Pɪᴋᴀ, Usᴇʀ Aʟʀᴇᴀᴅʏ Aᴜᴛʜᴏʀɪᴢᴇᴅ!")


@Client.on_message(command("deauth") & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        await message.reply("❗Pɪᴋᴀ Pɪᴋᴀ, Rᴇᴘʟʏ Tᴏ Mᴇssᴀɢᴇ Tᴏ Dᴇᴀᴜᴛʜᴏʀɪᴢᴇ Usᴇʀ!")
        return
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply("🔴 Pɪᴋᴀ Pɪᴋᴀ, Usᴇʀ Dᴇᴀᴜᴛʜᴏʀɪᴢᴇᴅ.\n\nFʀᴏᴍ Nᴏᴡ Tʜᴀᴛ's Usᴇʀ Cᴀɴ'ᴛ Usᴇ Tʜᴇ Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs.")
    else:
        await message.reply("✅ Pɪᴋᴀ Pɪᴋᴀ, Usᴇʀ Aʟʀᴇᴀᴅʏ Dᴇᴀᴜᴛʜᴏʀɪᴢᴇᴅ!")


# this is a anti cmd feature
@Client.on_message(command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & ~filters.private)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Pɪᴋᴀ Pɪᴋᴀ, Rᴇᴀᴅ Tʜᴇ /help Mᴇssᴀɢᴇ Tᴏ Kɴᴏᴡ Hᴏᴡ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ.")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            await message.reply_text("✅ Pɪᴋᴀ Pɪᴋᴀ, Aʟʀᴇᴀᴅʏ Aᴄᴛɪᴠᴀᴛᴇᴅ!")
            return
        else:
            await delcmd_on(chat_id)
            await message.reply_text(
                "🟢 Pɪᴋᴀ Pɪᴋᴀ, Aᴄᴛɪᴠᴀᴛᴇᴅ Sᴜᴄᴇssғᴜʟʟʏ!"
            )
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("🔴 Pɪᴋᴀ Pɪᴋᴀ, Dɪsᴀʙʟᴇᴅ Sᴜᴄᴄᴇsғᴜʟʟʏ!")
    else:
        await message.reply_text(
            "Pɪᴋᴀ Pɪᴋᴀ, Rᴇᴀᴅ Tʜᴇ /help Mᴇssᴀɢᴇ Tᴏ Kɴᴏᴡ Hᴏᴡ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ."
        )


# music player callbacks (control by buttons feature)

@Client.on_callback_query(filters.regex("cbpause"))
@cb_admin_check
async def cbpause(_, query: CallbackQuery):
    chat_id = get_chat_id(query.message.chat)
    if (
        query.message.chat.id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[query.message.chat.id] == "paused"
            ):
        await query.edit_message_text("❗Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Pʟᴀʏɪɴɢ!", reply_markup=BACK_BUTTON)
    else:
        callsmusic.pytgcalls.pause_stream(query.message.chat.id)
        await query.edit_message_text("▶️ Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pᴀᴜsᴇᴅ!", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbresume"))
@cb_admin_check
async def cbresume(_, query: CallbackQuery):
    chat_id = get_chat_id(query.message.chat)
    if (
        query.message.chat.id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[query.message.chat.id] == "resumed"
            ):
        await query.edit_message_text("❗️ Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Pᴀᴜsᴇᴅ!", reply_markup=BACK_BUTTON)
    else:
        callsmusic.pytgcalls.resume_stream(query.message.chat.id)
        await query.edit_message_text("⏸ Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Rᴇsᴜᴍᴇᴅ!", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbend"))
@cb_admin_check
async def cbend(_, query: CallbackQuery):
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text("❗Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Pʟᴀʏɪɴɢ!", reply_markup=BACK_BUTTON)
    else:
        try:
            queues.clear(query.message.chat.id)
        except QueueEmpty:
            pass
        
        callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        await query.edit_message_text("✅ Pɪᴋᴀ Pɪᴋᴀ, Tʜᴇ Mᴜsɪᴄ Qᴜᴇᴜᴇ Hᴀs Bᴇᴇɴ Cʟᴇᴀʀᴇᴅ Aɴᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ Lᴇғᴛ Vᴏɪᴄᴇ Cʜᴀᴛ.", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbskip"))
@cb_admin_check
async def cbskip(_, query: CallbackQuery):
    global que
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text("❗Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Pʟᴀʏɪɴɢ!", reply_markup=BACK_BUTTON)
    else:
        queues.task_done(query.message.chat.id)
        
        if queues.is_empty(query.message.chat.id):
            callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                query.message.chat.id, queues.get(query.message.chat.id)["file"]
            )
            
    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await query.edit_message_text(f"⏭ Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Sᴋɪᴘᴘᴇᴅ Mᴜsɪᴄ!\n\n» Sᴋɪᴘᴘᴇᴅ : **{skip[0]}**.\n» Nᴏᴡ Pʟᴀʏɪɴɢ : **{qeue[0][0]}**.", reply_markup=BACK_BUTTON)

# (C) Sanki Music Project

# ban & unban function

@Client.on_message(filters.command("b", COMMAND_PREFIXES))
@authorized_users_only
async def ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.kick_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ Pɪᴋᴀ Pɪᴋᴀ, Sᴜᴄᴄᴇssғᴜʟʟʏ Bᴀɴɴᴇᴅ "
                f"{user_first_name}"
                " Fʀᴏᴍ Tʜɪs Gʀᴏᴜᴘ!"
            )
        else:
            await message.reply_text(
                "✅ Pɪᴋᴀ Pɪᴋᴀ, Bᴀɴɴᴇᴅ "
                f"<a href='tg://user?id={user_id}'>"
                f" {user_first_name}"
                "</a>"
                " Fʀᴏᴍ Tʜɪs Gʀᴏᴜᴘ!"
            )


@Client.on_message(filters.command("tb", COMMAND_PREFIXES))
@authorized_users_only
async def temp_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "Tʜᴇ Sᴘᴇᴄɪғɪᴇᴅ Tɪᴍᴇ Tʏᴘᴇ Is Iɴᴠᴀʟɪᴅ."
                "Usᴇ m, h, or d, Fᴏʀᴍᴀᴛ Tɪᴍᴇ : {}"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.kick_member(
            user_id=user_id,
            until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ Pɪᴋᴀ Pɪᴋᴀ, Tᴇᴍᴘᴏʀᴀʀɪʟʏ Bᴀɴɴᴇᴅ "
                f"{user_first_name}"
                f" ,Bᴀɴɴᴇᴅ Fᴏʀ {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "✅ Pɪᴋᴀ Pɪᴋᴀ, Tᴇᴍᴘᴏʀᴀʀɪʟʏ Bᴀɴɴᴇᴅ "
                f"<a href='tg://user?id={user_id}'>"
                " Fʀᴏᴍ Tʜɪs Gʀᴏᴜᴘ!"
                "</a>"
                f" ,Bᴀɴɴᴇᴅ Fᴏʀ {message.command[1]}!"
            )

@Client.on_message(filters.command(["ub", "um"], COMMAND_PREFIXES))
@authorized_users_only
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ Pɪᴋᴀ Pɪᴋᴀ, Oᴋ Aᴄᴄᴇᴘᴛᴇᴅ, Usᴇʀ "
                f"{user_first_name} Cᴀɴ"
                " Jᴏɪɴ Tᴏ Tʜɪs Gʀᴏᴜᴘ Aɢᴀɪɴ!"
            )
        else:
            await message.reply_text(
                "✅ Pɪᴋᴀ Pɪᴋᴀ, Oᴋ, Nᴏᴡ "
                f"<a href='tg://user?id={user_id}'>"
                f" {user_first_name}"
                "</a> Is Nᴏᴛ"
                " Rᴇsᴛʀɪᴄᴛᴇᴅ Aɢᴀɪɴ!"
            )

@Client.on_message(filters.command("m", COMMAND_PREFIXES))
async def mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            )
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ Pɪᴋᴀ Pɪᴋᴀ, Oᴋᴀʏ,🏻 "
                f"{user_first_name}"
                " Sᴜᴄᴄᴇssғᴜʟʟʏ Mᴜᴛᴇᴅ!"
            )
        else:
            await message.reply_text(
                "🏻✅ Pɪᴋᴀ Pɪᴋᴀ, Oᴋᴀʏ, "
                f"<a href='tg://user?id={user_id}'>"
                "Nᴏᴡ Is"
                "</a>"
                " Mᴜᴛᴇᴅ!"
            )


@Client.on_message(filters.command("tm", COMMAND_PREFIXES))
async def temp_mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "Tʜᴇ Sᴘᴇᴄɪғɪᴇᴅ Tɪᴍᴇ Tʏᴘᴇ Is Iɴᴠᴀʟɪᴅ. "
                "Usᴇ m, h, or d, Fᴏʀᴍᴀᴛ Tɪᴍᴇ : {}"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            ),
            until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Pɪᴋᴀ Pɪᴋᴀ, Mᴜᴛᴇᴅ Fᴏʀ A Wʜɪʟᴇ! "
                f"{user_first_name}"
                f" Mᴜᴛᴇᴅ Fᴏʀ {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "Pɪᴋᴀ Pɪᴋᴀ, Mᴜᴛᴇᴅ Fᴏʀ A Wʜɪʟᴇ! "
                f"<a href='tg://user?id={user_id}'>"
                "Is"
                "</a>"
                " Nᴏᴡ "
                f" Mᴜᴛᴇᴅ, Fᴏʀ {message.command[1]}!"
            )
