from datetime import datetime, timezone

class InteractionLogger:
    async def log(self, user_id: str, prompt: str, response: str, metadata: dict):
        log_record = {
            "user_id": user_id,
            "prompt": prompt,
            "response": response,
            "metadata": metadata,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        
        print(log_record)