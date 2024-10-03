from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from API import API
from crud_functions import *
import asyncio


api = API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()           # Возраст
    growth = State()        # Рост
    weight = State()        # Вес


class RegistrationState(StatesGroup):
    username = State()      # Никнейм
    email = State()         # Емаил
    age = State()           # Возраст


@dp.message_handler(text = ['Расчитать'])
async def main_menu(message):
    await message.answer('Выберете опцию:', reply_markup = kb_InL)


@dp.callback_query_handler(text= ['formulas'])
async def text_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 х рост (см) - 5 х возраст (г) - 161')
    await call.answer()


@dp.callback_query_handler(text= ['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост.')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес.')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = (10 * int(data["weight"])) + (6.5 * int(data["growth"])) - (5 * int(data["age"])) + 5
    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()


@dp.message_handler(text=['Регистрация'])
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_growth(message, state):
    if is_included(message.text):
        await message.answer('Введите имя пользователя (только латинский алфавит):')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_email(message, state):
    await state.update_data(age=message.text)
    user = await state.get_data()
    add_user(user['username'], user['email'], user['age'])
    await message.answer('Регистрацйия прошла успешно')
    await state.finish()


@dp.message_handler(text = ['Купить!'])
async def get_buying_list(message):
    for product in get_all_products():
        with open(f'files/{product[0]}.png', 'rb') as img:
            await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
            await message.answer_photo(img)
    await message.answer('Выберете продукт для покупки:', reply_markup=kb_inline_buy)


@dp.callback_query_handler(text= ['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)
    initiate_db()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
