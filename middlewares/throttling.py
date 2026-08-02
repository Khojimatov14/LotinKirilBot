import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 0.5, penalty: float = 2.0) -> None:
        """
        :param limit: Xabarlar orasidagi minimal ruxsat berilgan vaqt (soniya).
        :param penalty: Spam bo'lganda foydalanuvchini bloklash vaqti (soniya).
        """
        self.limit = limit
        self.penalty = penalty
        self.users: Dict[int, Dict[str, Any]] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = None
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
        elif hasattr(event, "from_user") and getattr(event, "from_user"):
            user_id = event.from_user.id

        if not user_id:
            return await handler(event, data)

        current_time = time.time()
        user_data = self.users.get(user_id, {
            "last_time": 0.0,
            "blocked_until": 0.0
        })

        # Agar foydalanuvchi vaqtincha bloklangan bo'lsa, so'rovni e'tiborsiz qoldirish
        if current_time < user_data["blocked_until"]:
            return

        delta = current_time - user_data["last_time"]

        # Agar xabarlar orasidagi vaqt ko'rsatilgan limitdan kam bo'lsa (masalan 0.5 soniyadan kam)
        if delta < self.limit:
            user_data["blocked_until"] = current_time + self.penalty
            self.users[user_id] = user_data

            if isinstance(event, Message):
                await event.reply("<b>So'rov ko'payib ketdi! Iltimos, ozroq kuting.</b>")
            return

        # Ruxsat berilgan so'rov
        user_data["last_time"] = current_time
        user_data["blocked_until"] = 0.0
        self.users[user_id] = user_data

        return await handler(event, data)
