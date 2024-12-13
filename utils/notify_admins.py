from data.config import ADMINS
from loader import bot
import logging


async def on_startup_notify():
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="Bot ishga tushdi!")
        except Exception as err:
            logging.exception(err)
