import os, sys
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")

def make_list(str_input):
    str_list = str_input.split(" ")
    int_list = []
    for x in str_list:
        int_list.append(int(x))
    return int_list

" ===================== CONFIGS ===================== "

API_ID = int(os.getenv("API_ID", ""))
if not API_ID:
   print("[Team7 INFO]: You didn't fill API_ID var!")
   sys.exit()
else:
   print("[Team7 INFO]: Got API_ID")

API_HASH = os.getenv("API_HASH", "")
if not API_HASH:
   print("[Team7 INFO]: You didn't fill API_HASH var!")
   sys.exit()
else:
   print("[Team7 INFO]: Got API_HASH")

TOKEN = os.getenv("TOKEN", "")
if not TOKEN:
   print("[Team7 INFO]: You didn't fill TOKEN var!")
   sys.exit()
else:
   print("[Team7 INFO]: Got TOKEN")

SESSION = os.getenv("SESSION", "")
if not SESSION:
   print("[Team7 INFO]: You didn't fill SESSION var!")
   sys.exit()
else:
   print("[Team7 INFO]: Got SESSION")

OWNER_IDS = make_list(os.getenv("OWNER_IDS", ""))
if not OWNER_IDS:
   print("[Team7 INFO]: You didn't fill OWNER_IDS var!")
   sys.exit()
else:
   print("[Team7 INFO]: Got OWNER_IDS")

DEVS = make_list(os.getenv("DEVS", ""))
if not DEVS:
   print("[Team7 INFO]: You didn't fill DEVS var!")
   sys.exit()
else:
   print("[Team7 INFO]: Got DEVS")

SCAN_LOGS = os.getenv("SCAN_LOGS", "")
if not SCAN_LOGS:
   print("[Team7 INFO]: You didn't fill SCAN_LOGS var!")
   sys.exit()
else:
   print("[Team7 INFO]: Got SCAN_LOGS")

SEVEN_LOGS = os.getenv("SEVEN_LOGS", "")
if not SEVEN_LOGS:
   print("[Team7 INFO]: You didn't fill SEVEN_LOGS var!")
   sys.exit()
else:
   print("[Team7 INFO]: Got SEVEN_LOGS")

DB_URL = os.getenv("DATABASE_URL", "")
if DB_URL:
   print("[Team7 INFO]: Got DATABASE_URL")
   if 'postgres' in DB_URL and 'postgresql' not in DB_URL:
      DB_URL = DB_URL.replace("postgres", "postgresql")
else:
   print("[Team7 INFO]: You didn't fill DATABASE_URL")
   sys.exit()

Channel = "botupdatex"
Support = "botsupportx"
