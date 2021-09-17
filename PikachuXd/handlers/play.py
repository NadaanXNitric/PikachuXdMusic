import os
import json
import ffmpeg
import aiohttp
import aiofiles
import asyncio
import requests
import PikachuXd.converter
from os import path
from asyncio.queues import QueueEmpty
from pyrogram import Client, filters
from typing import Callable
from PikachuXd.helpers.channelmusic import get_chat_id
from PikachuXd.callsmusic import callsmusic
from PikachuXd.callsmusic.queues import queues
from PikachuXd.helpers.admins import get_administrators
from youtube_search import YoutubeSearch
from PikachuXd.callsmusic.callsmusic import client as USER
from pyrogram.errors import UserAlreadyParticipant
from PikachuXd.downloaders import youtube

from PikachuXd.config import que, THUMB_IMG, DURATION_LIMIT, BOT_USERNAME, BOT_NAME, UPDATES_CHANNEL, GROUP_SUPPORT, ASSISTANT_NAME
from PikachuXd.helpers.filters import command, other_filters
from PikachuXd.helpers.decorators import authorized_users_only
from PikachuXd.helpers.gets import get_file_name, get_url
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, Voice
from PikachuXd.converter.converter import convert
from PikachuXd.cache.admins import admins as a
from PIL import Image, ImageFont, ImageDraw


aiohttpsession = aiohttp.ClientSession()
chat_id = None
useer ="NaN"
DISABLED_GROUPS = []

KRONA = ImageFont.truetype("etc/KronaOne-Regular.ttf", 48)
KRONA_52 = ImageFont.truetype("etc/KronaOne-Regular.ttf", 52)
ITC_REG = ImageFont.truetype(
    "etc/ITC Avant Garde Gothic LT Book Regular.otf", 48)
KRONA_SMALL = ImageFont.truetype("etc/KronaOne-Regular.ttf", 32)

def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer("Yᴏᴜ Nᴏᴛ Aʟʟᴏᴡᴇᴅ Tᴏ Dᴏ Tʜɪs!", show_alert=True)
            return
    return decorator                                                                       
                                          
                                                                                    
def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw",
        format="s16le",
        acodec="pcm_s16le",
        ac=2,
        ar="48k"
    ).overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(title, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 60)
    draw.text((10, 580), f"Now Playing", fill="white", font=ITC_REG)
    draw.text((10, 640), f"{title}", fill="white", font=KRONA_52)
    draw.text((985, 20), f"A Sanki BOTs", fill="white", font=KRONA_SMALL)
    draw.text((1100, 50), f"Product", fill="white", font=KRONA_SMALL)
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(command(["playlist", f"playlist@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def playlist(client, message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text("**Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Iɴ Sᴛʀᴇᴀᴍɪɴɢ!**")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "**Nᴏᴡ Pʟᴀʏɪɴɢ** Oɴ {}".format(message.chat.title)
    msg += "\n• "+ now_playing
    msg += "\n• Rᴇǫᴜᴇsᴛᴇᴅ Bʏ "+by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Qᴜᴇᴜᴇᴅ Sᴏɴɢ**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n• {name}"
            msg += f"\n• Rᴇǫᴜᴇsᴛᴇᴅ Bʏ : {usr}\n"
    await message.reply_text(msg)
                            
# ============================= Settings =========================================
def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        stats = "Sᴇᴛᴛɪɴɢs Oғ **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "Vᴏʟᴜᴍᴇ : {}%\n".format(vol)
            stats += "Sᴏɴɢs Iɴ Qᴜᴇᴜᴇ : `{}`\n".format(len(que))
            stats += "Now Pʟᴀʏɪɴɢ : **{}**\n".format(queue[0][0])
            stats += "Rᴇǫᴜᴇsᴛᴇᴅ Bʏ : {}".format(queue[0][1].mention)
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
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip")
            ],
            [
                InlineKeyboardButton("📖 Pʟᴀʏʟɪsᴛ", "playlist"),
            ],
            [       
                InlineKeyboardButton("🗑 Cʟᴏsᴇ", "cls")
            ]        
        ]
    )
    return mar


@Client.on_message(command(["player", f"player@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    playing = None
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))
            
        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("**Pɪᴋᴀ Pɪᴋᴀ, Pʟᴇᴀsᴇ Tᴜʀɴ Oɴ Tʜᴇ Vᴏɪᴄᴇ Cʜᴀᴛ Fɪʀsᴛ.**")


@Client.on_message(
    command(["musicplayer", f"musicplayer@{BOT_USERNAME}"]) & ~filters.edited & ~filters.bot & ~filters.private
)
@authorized_users_only
async def hfmm(_, message):
    global DISABLED_GROUPS
    try:
        user_id = message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text(
            "**Pɪᴋᴀ Pɪᴋᴀ, I'ᴍ Oɴʟʏ Kɴᴏᴡ** `/musicplayer on` **Aɴᴅ** `/musicplayer off`"
        )
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await message.reply("`Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ...`")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("**Pɪᴋᴀ Pɪᴋᴀ, Mᴜsɪᴄ Pʟᴀʏᴇʀ Aʟʀᴇᴀᴅʏ Aᴄᴛɪᴠᴀᴛᴇᴅ.**")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"✅ **Pɪᴋᴀ Pɪᴋᴀ, Mᴜsɪᴄ Pʟᴀʏᴇʀ Hᴀs Bᴇᴇɴ Aᴄᴛɪᴠᴀᴛᴇᴅ Iɴ Tʜɪs Cʜᴀᴛ.**\n\n💬 {message.chat.id}"
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await message.reply("`Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ...`")
        
        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("**Pɪᴋᴀ Pɪᴋᴀ, Mᴜsɪᴄ Pʟᴀʏᴇʀ Aʟʀᴇᴀᴅʏ Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ.**")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"✅ **Pɪᴋᴀ Pɪᴋᴀ, Pʟᴀʏᴇʀ Hᴀs Bᴇᴇɴ Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ Iɴ Tʜɪs Cʜᴀᴛ.**\n\n💬 {message.chat.id}"
        )
    else:
        await message.reply_text(
            "**Pɪᴋᴀ Pɪᴋᴀ, I'ᴍ Oɴʟʏ Kɴᴏᴡ** `/musicplayer on` **Aɴᴅ** `/musicplayer off`"
        )


@Client.on_callback_query(filters.regex(pattern=r"^(playlist)$"))
async def p_cb(b, cb):
    global que    
    que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("**Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Is Pʟᴀʏɪɴɢ❗**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Nᴏᴡ Pʟᴀʏɪɴɢ** Oɴ {}".format(cb.message.chat.title)
        msg += "\n• " + now_playing
        msg += "\n• Rᴇǫᴜᴇsᴛ Bʏ " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Qᴜᴇᴜᴇᴅ Sᴏɴɢ**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n• {name}"
                msg += f"\n• Rᴇǫᴜᴇsᴛ Bʏ {usr}\n"
        await cb.message.edit(msg)      


@Client.on_callback_query(
    filters.regex(pattern=r"^(play|pause|skip|leave|puse|resume|menu|cls)$")
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
        chet_id = cb.message.chat.id
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "pause":
        if (
            chet_id not in callsmusic.pytgcalls.active_calls
                ) or (
                    callsmusic.pytgcalls.active_calls[chet_id] == "paused"
                ):
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Assɪsᴛᴀɴᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Vᴏɪᴄᴇ Cʜᴀᴛ!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)
            
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pᴀᴜsᴇᴅ!")
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply("play"))
                
    elif type_ == "play":       
        if (
            chet_id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[chet_id] == "playing"
            ):
                await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Assɪsᴛᴀɴᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Vᴏɪᴄᴇ Cʜᴀᴛ!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Rᴇsᴜᴍᴇᴅ!")
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply("pause"))

    elif type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:   
            await cb.message.edit("Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Nᴏᴛʜɪɴɢ Is Sᴛʀᴇᴀᴍɪɴɢ!")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Nᴏᴡ Pʟᴀʏɪɴɢ** Oɴ {}".format(cb.message.chat.title)
        msg += "\n• "+ now_playing
        msg += "\n• Rᴇǫᴜᴇsᴛ Bʏ "+by
        temp.pop(0)
        if temp:
             msg += "\n\n"
             msg += "**Qᴜᴇᴜᴇᴅ Sᴏɴɢ**"
             for song in temp:
                 name = song[0]
                 usr = song[1].mention(style="md")
                 msg += f"\n• {name}"
                 msg += f"\n• Rᴇǫᴜᴇsᴛ Bʏ {usr}\n"
        await cb.message.edit(msg)      
                      
    elif type_ == "resume":     
        if (
            chet_id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[chet_id] == "playing"
            ):
                await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Vᴏɪᴄᴇ Cʜᴀᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Oʀ Aʟʀᴇᴀᴅʏ Pʟᴀʏɪɴɢ!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Rᴇsᴜᴍᴇᴅ!")
     
    elif type_ == "puse":         
        if (
            chet_id not in callsmusic.pytgcalls.active_calls
                ) or (
                    callsmusic.pytgcalls.active_calls[chet_id] == "paused"
                ):
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Vᴏɪᴄᴇ, Cʜᴀᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Oʀ Aʟʀᴇᴀᴅʏ Pᴀᴜsᴇᴅ!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)
            
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pᴀᴜsᴇᴅ!")

    elif type_ == "cls":          
        await cb.answer("Cʟᴏsᴇᴅ Mᴇɴᴜ")
        await cb.message.delete()       

    elif type_ == "menu":  
        stats = updated_stats(cb.message.chat, qeue)  
        await cb.answer("Mᴇɴᴜ Oᴘᴇɴᴇᴅ")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip")
                
                ],
                [
                    InlineKeyboardButton("📖 Pʟᴀʏʟɪsᴛ", "playlist"),
                
                ],
                [       
                    InlineKeyboardButton("🗑 Cʟᴏsᴇ", "cls")
                ]        
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)

    elif type_ == "skip":        
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Assɪsᴛᴀɴᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Vᴏɪᴄᴇ Cʜᴀᴛ!", show_alert=True)
        else:
            callsmusic.queues.task_done(chet_id)

            if callsmusic.queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("• Pɪᴋᴀ Pɪᴋᴀ, Nᴏ Mᴏʀᴇ Pʟᴀʏʟɪsᴛ...\n• Lᴇᴀᴠɪɴɢ Vᴏɪᴄᴇ Cʜᴀᴛ!")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, callsmusic.queues.get(chet_id)["file"]
                )
                await cb.answer("skipped")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"⫸ Aᴍ Sᴋɪᴘᴘᴇᴅ ᴛʀᴀᴄᴋ\n⫸ Nᴏᴡ Pʟᴀʏɪɴɢ : **{qeue[0][0]}**"
                )

    elif type_ == "leave":
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("⏹ **music stopped!**")
        else:
            await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Assɪsᴛᴀɴᴛ Is Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Vᴏɪᴄᴇ Cʜᴀᴛ!", show_alert=True)


@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(_, message: Message):
    global que
    global useer
    if message.chat.id in DISABLED_GROUPS:
        return    
    lel = await message.reply("🔄 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ...**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name = "PikachuXdAssistant"
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
                        f"<b>Pɪᴋᴀ Pɪᴋᴀ, Pʟᴇᴀsᴇ Aᴅᴅ @PikachuXdAssistant Tᴏ Yᴏᴜʀ Cʜᴀɴɴᴇʟ.</b>",
                    )
                    pass
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>Pɪᴋᴀ Pɪᴋᴀ, Mᴀᴋᴇ Mᴇ As Aᴅᴍɪɴ Fɪʀsᴛ.</b>",
                    )
                    return
                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "🤖: Pɪᴋᴀ Pɪᴋᴀ, I'ᴍ Jᴏɪɴᴇᴅ Tᴏ Tʜɪs Gʀᴏᴜᴘ Fᴏʀ Pʟᴀʏɪɴɢ Mᴜsɪᴄ Oɴ Vᴏɪᴄᴇ Cʜᴀᴛ."
                    )
                    await lel.edit(
                        "<b>Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟᴘᴇʀ Usᴇʀʙᴏᴛ Jᴏɪɴᴇᴅ Yᴏᴜʀ Cʜᴀᴛ.</b>",
                    )
                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>Pɪᴋᴀ Pɪᴋᴀ, ⛑ Fʟᴏᴏᴅ Wᴀɪᴛ Eʀʀᴏʀ ⛑\n@PikachuXdAssistant Cᴏᴜʟᴅɴ'ᴛ Jᴏɪɴ Yᴏᴜʀ Gʀᴏᴜᴘ Dᴜᴇ Tᴏ Mᴀɴʏ Jᴏɪɴ Rᴇǫᴜᴇsᴛs Fᴏʀ Usᴇʀʙᴏᴛ! Mᴀᴋᴇ Sᴜʀᴇ Tʜᴇ Usᴇʀ Is Nᴏᴛ Bᴀɴɴᴇᴅ Iɴ Tʜᴇ Gʀᴏᴜᴘ."
                        f"\n\nOʀ Aᴅᴅ @PikachuXdAssistant Mᴀɴᴜᴀʟʟʏ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Tʀʏ Aɢᴀɪɴ.</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i>Pɪᴋᴀ Pɪᴋᴀ, @PikachuXdAssistant Wᴀs Bᴀɴɴᴇᴅ Iɴ Tʜɪs Gʀᴏᴜᴘ, Asᴋ Aᴅᴍɪɴ Tᴏ Uɴʙᴀɴ @PikachuXdAssistant Mᴀɴᴜᴀʟʟʏ.</i>"
        )
        return
    text_links=None
    await lel.edit("🔎 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Fɪɴᴅɪɴɢ...**")
    if message.reply_to_message:
        if message.reply_to_message.audio or message.reply_to_message.voice:
            pass
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
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ **Pɪᴋᴀ Pɪᴋᴀ, Vɪᴅᴇᴏs Lᴏɴɢᴇʀ Tʜᴀɴ `{DURATION_LIMIT}` ᴍɪɴᴜᴛᴇs Aʀᴇɴ'ᴛ Aʟʟᴏᴡᴇᴅ Tᴏ Pʟᴀʏ!**"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🖱 Mᴇɴᴜ", callback_data="menu"),
                    InlineKeyboardButton("🗑 Cʟᴏsᴇ", callback_data="cls"),
                ],[
                    InlineKeyboardButton("📣 Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/10a6ff6687de32dac14a3.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"
        requested_by = message.from_user.first_name
        await generate_cover(title, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🎵 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:25]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb-{title}-veezmusic.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]
        except Exception as e:
            await lel.edit(
                "😕 **Pɪᴋᴀ Pɪᴋᴀ, Sᴏʀʀʏ, Wᴇ Cᴏᴜʟᴅɴ'ᴛ Fɪɴᴅ Yᴏᴜʀ Rᴇǫᴜᴇsᴛᴇᴅ Sᴏɴɢ**\n• Cʜᴇᴄᴋ Tʜᴀᴛ Tʜᴇ Nᴀᴍᴇ Is Cᴏʀʀᴇᴄᴛ Oʀ Tʀʏ Bʏ Sᴇᴀʀᴄʜɪɴɢ Iɴ Iɴʟɪɴᴇ Mᴏᴅᴇ."
            )
            print(str(e))
            return
        dlurl=url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
                ],
                 [InlineKeyboardButton(text="❌ Cʟᴏsᴇ", callback_data="cls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(title, thumbnail)
        file_path = await converter.convert(youtube.download(url))        
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("🎵 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        
        try:
          results = YoutubeSearch(query, max_results=5).to_dict()
        except:
          await lel.edit("**Pɪᴋᴀ Pɪᴋᴀ, Pʟᴇᴀsᴇ Gɪᴠᴇ A Sᴏɴɢ Nᴀᴍᴇ Yᴏᴜ Wᴀɴᴛ Tᴏ Pʟᴀʏ!**")
        # veez project
        try:
            toxxt = "**Pɪᴋᴀ Pɪᴋᴀ, Cʜᴏᴏsᴇ A Sᴏɴɢ Tᴏ Pʟᴀʏ 🐬😼**\n\n"
            j = 0
            useer=user_name
            emojilist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣",]

            while j < 5:
                toxxt += f"{emojilist[j]} **Title - [{results[j]['title']}](https://youtube.com{results[j]['url_suffix']})**\n"
                toxxt += f" ├🍓• Dᴜʀᴀᴛɪᴏɴ - {results[j]['duration']}\n"
                toxxt += f" └🍓• Pᴏᴡᴇʀᴇᴅ ʙʏ - 「Pɪᴋᴀᴄʜᴜ • Mᴜsɪᴄ」ǫ\n"

                j += 1            
            koyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("1️⃣", callback_data=f'plll 0|{query}|{user_id}'),
                        InlineKeyboardButton("2️⃣", callback_data=f'plll 1|{query}|{user_id}'),
                        InlineKeyboardButton("3️⃣", callback_data=f'plll 2|{query}|{user_id}'),
                    ],
                    [
                        InlineKeyboardButton("4️⃣", callback_data=f'plll 3|{query}|{user_id}'),
                        InlineKeyboardButton("5️⃣", callback_data=f'plll 4|{query}|{user_id}'),
                    ],
                    [InlineKeyboardButton(text="Cʟᴏsᴇ 🛑", callback_data="cls")],
                ]
            )       
            await lel.edit(toxxt,reply_markup=koyboard,disable_web_page_preview=True)
            # WHY PEOPLE ALWAYS LOVE PORN ?? (A point to think)
            return
        except:
            await lel.edit("__Pɪᴋᴀ Pɪᴋᴀ, Nᴏ Eɴᴏᴜɢʜ Rᴇsᴜʟᴛs Tᴏ Cʜᴏᴏsᴇ.. Aᴍ Sᴛᴀʀᴛɪɴɢ Dɪʀᴇᴄᴛ Pʟᴀʏ...__")
                        
            # print(results)
            try:
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:25]
                thumbnail = results[0]["thumbnails"][0]
                thumb_name = f"thumb-{title}-veezmusic.jpg"
                thumb = requests.get(thumbnail, allow_redirects=True)
                open(thumb_name, "wb").write(thumb.content)
                duration = results[0]["duration"]
                results[0]["url_suffix"]
                views = results[0]["views"]
            except Exception as e:
                await lel.edit(
                    "**❌ Pɪᴋᴀ Pɪᴋᴀ, Sᴏɴɢ Nᴏᴛ Fᴏᴜɴᴅ.** Pʟᴇᴀsᴇ Gɪᴠᴇ A Vᴀʟɪᴅ Sᴏɴɢ Nᴀᴍᴇ."
                )
                print(str(e))
                return
            dlurl=url
            dlurl=dlurl.replace("youtube","youtubepp")
            keyboard = InlineKeyboardMarkup(
            [
                [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
                ],
                 [InlineKeyboardButton(text="❌ Cʟᴏsᴇ", callback_data="cls")],
            ]
       )
            requested_by = message.from_user.first_name
            await generate_cover(title, thumbnail)
            file_path = await converter.convert(youtube.download(url))   
    chat_id = get_chat_id(message.chat)
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
            caption=f"🏷 **Nᴀᴍᴇ :** [{title[:25]}]({url})\n📥 **Dᴏᴡɴʟᴏᴀᴅ :** [ℂ𝕃𝕀ℂ𝕂 ℍ𝔼ℝ𝔼]({dlurl})\n💡 **Qᴜᴇᴜᴇᴅ Aᴛ Poᴏsɪᴛɪᴏɴ :** `{position}`\n" \
                    + f"🎧 **Rᴇǫᴜᴇsᴛ Bʏ :** {message.from_user.mention}",
            reply_markup=keyboard
        )
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("**Pɪᴋᴀ Pɪᴋᴀ, Vᴏɪᴄᴇ Cʜᴀᴛ Gʀᴏᴜᴘ Nᴏᴛ Aᴄᴛɪᴠᴇ, Cᴀɴ'ᴛ Pʟᴀʏ A Sᴏɴɢ.**")
            return
        await message.reply_photo(
            photo="final.png",
            caption=f"🏷 **Nᴀᴍᴇ :** [{title[:45]}]({url})\n📥 **Dᴏᴡɴʟᴏᴀᴅ :** [ℂ𝕃𝕀ℂ𝕂 ℍ𝔼ℝ𝔼]({dlurl})\n💡 **Sᴛᴀᴛᴜs :** `Pʟᴀʏɪɴɢ`\n" \
                   +f"🎧 **Rᴇǫᴜᴇsᴛ Bʏ :** {message.from_user.mention}",
            reply_markup=keyboard
        )
        os.remove("final.png")
        return

@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def lol_cb(b, cb):
    global que
    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_=cbd.split(None, 1)[1]
    try:
        x,query,useer_id = typed_.split("|")      
    except:
        await cb.message.edit("❌ Pɪᴋᴀ Pɪᴋᴀ, Sᴏɴɢ Nᴏᴛ Fᴏᴜɴᴅ.")
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer("Pɪᴋᴀ Pɪᴋᴀ, Yᴏᴜ Aʀᴇ Nᴏᴛ Pᴇᴏᴘʟᴇ Wʜᴏ Rᴇǫᴜᴇsᴛᴇᴅ Tʜɪs Sᴏɴɢ!", show_alert=True)
        return
    await cb.message.edit("🎥 __**Pɪᴋᴀ Pɪᴋᴀ, Gᴇɴᴇʀᴀᴛɪɴɢ Tʜᴜᴍʙɴᴀɪʟ**__")
    x=int(x)
    try:
        useer_name = cb.message.reply_to_message.from_user.first_name
    except:
        useer_name = cb.message.from_user.first_name
    results = YoutubeSearch(query, max_results=6).to_dict()
    resultss=results[x]["url_suffix"]
    title=results[x]["title"][:25]
    thumbnail=results[x]["thumbnails"][0]
    duration=results[x]["duration"]
    views=results[x]["views"]
    url = f"https://www.youtube.com{resultss}"
    try:    
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
             await cb.message.edit(f"❌ Pɪᴋᴀ Pɪᴋᴀ, Vɪᴅᴇᴏs Lᴏɴɢᴇʀ Tʜᴀɴ `{DURATION_LIMIT}` ᴍɪɴᴜᴛᴇs Aʀᴇɴ'ᴛ Aʟʟᴏᴡᴇᴅ Tᴏ Pʟᴀʏ!")
             return
    except:
        pass
    try:
        thumb_name = f"thumb-{title}veezmusic.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        print(e)
        return
    dlurl=url
    dlurl=dlurl.replace("youtube", "youtubepp")
    keyboard = InlineKeyboardMarkup(
            [
                [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
                ],
                 [InlineKeyboardButton(text="❌ Cʟᴏsᴇ", callback_data="cls")],
            ]
    )
    requested_by = useer_name
    await generate_cover(title, thumbnail)
    file_path = await converter.convert(youtube.download(url))  
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await cb.message.delete()
        await b.send_photo(
        chat_id,
        photo="final.png",
        caption=f"🏷 **Nᴀᴍᴇ :** [{title[:25]}]({url})\n📥 **Dᴏᴡɴʟᴏᴀᴅ :** [ℂ𝕃𝕀ℂ𝕂 ℍ𝔼ℝ𝔼]({dlurl})\n💡 **Qᴜᴇᴜᴇᴅ Aᴛ Pᴏsɪᴛɪᴏɴ :** `{position}`\n" \
                    + f"🎧 **Rᴇǫᴜᴇsᴛ Bʏ :** {message.from_user.mention}",
        reply_markup=keyboard,
        )
        if path.exists("final.png"):
            os.remove("final.png")
    else:
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await cb.message.delete()
        await b.send_photo(
        chat_id,
        photo="final.png",
        caption=f"🏷 **Nᴀᴍᴇ :** [{title[:45]}]({url})\n📥 **Dᴏᴡɴʟᴏᴀᴅ :** [ℂ𝕃𝕀ℂ𝕂 ℍ𝔼ℝ𝔼]({dlurl})\n💡 **Sᴛᴀᴛᴜs :** `Pʟᴀʏɪɴɢ`\n" \
               +f"🎧 **Rᴇǫᴜᴇsᴛ Bʏ :** {r_by.mention}",
        reply_markup=keyboard,
        )
        if path.exists("final.png"):
            os.remove("final.png")


@Client.on_message(command(["ytplay", f"ytplay@{BOT_USERNAME}"]) & other_filters)
async def ytplay(_, message: Message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("🔎 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Fɪɴᴅɪɴɢ...***")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "PikachuXMusic"
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
                        f"<b>Pɪᴋᴀ Pɪᴋᴀ, Pʟᴇᴀsᴇ Aᴅᴅ @PikachuXdAssistant Tᴏ Yᴏᴜʀ Cʜᴀɴɴᴇʟ.</b>",
                    )
                    pass
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>❗Pɪᴋᴀ Pɪᴋᴀ, Mᴀᴋᴇ Mᴇ As Aᴅᴍɪɴ Fɪʀsᴛ.</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "🤖: Pɪᴋᴀ Pɪᴋᴀ, I'ᴍ Jᴏɪɴᴇᴅ Tᴏ Tʜɪs Gʀᴏᴜᴘ Fᴏʀ Pʟᴀʏɪɴɢ Mᴜsɪᴄ Oɴ Vᴏɪᴄᴇ Cʜᴀᴛ."
                    )
                    await lel.edit(
                        "<b>💡 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟᴘᴇʀ Usᴇʀʙᴏᴛ Jᴏɪɴᴇᴅ Yᴏᴜʀ Cʜᴀᴛ.</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>Pɪᴋᴀ Pɪᴋᴀ, ⛑ Fʟᴏᴏᴅ Wᴀɪᴛ Eʀʀᴏʀ ⛑\n@PikachuXdAssistant Cᴏᴜʟᴅɴ'ᴛ Jᴏɪɴ Yᴏᴜʀ Gʀᴏᴜᴘ Dᴜᴇ Tᴏ Mᴀɴʏ Jᴏɪɴ Rᴇǫᴜᴇsᴛs Fᴏʀ Usᴇʀʙᴏᴛ! Mᴀᴋᴇ Sᴜʀᴇ Tʜᴇ Usᴇʀ Is Nᴏᴛ Bᴀɴɴᴇᴅ Iɴ Tʜᴇ Gʀᴏᴜᴘ."
                        f"\n\nOʀ Aᴅᴅ @PikachuXdAssistant Mᴀɴᴜᴀʟʟʏ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Tʀʏ Aɢᴀɪɴ.</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i>Pɪᴋᴀ Pɪᴋᴀ, @PikachuXdAssistant Wᴀs Bᴀɴɴᴇᴅ Iɴ Tʜɪs Gʀᴏᴜᴘ, Asᴋ Aᴅᴍɪɴ Tᴏ Uɴʙᴀɴ @PikachuXdAssistant Mᴀɴᴜᴀʟʟʏ.</i>"
        )
        return
    await lel.edit("🎵 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ...**")
    user_id = message.from_user.id
    user_name = message.from_user.first_name
     

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit("🎥 __**Pɪᴋᴀ Pɪᴋᴀ, Gᴇɴᴇʀᴀᴛɪɴɢ Tʜᴜᴍʙɴᴀɪʟ...**__")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:25]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        await lel.edit(
            "**❗Pɪᴋᴀ Pɪᴋᴀ, Sᴏɴɢ Nᴏᴛ Fᴏᴜɴᴅ."
        )
        print(str(e))
        return
    dlurl=url
    dlurl=dlurl.replace("youtube","youtubepp")
    keyboard = InlineKeyboardMarkup(
        [
                [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
                ],
                 [InlineKeyboardButton(text="❌ Cʟᴏsᴇ", callback_data="cls")],
            ]
    )
    requested_by = message.from_user.first_name
    await generate_cover(title, thumbnail)
    file_path = await convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
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
            caption = f"🏷 **Nᴀᴍᴇ :** [{title[:25]}]({url})\n📥 **Dᴏᴡɴʟᴏᴀᴅ :** [ℂ𝕃𝕀ℂ𝕂 ℍ𝔼ℝ𝔼]({dlurl})\n💡 **Qᴜᴇᴜᴇᴅ Aᴛ Pᴏsɪᴛɪᴏɴ :** `{position}`\n" \
                    + f"🎧 **Rᴇǫᴜᴇsᴛ Bʏ :** {message.from_user.mention}",
                   reply_markup=keyboard,
        )
        os.remove("final.png")
        return 
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("**❗Sᴏʀʀʏ, Nᴏ Aᴄᴛɪᴠᴇ Vᴏɪᴄᴇ Cʜᴀᴛ Hᴇʀᴇ, Pʟᴇᴀsᴇ Tᴜʀɴ Oɴ Tʜᴇ Vᴏɪᴄᴇ Cʜᴀᴛ Fɪʀsᴛ.**")
            return
        await message.reply_photo(
            photo="final.png",
            caption = f"🏷 **Nᴀᴍᴇ :** [{title[:25]}]({url})\n📥 **Dᴏᴡɴʟᴏᴀᴅ :** [ℂ𝕃𝕀ℂ𝕂 ℍ𝔼ℝ𝔼]({dlurl})\n💡 **Sᴛᴀᴛᴜs :** `Playing`\n" \
                    + f"🎧 **Rᴇǫᴜᴇsᴛ Bʏ :** {message.from_user.mention}",
                   reply_markup=keyboard,)
        os.remove("final.png")
        return
