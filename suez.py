import os
import sys
import time
import random

import dotenv
import requests

dotenv.load_dotenv()

INTERVAL = int(os.getenv("INTERVAL")) or 60

GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DISCORD_AVATAR_URL = os.getenv("AVATAR_URL")

def find_gif(is_stuck: bool) -> str:
    """
    Finds a suitable GIF using the GIPHY API depending upon
    if the Ever Given is still stuck or not.

    @params
    is_stuck: bool
        If it is stuck or not.

    @returns
    str
        A string pointing to the GIF chosen.
    """
    q = "stuck" if is_stuck else "im free"

    try:
        r = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={q}&limit=50")
        if r.status_code == 200:
            return random.choice(r.json()['data'])['url']
        else:
            return None
    except Exception:
        return None

def send_discord_message(message: str):
    """
    Sends a message to a Discord Webhook.

    @params
    message: str
        The message to send.
    """
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, data={
            'username':'Ever Given',
            'avatar_url': DISCORD_AVATAR_URL,
            'content': message,
            'username': "Ever Given"
        })
    except Exception:
        pass

def is_stillstuck() -> bool:
    """
    Works out if the Ever Given is still stuck in the Suez.

    @returns
    bool
        If the Ever Given is still stuck or not.
    """
    try:
        r = requests.get("https://isitstillstuck.com/json/")
        if r.status_code == 200:
            return r.json()['stillstuck']
        else:
            return True
    except Exception:
        return True

stillstuck = True
while stillstuck:
    # Get if it is still stuck or not and then set the
    # message and GIF accordingly
    stillstuck = is_stillstuck()
    g = find_gif(stillstuck)
    if stillstuck:
        m = "The Ever Given is still stuck in the Suez🚢"
    else:
        m = "The Ever Given is freeeeeeeee! 🆓"

    send_discord_message(m)
    send_discord_message(g)

    # If it isn't stuck, then send a goodbye message as our job
    # is done and then exit...
    if not stillstuck:
        send_discord_message("The Ever Given has gone, and so will I...")
        send_discord_message("https://media.giphy.com/media/LTFbyWuELIlqlXGLeZ/giphy.gif")
        break

    # Check every so often (default 1 hour)
    time.sleep(60 * INTERVAL)