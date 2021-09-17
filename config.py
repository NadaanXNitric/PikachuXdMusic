
import os
from os import getenv

from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "Sanki_BOTs")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/10a6ff6687de32dac14a3.png")
admins = {}
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_USERNAME = getenv("BOT_USERNAME")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "PikachuXdAssistant")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "Sanki_BotsSupport")
PROJECT_NAME = getenv("PROJECT_NAME", "PikachuXMusic")
SOURCE_CODE = getenv("SOURCE_CODE", "https://t.me/iTs_Nitric")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "90"))
ARQ_API_KEY = getenv("ARQ_API_KEY", None)
PMPERMIT = getenv("PMPERMIT", None)
LOG_GRP = getenv("LOG_GRP", "1001522296749")
OWNER_NAME = getenv("OWNER_NAME", "iTs_Nitric")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
