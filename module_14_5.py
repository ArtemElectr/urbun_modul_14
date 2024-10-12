from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *
import asyncio

initiate_db()
list_products = get_all_products()
list_photo = ['files/shutterstock_71010697.0.jpeg', 'files/8dbf5ae4fdff321c612627522b4efba2.jpg',
              'files/Сок-ананасовый-свежевыжатый.jpg', 'files/tomatnyy-sok.jpeg']

api = '8139003933:AAGYQqobCCfo12tNfBU9kwwI9-o0AdrLBBU'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_ = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Регистрация')],
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [KeyboardButton(text='Купить')]
    ],
    resize_keyboard=True
)


kb = InlineKeyboardMarkup(resize_keyboard=True)
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')

kb.add(button3, button4)

kb_3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Яблочный сок', callback_data='product_buying'),
            InlineKeyboardButton(text='Апельсиновый сок', callback_data='product_buying'),
            InlineKeyboardButton(text='Ананасовый сок', callback_data='product_buying'),
            InlineKeyboardButton(text='Томатный сок', callback_data='product_buying')
        ],

    ],
    resize_keyboard=True
)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer(text='Введите имя пользователя(только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer(text='Введите свой email:')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email = message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age= message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Регистрация прошла успешно.')
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(len(list_products)):
        await message.answer(text=f'Название: {list_products[i][1]} | Описание: {list_products[i][2]} | Цена: {str(list_products[i][3])}')
        with open(list_photo[i], 'rb') as img:
            await message.answer_photo(img)

    await message.answer(text='Выберите продукт для покупки:', reply_markup=kb_3)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer(f'Вы успешно приобрели продукт')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    # для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
    await message.answer(f"Ваша норма калорий {round((10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5), 2)}")
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_)


@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)