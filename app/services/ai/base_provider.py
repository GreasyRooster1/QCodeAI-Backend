from abc import ABC, abstractmethod
from app.models.ai_result import AIResult

class BaseAIProvider(ABC):
    
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        top_p:float,
        frequency_penalty:float,
        max_tokens: int
    ) -> AIResult:
        pass
    
    @abstractmethod
    def stream_generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        top_p: float,
        frequency_penalty: float,
        max_tokens: int
    ):
        pass