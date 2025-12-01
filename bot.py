import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from question import QUESTIONS
from database import save_answer, init_db
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Track question progress for each user
user_progress = {}


def build_keyboard(options, qid):
    inline_keyboard = []

    for opt in options:
        button = InlineKeyboardButton(
            text=opt,
            callback_data=f"{qid}:{opt}"
        )
        inline_keyboard.append([button])  # 1 button per row

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_progress[user_id] = 0
    await send_question(user_id)

async def send_question(user_id):
    index = user_progress.get(user_id, 0)

    if index >= len(QUESTIONS):
        await bot.send_message(user_id, "Thank you! All questions are answered.")
        return

    q = QUESTIONS[index]

    keyboard = build_keyboard(q["options"], q["id"])

    await bot.send_message(
        chat_id=user_id,
        text=q["text"],
        reply_markup=keyboard
    )



@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    qid, answer = callback.data.split(":")

    save_answer(user_id, int(qid), answer)

    user_progress[user_id] += 1

    await callback.answer("Saved!")
    await send_question(user_id)


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
