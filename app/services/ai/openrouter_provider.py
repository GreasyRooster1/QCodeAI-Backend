import os
import time

from openrouter import OpenRouter
from openai import AsyncOpenAI
from pygments.styles.dracula import yellow

from app.services.ai.base_provider import BaseAIProvider
from app.models.ai_result import AIResult

class OpenRouterProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str, reasoning_effort: str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = model
        self.provider_name = "openrouter"
        self.reasoning_effort = reasoning_effort
    
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
                reasoning_effort=self.reasoning_effort,
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
        with OpenRouter(
                api_key=os.getenv("OPENROUTER_API_KEY", ""),
        ) as open_router:
            res = await open_router.chat.send_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=True,
                model=self.model,
                max_completion_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                reasoning_effort=self.reasoning_effort,
            )

        async with res as event_stream:
            async for chunk in event_stream:
                if not chunk.choices:  # usage-only / keepalive chunks
                    continue
                reasoning = chunk.choices[0].delta.reasoning
                content = chunk.choices[0].delta.content

                if content:
                    yield {"type":"content","content":content}

                if reasoning:
                    yield {"type":"reasoning","content":reasoning}