""" © Team7 RiZoeL """
import time, datetime

from . import Team7Users

from Team7 import start_time
from Team7.functions import report_user_query, get_time
from Team7.core import inline_alive_msg, get_inline_stats

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Client.on_callback_query()
async def T7callbacks(T7: Client, callback_query: CallbackQuery):
   query = callback_query.data.lower()
   chat = callback_query.message.chat
   admin = callback_query.from_user
   message = callback_query.message
   if query == "do_report":
      if admin.id in Team7Users:
         await callback_query.answer("You have rights to scan!", show_alert=True)
      else:
         await callback_query.answer("Follow process!", show_alert=True)
         await callback_query.delete()
         await report_user_query(T7, message)

   elif query == "ping":
      start = datetime.datetime.now()
      uptime = await get_time((time.time() - start_time))
      end = datetime.datetime.now()
      ms = (end-start).microseconds / 1000
      await callback_query.answer(f"Team7 Scanner Here!\n\n Ping: {ms}ms \n Uptime: {uptime}", show_alert=True)

   elif query == "alive":
      await callback_query.answer(inline_alive_msg, show_alert=True)

   elif query == "stats":
      await callback_query.answer(get_inline_stats(), show_alert=True)

   

