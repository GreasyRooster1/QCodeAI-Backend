import os
import time

from openrouter import OpenRouter
from openai import AsyncOpenAI
from app.services.ai.base_provider import BaseAIProvider
from app.models.ai_result import AIResult

class OpenRouterProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = model
        self.provider_name = "openrouter"
    
    async def generate(self, system_prompt: str, user_prompt: str, temperature: float, top_p:float, frequency_penalty:float, max_tokens: int) -> AIResult:
        start = time.time()
        with OpenRouter(
                api_key=os.getenv("OPENROUTER_API_KEY", ""),
        ) as open_router:
            res = open_router.chat.send(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=False,
                model=self.model,
                max_completion_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                reasoning_effort="none",
            )
        print(res)
        output = res.choices[0].message.content
        latency = (time.time() - start) * 1000
        token_count: int = 0
        if not output is None:
            token_count = len(output.split())
        
        return AIResult(
            output=output,
            provider=self.provider_name,
            model=self.model,
            latency_ms=latency,
            token_count=token_count
        )
    
    async def stream_generate(self, system_prompt: str, user_prompt: str, temperature: float, top_p:float, frequency_penalty:float, max_tokens: int):
        stream = await self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content