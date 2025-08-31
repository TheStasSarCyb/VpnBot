from bot import bot

LAST_MESSAGES_FOR_DELETING = {}

def add(user_id: str, msg_id:int):
    if user_id not in LAST_MESSAGES_FOR_DELETING: 
        LAST_MESSAGES_FOR_DELETING[user_id] = []
    LAST_MESSAGES_FOR_DELETING[user_id].append(msg_id)

async def clear(user_id: str, client=bot):
    if user_id not in LAST_MESSAGES_FOR_DELETING: 
        LAST_MESSAGES_FOR_DELETING[user_id] = []
        return
    for msg in LAST_MESSAGES_FOR_DELETING[user_id]:
        await client.delete_message(chat_id=int(user_id), message_id=msg)
    LAST_MESSAGES_FOR_DELETING[user_id].clear()
