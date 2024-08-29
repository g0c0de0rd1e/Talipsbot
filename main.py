from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import asyncio
import os
import logging
from functools import lru_cache
import buttons
import aiohttp

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
CHANNEL_URL = os.getenv('CHANNEL_URL')
API_URL = os.getenv('API_URL')  # URL сайта для GET/POST запросов

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

@lru_cache(maxsize=128)
@dp.message(CommandStart())
async def start(message: types.Message):
    args = message.text.split()
    if len(args) > 1:
        # Разделяем параметры
        data = args[1].split('_')
        if len(data) == 3:
            name = data[0]
            surname = data[1]
            phone_number = data[2]
            user_data[message.from_user.id] = phone_number  # Сохраняем номер телефона
            await message.reply(f'Привет, {name} {surname}! Ваш номер телефона: {phone_number}\nПожалуйста, подпишись на наш канал: {CHANNEL_URL}')
        else:
            await message.reply('Неверный формат данных.')
    else:
        await message.reply('Привет!')

    await message.reply('Нажмите кнопку ниже, чтобы проверить подписку:', reply_markup=buttons.menu)

@lru_cache(maxsize=128)
@dp.callback_query(lambda c: c.data == 'check_sub')
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        if member.status != 'left':
            await bot.send_message(callback_query.from_user.id, 'Спасибо за подписку!')
        else:
            await bot.send_message(callback_query.from_user.id, 'Пожалуйста, подпишись на наш канал для продолжения.', reply_markup=buttons.subscribe_button)
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        await bot.send_message(callback_query.from_user.id, 'Произошла ошибка при проверке подписки.')

@dp.message(lambda message: message.chat.id == int(CHANNEL_ID))
async def handle_channel_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    phone_number = user_data.get(user_id) 
    if phone_number:
        data = {
            'phone_number': phone_number,
            'text': text
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=data) as response:
                if response.status == 200:
                    logging.info(f"Сообщение от {phone_number} отправилось успешно.")
                else:
                    logging.error(f"Ошибка отправления сообщения от {phone_number}. Код ошибки: {response.status}")
    else:
        logging.error(f"Номер телефона для пользователя {user_id} не найден.")

if __name__ == '__main__':
    asyncio.run(main())
