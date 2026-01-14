from instagrapi import Client
import time
import random
import os
from keep_alive import keep_alive

# ----------------------------
# KEEP BOT ALIVE (Render ping)
# ----------------------------
keep_alive()

# ----------------------------
# ENV VARS
# ----------------------------
SESSION_ID = os.getenv("IG_SESSION_ID")
if not SESSION_ID:
    raise Exception("❌ IG_SESSION_ID not found in environment variables")

# ----------------------------
# LOGIN
# ----------------------------
cl = Client()
cl.login_by_sessionid(SESSION_ID)

me_id = cl.user_id
my_username = cl.username
print(f"🤖 Logged in as @{my_username} (ID: {me_id})")

# ----------------------------
# REPLY TEMPLATES
# ----------------------------
reply_templates_master = [
    """ARJUN TMKC_________________//🩷
    
ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷

ARJUN TMKC_________________//🩷""",
    """OYE MSG MT KR VRNA ARJUN KI MAA CUD JAYEGI"""
]

# Track last message ID per user
last_msg_id_by_user = {}
user_reply_history = {}

# ----------------------------
# AUTO-REPLY FUNCTIONS
# ----------------------------
def get_next_reply(username, history):
    possible_replies = [r for r in reply_templates_master if r not in history]
    if not possible_replies:
        history.clear()
        possible_replies = reply_templates_master.copy()
    reply = random.choice(possible_replies)
    history.add(reply)
    return reply.replace("{user}", username)

# ----------------------------
# AUTO GC NAME RESET
# ----------------------------
LOCKED_GC_NAME = "🔥 ARJUN KI MA CUDI AXLE SE 🔥"

def enforce_gc_name(thread):
    try:
        current_title = thread.title
        if current_title != LOCKED_GC_NAME:
            cl.direct_thread_edit_title(thread.id, LOCKED_GC_NAME)
            print(f"🔁 GC name reset: {current_title} → {LOCKED_GC_NAME}")
            return True
    except Exception as e:
        print(f"⚠️ GC rename failed: {e}")
    return False

# ----------------------------
# MAIN AUTO-REPLY LOOP
# ----------------------------
def auto_reply():
    while True:
        try:
            threads = cl.direct_threads(amount=10)  # last 10 threads

            for thread in threads:
                # ----------------------------
                # GC name enforcement
                # ----------------------------
                if thread.is_group:
                    renamed = enforce_gc_name(thread)
                    if renamed:
                        time.sleep(60)  # 1 rename per minute max
                        continue  # skip this loop to avoid spamming

                # ----------------------------
                # Skip empty threads
                # ----------------------------
                if not thread.messages:
                    continue

                latest_msg = thread.messages[0]

                # Ignore own messages
                if latest_msg.user_id == me_id:
                    continue

                user_id = latest_msg.user_id
                username = cl.user_info(user_id).username

                # Skip if already replied
                if last_msg_id_by_user.get(user_id) == latest_msg.id:
                    continue

                # Init user history
                if user_id not in user_reply_history:
                    user_reply_history[user_id] = set()

                # Generate reply
                reply = get_next_reply(username, user_reply_history[user_id])

                try:
                    cl.direct_answer(thread.id, reply)
                    print(f"✔️ Replied to @{username}: {reply}")
                    last_msg_id_by_user[user_id] = latest_msg.id
                    time.sleep(random.randint(15, 25))  # human-like delay
                except Exception as e:
                    print(f"⚠️ Failed to reply in thread {thread.id}: {e}")

            # Main loop delay
            time.sleep(random.randint(15, 25))

        except Exception as err:
            print(f"🚨 Main loop error: {err}")
            time.sleep(random.randint(25, 30))

# ----------------------------
# START BOT
# ----------------------------
auto_reply()
