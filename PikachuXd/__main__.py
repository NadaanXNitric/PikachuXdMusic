import requests
from pyrogram import Client as Bot

from PikachuXd.callsmusic import run
from PikachuXd.config import API_ID, API_HASH, BOT_TOKEN, BG_IMAGE

response = requests.get(BG_IMAGE)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)


bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="PikachuXd/handlers"),
)

print("[INFO]:  STARTED Join @Sanki_BOTs!")

bot.start()
run()
