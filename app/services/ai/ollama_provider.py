import time
import ollama
from app.models.ai_result import AIResult
from app.services.ai.base_provider import BaseAIProvider

class OllamaProvider(BaseAIProvider):
    def __init__(self, model: str):
        self.model = model
        self.provider_name = "ollama"
    
    def generate(self, system_prompt: str, user_prompt: str, temperature: float, top_p:float, frequency_penalty:float, max_tokens: int) -> AIResult:
        start = time.time()
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )
        
        output = response["message"]["content"]
        
        latency = (time.time() - start) * 1000
        
        token_count = len(output.split())
        
        return AIResult(
            output=output,
            provider=self.provider_name,
            model=self.model,
            latency_ms=latency,
            token_count=token_count
        )
    
    def stream_generate(self, system_prompt: str, user_prompt: str, temperature: float, top_p:float, frequency_penalty:float, max_tokens: int):
        stream = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            options={
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            stream=True
        )
        
        for chunk in stream:
            content = chunk["message"]["content"]
            yield content