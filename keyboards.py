from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Расчитать'), KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить!'), KeyboardButton(text='Регистрация')]
    ], resize_keyboard=True
)

kb_inline_buy = InlineKeyboardMarkup(
    inline_keyboard=[
        [
        InlineKeyboardButton(text='Product1', callback_data='product_buying'),
        InlineKeyboardButton(text='Product2', callback_data='product_buying'),
        InlineKeyboardButton(text='Product3', callback_data='product_buying'),
        InlineKeyboardButton(text='Product4', callback_data='product_buying')
         ]
    ]
)


kb_InL = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)
