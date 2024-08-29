from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')]
])

subscribe_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписаться', url='https://t.me/+wcVjhfctVNs3ZWZi')],
    [InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')]
])
