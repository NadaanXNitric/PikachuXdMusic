import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Pɪᴋᴀᴄʜᴜ • Mᴜsɪᴄ")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/20147c4f049e2c1f2f248.png")
THUMB_IMG = getenv("THUMB_IMG", None)
AUD_IMG = getenv("AUD_IMG", None)
QUE_IMG = getenv("QUE_IMG", None)
admins = {}
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_USERNAME = getenv("BOT_USERNAME", "PikachuXdBot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "PikachuXdAssistant")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "Sanki_BOTs_Support")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "Sanki_BOTs")
OWNER_NAME = getenv("OWNER_NAME", "iTs_Nitric") # isi dengan username kamu tanpa simbol @
DEV_NAME = getenv("DEV_NAME", "iTs_Nitric")
PMPERMIT = getenv("PMPERMIT", None)
LOG_CHANNEL = getenv("LOG_CHANNEL", "1001334104062)
OWNER_ID = getenv("OWNER_ID", "1961533931)

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "90"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
