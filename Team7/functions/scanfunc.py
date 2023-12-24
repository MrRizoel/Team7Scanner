""" © Team7 || RiZoeL """

from Team7.database import users_db, scan_db, report_db
from Team7.core import Team7Scanner, assistant, SCAN_LOGS as seven_logs
from Team7.core.errors import user_errors

from pyrogram import filters 
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from .revertfunc import revertcallpass
from .check_reason import check_reason
from .redfunc import passcmd_to_red 
from .basic import make_tg, user_in_res


scan_cmd = """
/gban {} 
Reason: {}
Proof: {}

Note: user {} is official scanned by Team7 || Red7
"""

async def scanpass(T7, message, user, reason_code, proof):
   reason, red7code = check_reason(reason_code)
   if scan_db.check_scan(user.id):
      alreson = check_reason(scan_db.check_scan(user.id).reason)
      await message.reply(f"User {user.mention} already in scan list \nReason: {alreson}")
      return
   if user.username:
      bancmd = scan_cmd.format(f"@{user.username}", reason, proof, user.first_name)
   else:
      bancmd = scan_cmd.format(user.id, reason, proof, user.first_name)

   huh = await message.reply("Passing cmd..")
   done = 0
   fail = 0
   for bot in users_db.get_all_bots():
      try:
         await assistant.send_message(bot.username, bancmd)
         done += 1
      except:
         try:
            await assistant.send_message(bot.user_id, bancmd)
            done += 1
         except:
            fail += 1

   final_text = f"User {user.mention} in scan list! \n\ncmd passed to `{done}` bots and failed in `{fail}` bots!"
   await huh.delete()
   await message.reply(final_text, reply_markup=InlineKeyboardMarkup([
                                 [
                                 InlineKeyboardButton("• Revert •", callback_data=f"revert:{user.id}")
                                 ],
                                 ]
                                 )
                                 )
   scan_db.scan_user(user.id, reason_code)
   try:
      await passcmd_to_red(user, red7code, proof)
   except Exception as eor:
      print(f"[Team7 Error]: {str(eor)}")
      pass
   log_msg = "**#SCAN** \n\n"
   log_msg += f"Admin: {message.from_user.mention}\n"
   log_msg += f"User: {user.mention} (`{user.id}`) \n"
   log_msg += f"Reason: `{reason}` \n"
   log_msg += f"Proof: `{proof}` \n"
   await T7.send_message(seven_logs, log_msg)
   try:
      to_user_text = f"Hey {user.mention}! \n\n You're Scanned By [Team7](https://t.me/Team7_Support_chats) \n\n Reason: {reason} \n Proof: {proof}"
      if user.username:
         await assistant.send_message(user.username, to_user_text, disable_web_page_preview=True)
      else:
         await assistant.send_message(user.id, to_user_text, disable_web_page_preview=True)
   except:
      print(f"{user.first_name} is Noob!")
      pass
   repcheck = report_db.check_report(user.id)
   if repcheck:
      try:
          await assistant.send_message(repcheck.user_id, f"We scanned a user reported by you! \nUser {user.mention} \nReason {reason}")
      except Exception:
          pass
      report_db.rm_report(user.id)

async def scancallpass(T7, callback, user, reason_code, proof):
   reason, red7code = check_reason(reason_code)
   if user.username:
      bancmd = scan_cmd.format(user.username, reason, proof, user.first_name)
   else:
      bancmd = scan_cmd.format(user.id, reason, proof, user.first_name)

   await callback.answer("passing cmd....")
   done = 0
   fail = 0
   for bot in users_db.get_all_bots():
      try:
         await assistant.send_message(bot.username, bancmd)
         done += 1
      except:
         try:
            await assistant.send_message(bot.user_id, bancmd)
            done += 1
         except:
            fail += 1
   try:
       await callback.edit_message_text(f"User {user.mention} is now in Scanlist! \n\n cmd passed to `{done}` bots and failed in `{fail}` bots!")
   except Exception:
       await callback.delete()
   scan_db.scan_user(user.id, reason_code)
   try:
      await passcmd_to_red(user, red7code, proof)
   except Exception as eor:
      print(f"[Team7 Error]: {str(eor)}")
      pass
   log_msg = "**#SCAN** \n\n"
   log_msg += f"Admin: {callback.from_user.mention}\n"
   log_msg += f"User: {user.mention} (`{user.id}`) \n"
   log_msg += f"Reason: `{reason}` \n"
   log_msg += f"Proof: `{proof}` \n"
   await T7.send_message(seven_logs, log_msg)
   repcheck = report_db.check_report(user.id)
   if repcheck:
      try:
          await assistant.send_message(repcheck.user_id, f"We scanned a user reported by you! \nUser {user.mention} \nReason {reason}")
      except Exception:
          pass
      report_db.rm_report(user.id)

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("Cancelled the Process!", quote=True)
        return True
    elif "/restart" in msg.text:
        await msg.reply("Restarted!", quote=True)
        return True
    elif msg.text.startswith("/"):
        await msg.reply("Cancelled the process!", quote=True)
        return True
    else:
        return False

async def scan_user_query(T7: Team7Scanner, message: Message):
   chat = message.chat
   ask_user = await T7.ask(chat.id, "Gime username or user id of user!", filters=filters.text, timeout=300)
   if await cancelled(ask_user):
      return
   try:
      scan_user = await T7.get_users(ask_user.text)
      if await user_in_res(ask_user, scan_user.id):
         return
      if scan_db.check_scan(scan_user.id):
         await message.reply("user already scanned by Team7")
         return
   except Exception as eror:
      if '[400 PEER_ID_INVALID]' in str(eror):
         await ask_user.repky("Forward any message of user and type /id replying that message! \nThen try again ✓")
         return
      error = user_errors(str(eror))
      await message.reply(str(error))
      return 
   ask_reason = await T7.ask(chat.id, "Now Gime Reason code! Type /bancodes to get all reason codes!", filters.text, timeout=300)
   if await cancelled(ask_reason):
      return
   check_code, _ = check_reason(ask_reason.text)
   if check_code == "Null":
      await ask_reason.reply(f"Eh! `{ask_reason.text}` is wrong bancode! Type /bancodes to get all bancodes!")
      return
   reason_code = ask_reason.text
   ask_proof = await T7.ask(chat.id, "Now Gime proof (single telegraph link) or photo", timeout=300)
   if ask_proof.photo:
      proof = await make_tg(ask_proof)
   elif ask_proof.text:
      if await cancelled(ask_proof):
         return
      pr = ask_proof.text
      if pr.startswith("https://telegra.ph/file") or pr.startswith("https://telegra.ph") or pr.startswith("https://graph.org") or pr.startswith("https://graph.org/file"):
         proof = str(pr)
      else:
         await ask_proof.reply("need telegraph link as a proof!")
         return
   else:
       await ask_proof.reply("send Telegraph link or photo!")
       return
   await scanpass(T7, message, scan_user, reason_code, proof)

@Team7Scanner.on_callback_query(filters.regex(r'revert'))
async def scan_callback(T7: Team7Scanner, callback: CallbackQuery):
    query = callback.data.split(":")
    admin = callback.from_user
    message = callback.message
    if users_db.check_owner(admin.id) or users_db.check_dev(admin.id):
       user = await T7.get_users(query[1])
       await revertcallpass(T7, callback, user)
    else:
       await callback.answer("Only Team7Scanne's Owner and Devs can!", show_alert=True)
