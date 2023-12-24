""" Team7 || RiZoeL """

import re
from . import Team7Users, Owners, Devs
from Team7.functions import scanpass, revertpass, get_urp, getuser, user_in_res, check_reason, scan_user_query
from pyrogram import filters, Client
from pyrogram.types import Message 
from Team7.database import report_db

@Client.on_message(filters.user(Team7Users) & filters.command(["scan"], ["!", "?", "/", "."]))
async def scan_user(Team7: Client, message: Message):
    if message.from_user.id == message.chat.id:
       await scan_user_query(Team7, message)
       return 
    user, re, pr = await get_urp(Team7, message)
    if not user:
       return 
    if await user_in_res(message, user.id):
       return

    reason_code, _ = check_reason(re)
    if reason_code == "Null":
       await message.reply(f"Eh! `{re}` is wrong bancode! Type /bancodes to get all bancodes!")
       return
    if pr.startswith("https://telegra.ph/file") or pr.startswith("https://telegra.ph") or pr.startswith("https://graph.org") or pr.startswith("https://graph.org/file"):
        proof = str(pr)
    else:
        await message.reply("need telegraph link as a proof!")
        return
    await scanpass(Team7, message, user, re, proof)

@Client.on_message(filters.user(Team7Users) & filters.command(["revert"], ["!", "?", "/", "."]))
async def revert_user(Team7: Client, message: Message):
    user = await getuser(Team7, message)
    if not user:
        return 
    if await user_in_res(message, user.id):
       return
    await revertpass(Team7, message, user)

@Client.on_message(filters.user(Owners) & filters.command(["rmreport", "removereport"], ["!", "?", "/", "."]))
@Client.on_message(filters.user(Devs) & filters.command(["rmreport", "removereport"], ["!", "?", "/", "."]))
async def removereport(Team7: Client, message: Message):
   user = await getuser(Team7, message)
   if not user:
      return 
   if await user_in_res(message, user.id):
      return

   if report_db.check_report(user.id):
      report_db.rm_report(user.id)
      await message.reply(f"{user.mention} removed from report list!")
   else:
      await message.reply("user not in report list!")
