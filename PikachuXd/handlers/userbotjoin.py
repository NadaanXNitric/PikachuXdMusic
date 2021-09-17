import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from PikachuXd.helpers.filters import command
from PikachuXd.helpers.decorators import authorized_users_only, errors
from PikachuXd.callsmusic.callsmusic import client as USER
from PikachuXd.config import BOT_USERNAME, SUDO_USERS


@Client.on_message(command(["userbotjoin", f"userbotjoin@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Pɪᴋᴀ Pɪᴋᴀ, Mᴀᴋᴇ Mᴇ As Aᴅᴍɪɴ Fɪʀsᴛ.</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: i'm joined here for playing music on voice chat")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟᴘᴇʀ Aʟʀᴇᴀᴅʏ Iɴ Yᴏᴜʀ Cʜᴀᴛ.</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>Pɪᴋᴀ Pɪᴋᴀ, ⛑ Fʟᴏᴏᴅ Wᴀɪᴛ Eʀʀᴏʀ ⛑\n@PikachuXdAssistant Cᴏᴜʟᴅɴ'ᴛ Jᴏɪɴ Yᴏᴜʀ Gʀᴏᴜᴘ Dᴜᴇ Tᴏ Mᴀɴʏ Jᴏɪɴ Rᴇǫᴜᴇsᴛs Fᴏʀ Usᴇʀʙᴏᴛ! Mᴀᴋᴇ Sᴜʀᴇ Tʜᴇ Usᴇʀ Is Nᴏᴛ Bᴀɴɴᴇᴅ Iɴ Tʜᴇ Gʀᴏᴜᴘ."
            "\n\nOʀ Aᴅᴅ @PikachuXdAssistant Mᴀɴᴜᴀʟʟʏ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Tʀʏ Aɢᴀɪɴ.</b>",
        )
        return
    await message.reply_text(
        "<b>Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟᴘᴇʀ Usᴇʀʙᴏᴛ Jᴏɪɴᴇᴅ Yᴏᴜʀ Cʜᴀᴛ.</b>",
    )


@Client.on_message(command(["userbotleave", f"userbotleave@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def rem(client, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>Usᴇʀ Cᴏᴜʟᴅɴ'ᴛ Lᴇᴀᴠᴇ Yᴏᴜʀ Gʀᴏᴜᴘ! Mᴀʏ Bᴇ Fʟᴏᴏᴅᴡᴀɪᴛs."
            "\n\nOʀ Mᴀɴᴜᴀʟʟʏ Kɪᴄᴋ Mᴇ Fʀᴏᴍ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ.</b>",
        )
        return
    
@Client.on_message(command(["userbotleaveall", f"userbotleaveall@{BOT_USERNAME}"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("Pɪᴋᴀ Pɪᴋᴀ, Assɪsᴛᴀɴᴛ Lᴇᴀᴠɪɴɢ Aʟʟ Cʜᴀᴛs.")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Pɪᴋᴀ Pɪᴋᴀ, Assɪsᴛᴀɴᴛ Lᴇᴀᴠɪɴɢ... Lᴇғᴛ : {left} Cʜᴀᴛs. Fᴀɪʟᴇᴅ : {failed} Cʜᴀᴛs.")
            except:
                failed=failed+1
                await lol.edit(f"Pɪᴋᴀ Pɪᴋᴀ, Assɪsᴛᴀɴᴛ Lᴇᴀᴠɪɴɢ... Lᴇғᴛ : {left} Cʜᴀᴛs. Fᴀɪʟᴇᴅ : {failed} Cʜᴀᴛs.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Lᴇғᴛ  {left} Cʜᴀᴛs. Fᴀɪʟᴇᴅ : {failed} Cʜᴀᴛs.")


@Client.on_message(command(["userbotjoinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("is the chat even linked ?")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Pɪᴋᴀ Pɪᴋᴀ, Mᴀᴋᴇ Mᴇ As Aᴅᴍɪɴ Fɪʀsᴛ.</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: i joined here as you requested")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟᴘᴇʀ Aʟʀᴇᴀᴅʏ Iɴ Yᴏᴜʀ Cʜᴀᴛ.</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>Pɪᴋᴀ Pɪᴋᴀ, ⛑ Fʟᴏᴏᴅ Wᴀɪᴛ Eʀʀᴏʀ ⛑\n@PikachuXdAssistant Cᴏᴜʟᴅɴ'ᴛ Jᴏɪɴ Yᴏᴜʀ Gʀᴏᴜᴘ Dᴜᴇ Tᴏ Mᴀɴʏ Jᴏɪɴ Rᴇǫᴜᴇsᴛs Fᴏʀ Usᴇʀʙᴏᴛ! Mᴀᴋᴇ Sᴜʀᴇ Tʜᴇ Usᴇʀ Is Nᴏᴛ Bᴀɴɴᴇᴅ Iɴ Tʜᴇ Gʀᴏᴜᴘ."
            "\n\nOʀ Aᴅᴅ @PikachuXdAssistant Mᴀɴᴜᴀʟʟʏ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Tʀʏ Aɢᴀɪɴ.</b>",
        )
        return
    await message.reply_text(
        "<b>Pɪᴋᴀ Pɪᴋᴀ, Hᴇʟᴘᴇʀ Usᴇʀʙᴏᴛ Jᴏɪɴᴇᴅ Yᴏᴜʀ Cʜᴀᴛ.</b>",
    )
