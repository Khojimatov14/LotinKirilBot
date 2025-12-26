import os
import sys
import logging
from aiohttp import web
from loader import dp, bot
import middlewares, filters, handlers
from middlewares import ThrottlingMiddleware
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Webhook konfiguratsiyasi
RAILWAY_DOMAIN = "https://lotinkirilbot.up.railway.app"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{RAILWAY_DOMAIN}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8080))


async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    await on_startup_notify()
    await set_default_commands()
    dp.update.middleware.register(ThrottlingMiddleware())


async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()


async def main():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    setup_application(app, dp, bot=bot)
    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    web.run_app(main(), host=WEBAPP_HOST, port=WEBAPP_PORT)
