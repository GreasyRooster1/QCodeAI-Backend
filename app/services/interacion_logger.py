from datetime import datetime, timezone
from firebase_admin import db as firebase_db

# class InteractionLogger:
#     async def log(self, user_id: str, prompt: str, response: str, metadata: dict):
#         log_record = {
#             "user_id": user_id,
#             "prompt": prompt,
#             "response": response,
#             "metadata": metadata,
#             "timestamp": datetime.now(timezone.utc).isoformat(),
#         }
        
#         get_db_ref("logs").push(log_record)
        
#         tokens_spent = metadata.get("token_count", 0)
#         if tokens_spent > 0:
#             user_token_counter = get_db_ref(f"users/{user_id}/tokens_used")
#             user_token_counter.set(firebase_db.ServerValue.increment(tokens_spent))

class InteractionLogger:
    def log(self, user_id: str, prompt: str, response: str, metadata: dict):
        print(f"[AUTH OK] User: {user_id} | Tokens: {metadata.get('token_count')}")