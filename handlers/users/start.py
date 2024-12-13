from aiogram import types, F
from aiogram.filters.command import CommandStart, Command
from loader import dp


@dp.message(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(text="Assalomu alekum\nMatn yuboring...\n\nYuborgan matningiz kiril bo'lsa lotin, lotin "
                              "bo'lsa kiril harflariga o'zgartirib beraman!")


@dp.message(Command("bot"))
async def bot_start(message: types.Message):
    await message.answer(text="Assalomu alekum\n\nAgar siz Telegram bot yaratish hizmati kerak bo'lsa menga yozing! "
                              "Yoki qo'ng'iroq qiling!\n\nTelegram: @khojimatov14\n+998 90-626-66-44")