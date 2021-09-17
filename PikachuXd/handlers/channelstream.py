# Copyright (C) 2021 VeezMusic Project

import json
import os
from os import path
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import Voice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch
from handlers.play import generate_cover
from handlers.play import cb_admin_check
from handlers.play import transcode
from handlers.play import convert_seconds
from handlers.play import time_to_seconds
from handlers.play import changeImageSize
from config import BOT_NAME as bn
from config import DURATION_LIMIT
from config import UPDATES_CHANNEL as updateschannel
from config import que
from cache.admins import admins as a
from helpers.errors import DurationLimitError
from helpers.decorators import errors
from helpers.admins import get_administrators
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only
from helpers.filters import command, other_filters
from helpers.gets import get_file_name
from callsmusic import callsmusic
from callsmusic.callsmusic import client as USER
from converter.converter import convert
from downloaders import youtube
from callsmusic.queues import queues

chat_id = None



@Client.on_message(filters.command(["channelplaylist","cplaylist"]) & filters.group & ~filters.edited)
async def playlist(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
    except:
      message.reply("Pɪᴋᴀ Pɪᴋᴀ, Is Tʜɪs Cʜᴀᴛ Eᴠᴇɴ Lɪɴᴋᴇᴅ ?")
      return
    global que
    queue = que.get(lol)
    if not queue:
        await message.reply_text("Pɪᴋᴀ Pɪᴋᴀ, Pʟᴀʏᴇʀ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Tʜᴇ Vᴏɪᴄᴇ Cʜᴀᴛ!")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "**Nᴏᴡ Pʟᴀʏɪɴɢ** Iɴ {}".format(lel.linked_chat.title)
    msg += "\n- " + now_playing
    msg += "\n- Rᴇǫᴜᴇsᴛᴇᴅ Fʀᴏᴍ : " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Qᴜᴇᴜᴇ**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n- {name}"
            msg += f"\n- Rᴇǫᴜᴇsᴛᴇᴅ Fʀᴏᴍ : {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        # if chat.id in active_chats:
        stats = "Pɪᴋᴀ Pɪᴋᴀ, Sᴇᴛᴛɪɴɢs Oғ **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "Vᴏʟᴜᴍᴇ : {}%\n".format(vol)
            stats += "Sᴏɴɢs Iɴ Qᴜᴇᴜᴇ : `{}`\n".format(len(que))
            stats += "Now Pʟᴀʏɪɴɢ : **{}**\n".format(queue[0][0])
            stats += "Rᴇǫᴜᴇsᴛᴇᴅ Fʀᴏᴍ : {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "cleave"),
                InlineKeyboardButton("⏸", "cpuse"),
                InlineKeyboardButton("▶️", "cresume"),
                InlineKeyboardButton("⏭", "cskip"),
            ],
            [
                InlineKeyboardButton("Pʟᴀʏʟɪsᴛ 📖", "cplaylist"),
            ],
            [InlineKeyboardButton("❌ Cʟᴏsᴇ", "ccls")],
        ]
    )
    return mar


@Client.on_message(filters.command(["channelcurrent","ccurrent"]) & filters.group & ~filters.edited)
async def ee(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("Pɪᴋᴀ Pɪᴋᴀ, Is Tʜɪs Cʜᴀᴛ Eᴠᴇɴ Lɪɴᴋᴇᴅ ?")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("Pɪᴋᴀ Pɪᴋᴀ, Pʟᴇᴀsᴇ Tᴜʀɴ Oɴ Tʜᴇ Vᴏɪᴄᴇ Cʜᴀᴛ Fɪʀsᴛ!")


@Client.on_message(filters.command(["channelplayer","cplayer"]) & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    playing = None
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("Pɪᴋᴀ Pɪᴋᴀ, Is Tʜɪs Cʜᴀᴛ Eᴠᴇɴ Lɪɴᴋᴇᴅ ?")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("Pɪᴋᴀ Pɪᴋᴀ, Pʟᴇᴀsᴇ Tᴜʀɴ Oɴ Tʜᴇ Vᴏɪᴄᴇ Cʜᴀᴛ Fɪʀsᴛ!")


@Client.on_callback_query(filters.regex(pattern=r"^(cplaylist)$"))
async def p_cb(b, cb):
    global que
    try:
      lel = await client.get_chat(cb.message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      return    
    que.get(lol)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(lol)
        if not queue:
            await cb.message.edit("Pɪᴋᴀ Pɪᴋᴀ, Pʟᴀʏᴇʀ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Tʜᴇ Vᴏɪᴄᴇ Cʜᴀᴛ!")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Nᴏᴡ Pʟᴀʏɪɴɢ** Iɴ {}".format(conv.title)
        msg += "\n- " + now_playing
        msg += "\n- Rᴇǫᴜᴇsᴛᴇᴅ Fʀᴏᴍ : " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Qᴜᴇᴜᴇ**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Rᴇǫᴜᴇsᴛᴇᴅ Fʀᴏᴍ {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(cplay|cpause|cskip|cleave|cpuse|cresume|cmenu|ccls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
      try:
        lel = await b.get_chat(cb.message.chat.id)
        lol = lel.linked_chat.id
        conv = lel.linked_chat
        chet_id = lol
      except:
        return
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat
    

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "cpause":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Cʜᴀᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pᴀᴜsᴇᴅ!")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "cplay":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Cʜᴀᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Rᴇsᴜᴍᴇᴅ!")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "cplaylist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("Pɪᴋᴀ Pɪᴋᴀ, Pʟᴀʏᴇʀ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Tʜᴇ Vᴏɪᴄᴇ Cʜᴀᴛ!")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Nᴏᴡ Pʟᴀʏɪɴɢ** Iɴ {}".format(cb.message.chat.title)
        msg += "\n- " + now_playing
        msg += "\n- Rᴇǫᴜᴇsᴛᴇᴅ Fʀᴏᴍ : " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Qᴜᴇᴜᴇ**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Rᴇǫᴜᴇsᴛᴇᴅ Fʀᴏᴍ {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "cresume":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Cʜᴀᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Oʀ Aʟʀᴇᴀᴅʏ Pʟᴀʏɪɴɢ!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Rᴇsᴜᴍᴇᴅ!")
    elif type_ == "cpuse":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Cʜᴀᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Oʀ Aʟʀᴇᴀᴅʏ Pᴀᴜsᴇᴅ!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pᴀᴜsᴇᴅ!")
    elif type_ == "ccls":
        await cb.answer("Cʟᴏsᴇᴅ Mᴇɴᴜ")
        await cb.message.delete()

    elif type_ == "cmenu":
        stats = updated_stats(conv, qeue)
        await cb.answer("Mᴇɴᴜ Oᴘᴇɴᴇᴅ")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "cleave"),
                    InlineKeyboardButton("⏸", "cpuse"),
                    InlineKeyboardButton("▶️", "cresume"),
                    InlineKeyboardButton("⏭", "cskip"),
                ],
                [
                    InlineKeyboardButton("Pʟᴀʏʟɪsᴛ 📖", "cplaylist"),
                ],
                [InlineKeyboardButton("❌ Cʟᴏsᴇ", "ccls")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)
    elif type_ == "cskip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Cʜᴀᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ!", show_alert=True)
        else:
            queues.task_done(chet_id)

            if queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("- Pɪᴋᴀ Pɪᴋᴀ, Nᴏ Mᴏʀᴇ Pʟᴀʏʟɪsᴛ...\n- Lᴇᴀᴠɪɴɢ Vᴄ !!")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, queues.get(chet_id)["file"]
                )
                await cb.answer("Skipped")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"- Aᴍ Sᴋɪᴘᴘᴇᴅ Tʀᴀᴄᴋ\n- Nᴏᴡ Pʟᴀʏɪɴɢ : **{qeue[0][0]}**."
                )

    else:
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("Pɪᴋᴀ Pɪᴋᴀ, Mᴜsɪᴄ Pʟᴀʏᴇʀ Wᴀs Dɪsᴄᴏɴɴᴇᴄᴛᴇᴅ Fʀᴏᴍ Vᴏɪᴄᴇ Cʜᴀᴛ!"")
        else:
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Cʜᴀᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ!", show_alert=True)


@Client.on_message(filters.command(["channelplay","cplay"])  & filters.group & ~filters.edited)
@authorized_users_only
async def play(_, message: Message):
    global que
    lel = await message.reply("🔄 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ..**")

    try:
      conchat = await _.get_chat(message.chat.id)
      conv = conchat.linked_chat
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Pɪᴋᴀ Pɪᴋᴀ, Is Tʜɪs Cʜᴀᴛ Eᴠᴇɴ Lɪɴᴋᴇᴅ ?")
      return
    try:
      administrators = await get_administrators(conv)
    except:
      await message.reply("Pɪᴋᴀ Pɪᴋᴀ, I'ᴍ Nᴏᴛ Aᴅᴍɪɴ Iɴ Tʜɪs Cʜᴀɴɴᴇʟ, Sᴏʀʀʏ!")
    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>Pɪᴋᴀ Pɪᴋᴀ, Rᴇᴍᴇᴍʙᴇʀ Tᴏ Aᴅᴅ Hᴇʟᴘᴇʀ Tᴏ Yᴏᴜʀ Cʜᴀɴɴᴇʟ.</b>",
                    )
                    pass

                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>Pɪᴋᴀ Pɪᴋᴀ, Aᴅᴅ Mᴇ As Aᴅᴍɪɴ Oғ Yᴏᴜʀ Gʀᴏᴜᴘ Fɪʀsᴛ.</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        "<b>Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟᴘᴇʀ Usᴇʀʙᴏᴛ Jᴏɪɴᴇᴅ Yᴏᴜʀ Cʜᴀᴛ.</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 Pɪᴋᴀ Pɪᴋᴀ, 🔴 Fʟᴏᴏᴅ Wᴀɪᴛ Eʀʀᴏʀ 🔴 \nUsᴇʀ @PikachuXdAssistant Cᴏᴜʟᴅɴ'ᴛ Jᴏɪɴ Yᴏᴜʀ Gʀᴏᴜᴘ Dᴜᴇ Tᴏ Hᴇᴀᴠʏ Rᴇǫᴜᴇsᴛᴇᴅ Fᴏʀ Usᴇʀʙᴏᴛ! Mᴀᴋᴇ Sᴜʀᴇ Usᴇʀ Is Nᴏᴛ Bᴀɴɴᴇᴅ Iɴ Gʀᴏᴜᴘ."
                        "\n\nOʀ Mᴀɴᴜᴀʟʟʏ Aᴅᴅ @PikachuXdAssistant Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Tʀʏ Aɢᴀɪɴ.</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> Pɪᴋᴀ Pɪᴋᴀ, @PikachuXdAssistant Usᴇʀʙᴏᴛ Nᴏᴛ Iɴ Tʜɪs Cʜᴀᴛ, Asᴋ Aᴅᴍɪɴ Tᴏ Sᴇɴᴅ /play Cᴏᴍᴍᴀɴᴅ Fᴏʀ Fɪʀsᴛ Tɪᴍᴇ Oʀ Aᴅᴅ @PikachuXdAssistant Mᴀɴᴜᴀʟʟʏ.</i>"
        )
        return
    message.from_user.id
    text_links = None
    message.from_user.first_name
    await lel.edit("🔎 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Fɪɴᴅɪɴɢ...**")
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    if message.reply_to_message:
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == 'url']
        text_links = [
            entity for entity in entities if entity.type == 'text_link'
        ]
    else:
        urls=None
    if text_links:
        urls = True    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Pɪᴋᴀ Pɪᴋᴀ, Vɪᴅᴇᴏs Lᴏɴɢᴇʀ Tʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs Aʀᴇɴ'ᴛ Aʟʟᴏᴡᴇᴅ Tᴏ Pʟᴀʏ!"
            )
        keyboard = InlineKeyboardMarkup(
            [
            [
                [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
                ],
                [InlineKeyboardButton(text="🎧 Cʜᴀɴɴᴇʟ", url=f"https://t.me/{updateschannel}")],
                 [InlineKeyboardButton(text="❌ Cʟᴏsᴇ", callback_data="cls")],
            ]
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/f6086f8909fbfeb0844f2.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🎵 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ...**")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "❗Pɪᴋᴀ Pɪᴋᴀ, Sᴏɴɢ Nᴏᴛ Fᴏᴜɴᴅ, Pʟᴇᴀsᴇ Gɪᴠᴇ A Vᴀʟɪᴅ Sᴏɴɢ Nᴀᴍᴇ..."
            )
            print(str(e))
            return
        dlurl = url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
          [
              [
                  InlineKeyboardButton("⏺ Mᴇɴᴜ", callback_data="cmenu"),
                  InlineKeyboardButton("🗑 Cʟᴏsᴇ", callback_data="ccls")
              ],
          ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))        
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("🎵 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ...**")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "❗ Pɪᴋᴀ Pɪᴋᴀ, Sᴏɴɢ Nᴏᴛ Fᴏᴜɴᴅ, Pʟᴇᴀsᴇ Gɪᴠᴇ A Vᴀʟɪᴅ Sᴏɴɢ Nᴀᴍᴇ..."
            )
            print(str(e))
            return

        dlurl = url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
                ],
                [
                  InlineKeyboardButton(text="🎬 Yᴏᴜᴛᴜʙᴇ", url=f"{url}"),
                  InlineKeyboardButton(text="Dᴏᴡɴʟᴏᴀᴅ 📥", url=f"{dlurl}"),
                ],
                 [InlineKeyboardButton(text="❌ Cʟᴏsᴇ", callback_data="cls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))
    chat_id = chid
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"🏷 **Nᴀᴍᴇ :** [{title[:25]}]({url})\n📥 **Dᴏᴡɴʟᴏᴀᴅ :** [ℂ𝕃𝕀ℂ𝕂 ℍ𝔼ℝ𝔼]{durl}\n💡 **Qᴜᴇᴜᴇᴅ Aᴛ Pᴏsɪᴛɪᴏɴ :** `{position}`\n" \
                    + f"🎧 **Rᴇǫᴜᴇsᴛ Bʏ :** {message.from_user.mention}",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = chid
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"🏷 **Nᴀᴍᴇ :** [{title[:45]}]({url})\n📥 **Dᴏᴡɴʟᴏᴀᴅ :** [ℂ𝕃𝕀ℂ𝕂 ℍ𝔼ℝ𝔼]{durl}\n💡 **Sᴛᴀᴛᴜs :** `Playing`\n" \
                   +f"🎧 **Rᴇǫᴜᴇsᴛ Bʏ :** {message.from_user.mention}")
        os.remove("final.png")
        return await lel.delete()
