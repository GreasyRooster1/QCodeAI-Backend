from openai import AsyncOpenAI
from app.services.ai.base_provider import BaseAIProvider

class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate(self, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int):
        response = await self.client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
    
        return response.choices[0].message.content