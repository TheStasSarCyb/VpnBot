# LAST_MESSAGES_FOR_DELETING = {}

# def add(user_id: str, msg_id:int):
#     if user_id not in LAST_MESSAGES_FOR_DELETING: 
#         LAST_MESSAGES_FOR_DELETING[user_id] = []
#     LAST_MESSAGES_FOR_DELETING[user_id].append(msg_id)

# async def clear(user_id: str, client=bot_client):
#     if user_id not in LAST_MESSAGES_FOR_DELETING: 
#         LAST_MESSAGES_FOR_DELETING[user_id] = []
#         return
#     await client.delete_messages(int(user_id), message_ids=LAST_MESSAGES_FOR_DELETING[user_id])
#     LAST_MESSAGES_FOR_DELETING[user_id].clear()
