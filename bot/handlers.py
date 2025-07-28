from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.functions import save_user, States, check_code

router = Router()


# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     user = {
#         'user_id': message.from_user.id,
#         'username': message.from_user.username,
#         'first_name': message.from_user.first_name,
#         'last_name': message.from_user.last_name,
#     }
#     await save_user(**user)
#     text = f"Assalomu alaykum{user['first_name']}"
#     await message.answer(text)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(States.first_name)
    token = message.text.split()[1]
    query = await check_code(token)
    if query:
        await message.answer('Ismingizni kiriting:')
    await message.answer('Bu qr code ishlatilgan')


@router.message(States.first_name)
async def hand_first_name(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await state.set_state(States.last_name)
    await message.answer('Familyani kiriting:')


@router.message(States.last_name)
async def hand_first_name(message: Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    await state.set_state(States.phone_number)
    await message.answer('Telefon raqam kiriting:')


@router.message(States.phone_number)
async def hand_first_name(message: Message, state: FSMContext):
    phone_number = message.text
    data = await state.get_data()
    user = {
        'user_id': message.from_user.id,
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'phone_number': phone_number
    }
    await save_user(**user)
    await message.answer('Muvafaqiyatli saqlandi')
