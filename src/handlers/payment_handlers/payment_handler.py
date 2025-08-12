from bot import user_client
from telethon import events, types

@user_client.on(events.NewMessage)
async def new_donors_messages(event: types.Message):
    pass