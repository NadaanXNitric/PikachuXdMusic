# this module i created only for playing music using audio file, idk, because the audio player on play.py module not working
# so this is the alternative
# audio play function

from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from PikachuXd.callsmusic import callsmusic, queues

import PikachuXd.converter
from PikachuXd.downloaders import youtube

from PikachuXd.config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, AUD_IMG, QUE_IMG, GROUP_SUPPORT
from PikachuXd.helpers.filters import command, other_filters
from PikachuXd.helpers.decorators import errors
from PikachuXd.helpers.errors import DurationLimitError
from PikachuXd.helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(command("audio") & other_filters)
@errors
async def stream(_, message: Message):

    lel = await message.reply("🔁 **Pɪᴋᴀ Pɪᴋᴀ, Aᴍ Pʀᴏᴄᴇssɪɴɢ Sᴏᴜɴᴅ...")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✨ Gʀᴏᴜᴘ",
                        url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton(
                        text="🌻 Cʜᴀɴɴᴇʟ",
                        url=f"https://t.me/{UPDATES_CHANNEL}")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Pɪᴋᴀ Pɪᴋᴀ, Vɪᴅᴇᴏs Lᴏɴɢᴇʀ Tʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs Aʀᴇɴ'ᴛ Aʟʟᴏᴡᴇᴅ Tᴏ Pʟᴀʏ!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("❗Pɪᴋᴀ Pɪᴋᴀ, Yᴏᴜ Dɪᴅ Nᴏᴛ Gɪᴠᴇ Mᴇ Aᴜᴅɪᴏ Fɪʟᴇ Oʀ Yᴛ Lɪɴᴋ Tᴏ Sᴛʀᴇᴀᴍ!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"{QUE_IMG}",
        reply_markup=keyboard,
        caption=f"💡 Pɪᴋᴀ Pɪᴋᴀ, Tʀᴀᴄᴋ Aᴅᴅᴇᴅ Tᴏ Tʜᴇ **queue**\n\n🔢 Pᴏsɪᴛɪᴏɴ: » `{position}` «\n🎧 Rᴇǫᴜᴇsᴛ Bʏ : {costumer}\n\n⚡ __Pᴏᴡᴇʀᴇᴅ Bʏ {bn} ᴀ.ɪ.__")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"{AUD_IMG}",
        reply_markup=keyboard,
        caption=f"💡 Pɪᴋᴀ Pɪᴋᴀ, **Sᴛᴀᴛᴜs**: `Pʟᴀʏɪɴɢ`\n🎧 Rᴇǫᴜᴇsᴛ Bʏ : {costumer}\n\n⚡ __Pᴏᴡᴇʀᴇᴅ Bʏ {bn} ᴀ.ɪ.__"
        )
        return await lel.delete()
