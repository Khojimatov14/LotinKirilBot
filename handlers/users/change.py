from aiogram.types import Message
from loader import dp
from utils.functions import get_words


@dp.message()
async def change_alpha(message: Message):
    await message.answer(text=get_words(text=message.text))

