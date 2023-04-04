""" Team7 || RiZoeL """

import re
from pyrogram import Client, filters
from pyrogram.types import Message

from Team7.functions import itsme, user_in_res, getuser_extra, getuser #user_in_devs, user_in_sudos 
from . import Team7Users, Owners, Devs
from Team7.database import users_db as db
from Team7.core import SEVEN_LOGS, assistant 


@Client.on_message(filters.user(Owners) & filters.command(["adddev"], ["!", "?", "/", "."]))
async def adddev(T7: Client, message: Message):
   user = await getuser(T7, message)
   if await user_in_res(message, user.id):
      return

   db.add_dev(user.id)
   await message.reply(f"User {user.mention} is successfully promoted as Dev ⚜️ -!")

   Logs = "**#NEW DEV**\n\n"
   Logs += f"**× Admin:** {message.from_user.mention} (`{message.from_user.id}`)\n"
   Logs += f"**× User:** {user.mention} (`{user.id}`)"
   await T7.send_message(SEVEN_LOGS, Logs)


@Client.on_message(filters.user(Owners) & filters.command(["addsudo", "addredsudo"], ["!", "?", "/", "."]))
@Client.on_message(filters.user(Devs) & filters.command(["addsudo", "addredsudo"], ["!", "?", "/", "."]))
async def add_user(T7: Client, message: Message):
   user, bot = await getuser_extra(T7, message)
   if await user_in_res(message, user.id):
      return
   if await itsme(message, bot.id):
         return

   if bot.is_bot:
      if db.check_bot(bot.id):
         await message.reply(f"@{bot.username} already in bot list!")
         return 
      db.add_sudo(user.id, bot.username)
      db.add_bot(bot.id, bot.username)
      await message.reply_text(f"User {user.mention} is successfully added in sudo list 👤-!")
      await assistant.send_message(bot.username, "/start")
      Logs = "**#NEW SUDO**\n\n"
      Logs += f"**× Admin:** {message.from_user.mention} (`{message.from_user.id}`)\n"
      Logs += f"**× User:** {user.mention} (`{user.id}`) \n"
      Logs += f"**× Bot:** @{bot.username}"
      await T7.send_message(SEVEN_LOGS, Logs)

   else:
      await message.reply(f"{extra.mention} is not bot!")
      return


@Client.on_message(filters.user(Owners) & filters.command(["addbot"], ["!", "?", "/", "."]))
@Client.on_message(filters.user(Devs) & filters.command(["addbot"], ["!", "?", "/", "."]))
async def add_bot(T7: Client, message: Message):
   bot = await getuser(T7, message)
   if await itsme(message, bot.id):
      return
   if bot.is_bot:
      if db.check_bot(bot.id):
         await message.reply(f"@{bot.username} already in bot list!")
         return
      db.add_bot(bot.id, bot.username)
      await message.reply(f"User {bot.mention} is successfully added in Bot list 🤖 -!")
      await assistant.send_message(bot.username, "/start")
      Logs = "**#NEW BOT**\n\n"
      Logs += f"**× Admin:** {message.from_user.mention} (`{message.from_user.id}`)\n"
      Logs += f"**× Bot:** @{bot.username} (`{bot.id}`)"
      await T7.send_message(SEVEN_LOGS, Logs)

   else:
      await message.reply(f"{extra.mention} is not bot!")
