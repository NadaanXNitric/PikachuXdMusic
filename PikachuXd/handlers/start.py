from time import time
from datetime import datetime
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_USERNAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import sudo_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>✨ Pɪᴋᴀ Pɪᴋᴀ, Wᴇʟᴄᴏᴍᴇ</b> {query.from_user.mention}!\n\n💭 [{BOT_NAME}](t.me/{UPDATES_CHANNEL}) <b>Aʟʟᴏᴡs Yᴏᴜ Tᴏ Pʟᴀʏ Mᴜsɪᴄ Oɴ Gʀᴏᴜᴘs Tʜʀᴏᴜɢʜ Tʜᴇ Nᴇᴡ Tᴇʟᴇɢʀᴀᴍ's Vᴏɪᴄᴇ Cʜᴀᴛs!</b>\n\n💡 <b>Fɪɴᴅ Oᴜᴛ</b> Aʟʟ Tʜᴇ <b>Bᴏᴛ</b>'s <b>Cᴏᴍᴍᴀᴍᴅs</b> Aɴᴅ Hᴏᴡ Tʜᴇʏ <b>Wᴏʀᴋ</b> Bʏ Cʟɪᴄᴋɪɴɢ Oɴ Tʜᴇ » 📚 <b>Cᴏᴍᴍᴀɴᴅs</b> Bᴜᴛᴛᴏɴ!""",
        reply_markup=InlineKeyboardMarkup(
           [ 
                [
                    InlineKeyboardButton(
                        "➕ Sᴜᴍᴍᴏɴ Mᴇ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                         "📚 Cᴏᴍᴍᴀɴᴅs", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        "❤️ Dᴏɴᴀᴛᴇ", url=f"https://t.me/{OWNER_USERNAME}")
                ],[
                    InlineKeyboardButton(
                        "👥 Oғғɪᴄɪᴀʟ Gʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Oғғɪᴄɪᴀʟ Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton(
                        "❗️ Iɴғᴏ & Aʙᴏᴜᴛ 👨‍💻", callback_data="cbinfo")
                ],[
                    InlineKeyboardButton(
                        "🧪 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ 🧪", url="https://t.me/Sanki_BOTs"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""✅ **Pɪᴋᴀ Pɪᴋᴀ, Bᴏᴛ Is Rᴜɴɴɪɴɢ**\n<b>💠 **Uᴘᴛɪᴍᴇ :**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨ Gʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋🏻 **Pɪᴋᴀ Pɪᴋᴀ,** {message.from_user.mention()}</b>
**Pʟᴇᴀss Pʀᴇss Tʜᴇ Bᴜᴛᴛᴏɴ Bᴇʟᴏᴡ Tᴏ Rᴇᴀᴅ Tʜᴇ Exᴘʟᴀᴛɪᴏɴ Aɴᴅ Sᴇᴇ Tʜᴇ Lɪsᴛ Oғ Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs !**
⚡ __Pᴏᴡᴇʀᴇᴅ bʏ {BOT_NAME} A.I.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="❔ Hᴏᴡ Tᴏ Usᴇ Mᴇ", callback_data="cbguide"
                    )
                ]
            ]
        ),
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>💡 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟʟᴏ {message.from_user.mention}, Wᴇʟᴄᴏᴍᴇ Tᴏ Tʜᴇ Hᴇʟᴘ Mᴇɴᴜ!</b>
**in this menu you can open several available command menus, in each command menu there is also a brief explanation of each command**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Bᴀsɪᴄ Cᴍᴅ", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 Aᴅᴠᴀɴᴄᴇᴅ Cᴍᴅ", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Aᴅᴍɪɴ Cᴍᴅ", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Sᴜᴅᴏ Cᴍᴅ", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📙 Oᴡɴᴇʀ Cᴍᴅ", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📔 Fᴜɴ Cᴍᴅ", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ Tᴏ Hᴏᴍᴇ", callback_data="cbstart"
                    )
                ],
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("Pɪɴɢɪɴɢ...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🏓 `Pɪᴋᴀ Pɪᴋᴀ Pᴏɴɢ !!`\n"
        f"⚡️ `{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 Pɪᴋᴀ Pɪᴋᴀ, Bᴏᴛ Sᴛᴀᴛᴜs\n"
        f"• **Uᴘᴛɪᴍᴇ :** `{uptime}`\n"
        f"• **Sᴛᴀʀᴛ Tɪᴍᴇ :** `{START_TIME_ISO}`"
    )
