from bot import user_client
from telethon import events, types
import os
from dotenv import load_dotenv
from database import payment_succes

load_dotenv()

@user_client.on(events.NewMessage)
async def new_donors_messages(event: types.Message):
    if str(event.chat_id) == os.getenv("PAYMENT_CHAT_ID"):
        payment_id = event.text.split()[2]
        await payment_succes(payment_id)