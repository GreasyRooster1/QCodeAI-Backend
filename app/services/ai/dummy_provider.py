from app.models.ai_result import AIResult
from app.services.ai.base_provider import BaseAIProvider

class DummyProvider(BaseAIProvider):
    async def generate(self, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int):
        return AIResult(
            output="test",
            provider="dummy",
            model="dummy",
            latency_ms=0.0,
            token_count=1
        )
    
    async def stream_generate(self, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int):
        return AIResult(
            output="test",
            provider="dummy",
            model="dummy",
            latency_ms=0.0,
            token_count=1
        )