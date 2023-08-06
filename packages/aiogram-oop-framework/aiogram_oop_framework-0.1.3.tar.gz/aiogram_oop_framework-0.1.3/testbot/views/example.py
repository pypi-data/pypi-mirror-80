from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram_oop_framework.views import MessageView, CallbackQueryView


class Example(MessageView):

    @staticmethod
    async def execute(m: types.Message, state: FSMContext = None, **kwargs):
        await m.answer('undef')

    @classmethod
    async def execute_in_private(cls, m: types.Message, state: FSMContext = None, **kwargs):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('gg', callback_data='gg'))
        await m.answer('gg private brr', reply_markup=kb)

    @staticmethod
    async def execute_in_supergroup(m: types.Message, state: FSMContext = None, **kwargs):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('gg', callback_data='gg'))
        await m.answer('gg supergroup brr', reply_markup=kb)


class Example1(CallbackQueryView):

    @classmethod
    async def execute(cls, q: types.CallbackQuery, state: FSMContext = None, **kwargs):
        await q.answer('undef')

    @staticmethod
    async def execute_in_private(q: types.CallbackQuery, state: FSMContext = None, **kwargs):
        await q.answer('gg private brr')

    @classmethod
    async def execute_in_supergroup(cls, q: types.CallbackQuery, state: FSMContext = None, **kwargs):
        await q.answer('gg supergroup brr')
