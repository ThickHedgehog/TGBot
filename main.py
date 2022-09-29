import sqlite3

from datetime import datetime
import logging
import config
import emoji
from aiogram import Bot, Dispatcher, executor, types
from db import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


@dp.message_handler(commands=["mute"], commands_prefix="/")
async def mute(message: types.Message):
    if not db.mute(message.from_user.id):
        text = message.text.lower()
        if str(message.from_user.id) in config.ADMIN_ID:
            if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение")
                return

            mute_min = [int(s) for s in str.split(message.text) if s.isdigit()]
            db.add_mute(message.reply_to_message.from_user.id, int(mute_min[0]))
            await message.bot.delete_message(config.GROUP_ID, message.message_id)
            await message.reply_to_message.reply(f"Замучен на {mute_min[0]} минут")

        if message.from_user.id == 304555106:
            await bot.send_message(config.GROUP_ID, emoji.emojize("\u2b06") + emoji.emojize(
                "\N{pig}") + "СВИНЬЯ ХРЮКНУЛА" + emoji.emojize("\N{pig}") + emoji.emojize(
                "\u2b06"))

        if "хрюканина" in text:
            db.upd_timer(10)

        if db.timer() and message.from_user.id == 5201297228:
            await bot.send_message(config.GROUP_ID, emoji.emojize("\u2b06") + emoji.emojize(
                "\N{pile of poo}") + "ДЕБИЛ НАСРАЛ" + emoji.emojize("\N{pile of poo}") + emoji.emojize("\u2b06"))

    else:
        await message.delete()


@dp.message_handler(commands=["getID"], commands_prefix="/")
async def send_ID(message: types.Message):
    await bot.send_message(message.from_user.id, f"ID: {message.from_user.id}")


@dp.message_handler()
async def msg_handler(message: types.Message):
    text = message.text.lower()
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)

    if not db.mute(message.from_user.id):
        print(message.from_user.id)
        if message.from_user.id == 304555106:
            await bot.send_message(config.GROUP_ID, emoji.emojize("\u2b06") + emoji.emojize(
                "\N{pig}") + "СВИНЬЯ ХРЮКНУЛА" + emoji.emojize("\N{pig}") + emoji.emojize(
                "\u2b06"))

        if "хрюканина" in text:
            db.upd_timer(10)

        if db.timer() and message.from_user.id == 5201297228:
            await bot.send_message(config.GROUP_ID, emoji.emojize("\u2b06") + emoji.emojize(
                "\N{pile of poo}") + "ДЕБИЛ НАСРАЛ" + emoji.emojize("\N{pile of poo}") + emoji.emojize("\u2b06"))

    else:
        await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
