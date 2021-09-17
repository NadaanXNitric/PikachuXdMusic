from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import BOT_NAME, BOT_USERNAME, OWNER_USERNAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME, OWNER_USERNAME
from handlers.play import cb_admin_check


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
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


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟʟᴏ Tʜᴇʀᴇ, Wᴇʟᴄᴏᴍᴇ Tᴏ Tʜᴇ Hᴇʟᴘ Mᴇɴᴜ!</b>

**Iɴ Tʜɪs Mᴇɴᴜ Yᴏᴜ Cᴀɴ Oᴘᴇɴ Sᴇᴠᴇʀᴀʟ Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅ Mᴇɴᴜ, Iɴ Eᴀᴄʜ Cᴏᴍᴍᴀɴᴅ Mᴇɴᴜ Tʜᴇʀᴇ Is Aʟsᴏ A Bʀɪᴇғ Exᴘʟᴀɴᴀᴛɪᴏɴ Oғ Eᴀᴄʜ Cᴏᴍᴍᴀɴᴅ**""",
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
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʀᴇ Is Tʜᴇ Bᴀsɪᴄ Cᴏᴍᴍᴀɴᴅs</b>

🎧 [ ɢʀᴏᴜᴘ ᴠᴄ ᴄᴍᴅ ]

/play (sᴏɴɢ ɴᴀᴍᴇ) - ᴘʟᴀʏ sᴏɴɢ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ
/ytplay (sᴏɴɢ ɴᴀᴍᴇ) - ᴘʟᴀʏ sᴏɴɢ ᴅɪʀᴇᴄᴛʟʏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ
/audio (ʀᴇᴘʟʏ ᴛᴏ ᴀᴜᴅɪᴏ) - ᴘʟᴀʏ sᴏɴɢ ᴜsɪɴɢ ᴀᴜᴅɪᴏ ғɪʟᴇ
/playlist - sʜᴏᴡ ᴛʜᴇ ʟɪsᴛ sᴏɴɢ ɪɴ ǫᴜᴇᴜᴇ
/song (sᴏɴɢ ɴᴀᴍᴇ) - ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ
/search (ᴠɪᴅᴇᴏ ɴᴀᴍᴇ) - sᴇᴀʀᴄʜ ᴠɪᴅᴇᴏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ᴅᴇᴛᴀɪʟᴇᴅ
/vsong (ᴠɪᴅᴇᴏ ɴᴀᴍᴇ) - ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ᴅᴇᴛᴀɪʟᴇᴅ
/lyric - (sᴏɴɢ ɴᴀᴍᴇ) ʟʏʀɪᴄs sᴄʀᴀᴘᴘᴇʀ
/vk (sᴏɴɢ ɴᴀᴍᴇ) - ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ғʀᴏᴍ ɪɴʟɪɴᴇ ᴍᴏᴅᴇ

🎧 [ ᴄʜᴀɴɴᴇʟ ᴠᴄ ᴄᴍᴅ ]

/cplay - sᴛʀᴇᴀᴍ ᴍᴜsɪᴄ ᴏɴ ᴄʜᴀɴɴᴇʟ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ
/cplayer - sʜᴏᴡ ᴛʜᴇ sᴏɴɢ ɪɴ sᴛʀᴇᴀᴍɪɴɢ
/cpause - ᴘᴀᴜsᴇ ᴛʜᴇ sᴛʀᴇᴀᴍɪɴɢ ᴍᴜsɪᴄ
/cresume - ʀᴇsᴜᴍᴇ ᴛʜᴇ sᴛʀᴇᴀᴍɪɴɢ ᴡᴀs ᴘᴀᴜsᴇᴅ
/cskip - sᴋɪᴘ sᴛʀᴇᴀᴍɪɴɢ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ sᴏɴɢ
/cend - ᴇɴᴅ ᴛʜᴇ sᴛʀᴇᴀᴍɪɴɢ ᴍᴜsɪᴄ
/admincache - ʀᴇғʀᴇsʜ ᴛʜᴇ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ
/ubjoinc - ɪɴᴠɪᴛᴇ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ғᴏʀ ᴊᴏɪɴ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʀᴇ Is Tʜᴇ Aᴅᴠᴀɴᴄᴇᴅ Cᴏᴍᴍᴀɴᴅs</b>

/start (ɪɴ ɢʀᴏᴜᴘ) - sᴇᴇ ᴛʜᴇ ʙᴏᴛ ᴀʟɪᴠᴇ sᴛᴀᴛᴜs
/reload - ʀᴇʟᴏᴀᴅ ʙᴏᴛ ᴀɴᴅ ʀᴇғʀᴇsʜ ᴛʜᴇ ᴀᴅᴍɪɴ ʟɪsᴛ
/cache - ʀᴇғʀᴇsʜ ᴛʜᴇ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ
/ping - ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴘɪɴɢ sᴛᴀᴛᴜs
/uptime - ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴜᴘᴛɪᴍᴇ sᴛᴀᴛᴜs""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʀᴇ Is Tʜᴇ Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs</b>

/player - sʜᴏᴡ ᴛʜᴇ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ sᴛᴀᴛᴜs
/pause - ᴘᴀᴜsᴇ ᴛʜᴇ ᴍᴜsɪᴄ sᴛʀᴇᴀᴍɪɴɢ
/resume - ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴍᴜsɪᴄ ᴡᴀs ᴘᴀᴜsᴇᴅ
/skip - sᴋɪᴘ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ sᴏɴɢ
/end - sᴛᴏᴘ ᴍᴜsɪᴄ sᴛʀᴇᴀᴍɪɴɢ
/userbotjoin - ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ
/auth - ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ ғᴏʀ ᴜsɪɴɢ ᴍᴜsɪᴄ ʙᴏᴛ
/deauth - ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ғᴏʀ ᴜsɪɴɢ ᴍᴜsɪᴄ ʙᴏᴛ
/control - ᴏᴘᴇɴ ᴛʜᴇ ᴘʟᴀʏᴇʀ sᴇᴛᴛɪɴɢs ᴘᴀɴᴇʟ
/delcmd (on | off) - enable / disable del ᴄᴍᴅ ғᴇᴀᴛᴜʀᴇ del ᴄᴍᴅ ғᴇᴀᴛᴜʀᴇ
/musicplayer (on / off) - disable / enable ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ
/b and /tb (ban / temporary ban) - ʙᴀɴɴᴇᴅ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ ᴏʀ ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪɴ ɢʀᴏᴜᴘ
/ub - ᴛᴏ ᴜɴʙᴀɴɴᴇᴅ ᴜsᴇʀ ʏᴏᴜ'ʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ɢʀᴏᴜᴘ
/m and /tm (mute / temporary mute) - ᴍᴜᴛᴇ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ ᴏʀ ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ᴍᴜᴛᴇᴅ ᴜsᴇʀ ɪɴ ɢʀᴏᴜᴘ
/um - ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴜsᴇʀ ʏᴏᴜ'ʀᴇ ᴍᴜᴛᴇᴅ ɪɴ ɢʀᴏᴜᴘ""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʀᴇ Is Tʜᴇ Sᴜᴅᴏ Cᴏᴍᴍᴀɴᴅs</b>

/userbotleaveall - ᴏʀᴅᴇʀ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ ʟᴇᴀᴠᴇ ғʀᴏᴍ ᴀʟʟ ɢʀᴏᴜᴘ
/gcast - sᴇɴᴅ ᴀ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ ᴛʀᴏᴜɢʜᴛ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ
/stats - sʜᴏᴡ ᴛʜᴇ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄ
/rmd - ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ғɪʟᴇs
/clean - ʀᴇᴍᴏᴠᴇ ᴀʟʟ ʀᴀᴡ ғɪʟᴇs""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʀᴇ Is Tʜᴇ Oᴡɴᴇʀ Cᴏᴍᴍᴀɴᴅs</b>

/stats - sʜᴏᴡ ᴛʜᴇ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄ
/broadcast - sᴇɴᴅ ᴀ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ʙᴏᴛ
/block (ᴜsᴇʀ ɪᴅ - ᴅᴜʀᴀᴛɪᴏɴ - ʀᴇᴀsᴏɴ) - ʙʟᴏᴄᴋ ᴜsᴇʀ ғᴏʀ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ
/unblock (ᴜsᴇʀ ɪᴅ - ʀᴇᴀsᴏɴ) - ᴜɴʙʟᴏᴄᴋ ᴜsᴇʀ ʏᴏᴜ ʙʟᴏᴄᴋᴇᴅ ғᴏʀ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ
/blocklist - sʜᴏᴡ ʏᴏᴜ ᴛʜᴇ ʟɪsᴛ ᴏғ ᴜsᴇʀ ᴡᴀs ʙʟᴏᴄᴋᴇᴅ ғᴏʀ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ

📝 ɴᴏᴛᴇ: ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴏᴡɴᴇᴅ ʙʏ ᴛʜɪs ʙᴏᴛ ᴄᴀɴ ʙᴇ ᴇxᴇᴄᴜᴛᴇᴅ ʙʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ʙᴏᴛ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴇxᴄᴇᴘᴛɪᴏɴs.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbfun"))
async def cbfun(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʀᴇ Is Tʜᴇ Fᴜɴ Cᴏᴍᴍᴀɴᴅs</b>

/chika - ᴄʜᴇᴄᴋ ɪᴛ ʙʏ ʏᴏᴜʀsᴇʟғ
/wibu - ᴄʜᴇᴄᴋ ɪᴛ ʙʏ ʏᴏᴜʀsᴇʟғ
/asupan - ᴄʜᴇᴄᴋ ɪᴛ ʙʏ ʏᴏᴜʀsᴇʟғ
/truth - ᴄʜᴇᴄᴋ ɪᴛ ʙʏ ʏᴏᴜʀsᴇʟғ
/dare - ᴄʜᴇᴄᴋ ɪᴛ ʙʏ ʏᴏᴜʀsᴇʟғ""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ Hᴏᴡ Tᴏ Usᴇ Tʜɪs Bᴏᴛ :

1.) Fɪʀsᴛ, Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ.
2.) Tʜᴇɴ Pʀᴏᴍᴏᴛᴇ Mᴇ As Aᴅᴍɪɴ Aɴᴅ Gɪᴠᴇ Aʟʟ Pᴇʀᴍɪssɪᴏɴs Exᴄᴇᴘᴛ Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴ.
3.) Aᴅᴅ @{ASSISTANT_NAME} Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Oʀ Tʏᴘᴇ /userbotjoin Tᴏ Iɴᴠɪᴛᴇ Hᴇʀ.
4.) Tᴜʀɴ Oɴ Tʜᴇ Vᴏɪᴄᴇ Cʜᴀᴛ Fɪʀsᴛ Bᴇғᴏʀᴇ Sᴛᴀʀᴛ Tᴏ Pʟᴀʏ Mᴜsɪᴄ.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Cᴏᴍᴍᴀᴍᴅ Lɪsᴛ", callback_data="cbhelp"
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


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbback"))
@cb_admin_check
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        "**💡 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʀᴇ Is Tʜᴇ Cᴏɴᴛʀᴏʟ Mᴇɴᴜ Oғ Bᴏᴛ :**",
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


@Client.on_callback_query(filters.regex("cbgtools"))
@cb_admin_check
@authorized_users_only
async def cbgtools(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Pɪᴋᴀ Pɪᴋᴀ, Tʜɪs Is Tʜᴇ Fᴇᴀᴛᴜʀᴇ Iɴғᴏʀᴍᴀᴛɪᴏɴ :</b>

💡 **ғᴇᴀᴛᴜʀᴇ :** ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ᴄᴏɴᴛᴀɪɴs ғᴜɴᴄᴛɪᴏɴs ᴛʜᴀᴛ ᴄᴀɴ ʙᴀɴ, ᴍᴜᴛᴇ, ᴜɴʙᴀɴ, ᴜɴᴍᴜᴛᴇ ᴜsᴇʀs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.

ᴀɴᴅ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ sᴇᴛ ᴀ ᴛɪᴍᴇ ғᴏʀ ᴛʜᴇ ʙᴀɴ ᴀɴᴅ ᴍᴜᴛᴇ ᴘᴇɴᴀʟᴛɪᴇs ғᴏʀ ᴍᴇᴍʙᴇʀs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ᴛʜᴇʏ ᴄᴀɴ ʙᴇ ʀᴇʟᴇᴀsᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴘᴜɴɪsʜᴍᴇɴᴛ ᴡɪᴛʜ ᴛʜᴇ sᴘᴇᴄɪғɪᴇᴅ ᴛɪᴍᴇ.

❔ **ᴜsᴀɢᴇ :**

1️⃣ ʙᴀɴ & ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ʙᴀɴ ᴜsᴇʀ ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ :
   » type `/b username/reply to message` ban permanently
   » type `/tb username/reply to message/duration` temporarily ban user
   » type `/ub username/reply to message` to unban user

2️⃣ mute & temporarily mute user in your group:
   » type `/m username/reply to message` mute permanently
   » type `/tm username/reply to message/duration` temporarily mute user
   » type `/um username/reply to message` to unmute user

📝 note: cmd /b, /tb and /ub is the function to banned/unbanned user from your group, whereas /m, /tm and /um are commands to mute/unmute user in your group.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 Gᴏ Bᴀᴄᴋ", callback_data="cbback"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
@cb_admin_check
@authorized_users_only
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Pɪᴋᴀ Pɪᴋᴀ, Tʜɪs Is Tʜᴇ Fᴇᴀᴛᴜʀᴇ Iɴғᴏʀᴍᴀᴛɪᴏɴ :</b>
        
**💡 ғᴇᴀᴛᴜʀᴇ:** ᴅᴇʟᴇᴛᴇ ᴇᴠᴇʀʏ ᴄᴏᴍᴍᴀɴᴅs sᴇɴᴛ ʙʏ ᴜsᴇʀs ᴛᴏ ᴀᴠᴏɪᴅ sᴘᴀᴍ ɪɴ ɢʀᴏᴜᴘs !

❔ ᴜsᴀɢᴇ:**

 1️⃣ ᴛᴏ ᴛᴜʀɴ ᴏɴ ғᴇᴀᴛᴜʀᴇ:
     » type `/delcmd on`
    
 2️⃣ to turn off feature:
     » type `/delcmd off`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 Gᴏ Bᴀᴄᴋ", callback_data="cbback"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟʟᴏ Tʜᴇʀᴇ, Wᴇʟᴄᴏᴍᴇ Tᴏ Tʜᴇ Hᴇʟᴘ Mᴇɴᴜ!</b>

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
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ Hᴏᴡ Tᴏ Usᴇ Tʜɪs Bᴏᴛ:

1.) ғɪʀsᴛ, ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
2.) ᴛʜᴇɴ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴀɴᴅ ɢɪᴠᴇ ᴀʟʟ ᴘᴇʀᴍɪssɪᴏɴs ᴇxᴄᴇᴘᴛ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.
3.) ᴀᴅᴅ @{ASISTANT_NAME} ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ᴛʏᴘᴇ /userbotjoin ᴛᴏ ɪɴᴠɪᴛᴇ ʜᴇʀ.
4.) ᴛᴜʀɴ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғɪʀsᴛ ʙᴇғᴏʀᴇ sᴛᴀʀᴛ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ Tᴏ Hᴏᴍᴇ", callback_data="cbinfo"
                    )
                ]
            ]
        )
    )

@Client.on_callback_query(filters.regex("cbinfo"))
async def cbinfo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**👩‍💻 ɪɴғᴏʀᴍᴀᴛɪᴏɴ** \n\n`🤖 ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴘʏᴛɢᴄᴀʟʟs ᴛʜᴇ ᴀsʏɴᴄ ᴄʟɪᴇɴᴛ ᴀᴘɪ ғᴏʀ ᴛʜᴇ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ ᴄᴀʟʟs.` \n\n**ᴛʜɪs ʙᴏᴛ ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ɢɴᴜ-ɢᴘʟ 3.0 ʟɪᴄᴇɴsᴇ.**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❓ Hᴏᴡ Tᴏ Usᴇ Mᴇ", callback_data="cbhowtouse"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🧑‍💻Dᴇᴠs", callback_data="cbdevs"
                    ),
                     InlineKeyboardButton(
                        "❓ Cᴏᴍᴍᴀɴᴅs", callback_data="cbcmds"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ Tᴏ Hᴏᴍᴇ", callback_data="cbstart"
                    )
                ]
            ]
        )
    )

@Client.on_callback_query(filters.regex("cbdevs"))
async def cbdevs(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**ᴄʀᴇᴅɪᴛ ᴠᴄ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ** \n\n`ʜᴇʀᴇ sᴏᴍᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀs ʜᴇʟᴘɪɴɢ ɪɴ ᴍᴀᴋɪɴɢ ᴛʜᴇ` **ᴘɪᴋᴀᴄʜᴜ • ᴍᴜsɪᴄ**.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Nɪᴛʀɪᴄ (Oᴡɴᴇʀ)", url=f"https://t.me/iTs_Nitric"
                    ),
                     InlineKeyboardButton(
                        "Vɪᴄᴋs", url=f"https://t.me/viichitrapraani"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Hᴇxᴏʀ", url=f"https://t.me/iTs_Hexor"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏡 Bᴀᴄᴋ Tᴏ Hᴏᴍᴇ", callback_data="cbinfo"
                    )
                ]
            ]
        )
    )


