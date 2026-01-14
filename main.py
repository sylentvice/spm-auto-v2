from instagrapi import Client
import time
import random
import os
from keep_alive import keep_alive

keep_alive()

SESSION_ID = os.getenv("IG_SESSION_ID")

if not SESSION_ID:
    raise Exception("❌ IG_SESSION_ID not found in environment variables")

cl = Client()
cl.login_by_sessionid(SESSION_ID)

me_id = cl.user_id
my_username = cl.username
print(f"🤖 Logged in as @{my_username} (ID: {me_id})")

reply_templates_master = [
    "BOLA NA MSG MT KR VRNA ARJUN KI MAA TERE SE V CUD JAYEGI",
    "OYE MSG MT KR VRNA ARJUN KI MAA CUD JAYEGI"
]

last_msg_id_by_user = {}

def get_next_reply(history):
    possible = [r for r in reply_templates_master if r not in history]
    if not possible:
        history.clear()
        possible = reply_templates_master.copy()
    reply = random.choice(possible)
    history.add(reply)
    return reply

user_reply_history = {}

def auto_reply():
    while True:
        try:
            threads = cl.direct_threads(amount=1)

            for thread in threads:
                if not thread.messages:
                    continue

                latest_msg = thread.messages[0]

                if latest_msg.user_id == me_id:
                    continue

                user_id = latest_msg.user_id
                username = cl.user_info(user_id).username

                if last_msg_id_by_user.get(user_id) == latest_msg.id:
                    continue

                if user_id not in user_reply_history:
                    user_reply_history[user_id] = set()

                reply = get_next_reply(user_reply_history[user_id])

                # 👇 USERNAME MENTION ADDED
                final_reply = f"@{username} {reply}"

                try:
                    cl.direct_answer(thread.id, final_reply)
                    print(f"✔️ Replied to @{username}: {final_reply}")
                    last_msg_id_by_user[user_id] = latest_msg.id
                    time.sleep(random.randint(2, 6))
                except Exception as e:
                    print(f"⚠️ Failed to reply in thread {thread.id}: {e}")

            time.sleep(random.randint(2, 6))

        except Exception as err:
            print(f"🚨 Main loop error: {err}")
            time.sleep(random.randint(25, 30))

auto_reply()
