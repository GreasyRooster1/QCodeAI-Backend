from app.core.config import settings
from app.services.ai.openai_provider import OpenAIProvider
from app.services.ai.ollama_provider import OllamaProvider
from app.services.ai.dummy_provider import DummyProvider
from app.services.ai.groq_provider import GroqProvider
from app.services.ai.openrouter_provider import OpenRouterProvider


class ProviderFactory:
    @staticmethod
    def create(provider_name: str):
        if provider_name == "openrouter":
            return OpenRouterProvider(api_key=settings.OPENROUTER_API_KEY)
        elif provider_name == "groq":
            return GroqProvider(api_key=settings.GROQ_API_KEY)
        # elif provider_name == "ollama":
        #     return OllamaProvider(settings.DEFAULT_MODEL)
        # elif provider_name == "dummy":
        #     return DummyProvider()
        return ValueError("Invalid provider")