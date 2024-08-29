from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_URL = os.getenv('CHANNEL_URL')

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')]
])

subscribe_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписаться', url=CHANNEL_URL)],
    [InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')]
])
