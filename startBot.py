from aiogram import types
from aiogram.utils import executor
from bot import dp
from MSF import Otvet


@dp.message_handler()
async def echo_send(message: types.Message):
    otvet = Otvet(user_id=message.from_user.id, text=message.text)
    await message.answer(otvet.otvet)

executor.start_polling(dp)
