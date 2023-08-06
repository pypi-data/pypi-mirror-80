from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.chat_member import ChatMemberStatus

from aiogram_oop_framework.views import MessageView, CallbackQueryView
from aiogram_oop_framework.filters import filter_execute


class Example(MessageView):

    @staticmethod
    async def execute(m: types.Message, state: FSMContext = None, **kwargs):
        await m.answer('undef')

    @classmethod
    @filter_execute(chat_member_status=ChatMemberStatus.ADMINISTRATOR)
    async def execute_in_supergroup(cls, m: types.Message, state: FSMContext = None, **kwargs):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('gg', callback_data='gg'))
        await m.answer('gg admin brr', reply_markup=kb)

    @staticmethod
    @filter_execute(chat_member_status=ChatMemberStatus.CREATOR)
    async def execute_for_creators(m: types.Message, state: FSMContext = None, **kwargs):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('gg', callback_data='gg'))
        await m.answer('gg creator brr', reply_markup=kb)


class Example1(CallbackQueryView):

    @classmethod
    async def execute(cls, q: types.CallbackQuery, state: FSMContext = None, **kwargs):
        await q.answer('undef')

    @staticmethod
    @filter_execute(chat_member_status=ChatMemberStatus.ADMINISTRATOR)
    async def execute_for_admins(q: types.CallbackQuery, state: FSMContext = None, **kwargs):
        await q.answer('gg ADMIN brr')

    @classmethod
    @filter_execute(chat_member_status=ChatMemberStatus.CREATOR)
    async def execute_for_creators(cls, q: types.CallbackQuery, state: FSMContext = None, **kwargs):
        await q.answer('gg CREATOR brr')
