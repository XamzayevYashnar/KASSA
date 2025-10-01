import os
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

# Bot tokeningiz
TOKEN = "8499926544:AAHsRC7rNtUzA129E2WZWw8hM-e_XmBfpXA"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Fayl manzili
FILE_PATH = "scans.txt"

# Global o'zgaruvchilar
chat_id = None
known_lines = set()
start_time = None


# /start komandasi
@dp.message(Command("start"))
async def start_command(message: Message):
    global chat_id, start_time, known_lines
    chat_id = message.chat.id
    start_time = datetime.now()

    await message.answer(
        "🤖 Assalomu alaykum!\n"
        "✅ Bot faylni kuzatyapti.\n"
        "✍️ Kassir faylga yozsa, yangi yozuvlar darhol keladi.\n"
        "🕒 24 soatdan keyin fayl o‘chiriladi."
    )

    # Fayldagi mavjud yozuvlarni yuborish
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                known_lines = set(lines)  # hammasini eslab qoladi
                await message.answer("📂 Fayldagi mavjud ma'lumotlar:\n\n" + "\n".join(lines))
            else:
                await message.answer("📂 Fayl hozircha bo‘sh.")
    else:
        await message.answer("⚠️ Fayl topilmadi.")


# Faylni kuzatish
async def monitor_file():
    global known_lines, start_time
    while True:
        if chat_id and os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

                # faqat yangi qo‘shilgan qatordan xabar berish
                for line in lines:
                    if line not in known_lines:
                        known_lines.add(line)
                        await bot.send_message(chat_id, f"🆕 Yangi yozuv: {line}")

        # 24 soat o'tganini tekshirish
        if start_time and datetime.now() - start_time >= timedelta(hours=24):
            if os.path.exists(FILE_PATH):
                with open(FILE_PATH, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        await bot.send_message(chat_id, f"📂 Oxirgi fayl mazmuni:\n\n{content}")
                os.remove(FILE_PATH)
                await bot.send_message(chat_id, "🗑 Fayl 24 soatdan keyin o‘chirildi.")
            start_time = None  # qayta hisoblash uchun
            known_lines = set()  # eski yozuvlarni tozalash

        await asyncio.sleep(3)  # har 3 soniyada tekshiradi


async def main():
    asyncio.create_task(monitor_file())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
