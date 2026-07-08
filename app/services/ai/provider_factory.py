from app.core.config import settings
from app.services.ai.openai_provider import OpenAIProvider
from app.services.ai.ollama_provider import OllamaProvider
from app.services.ai.dummy_provider import DummyProvider
from app.services.ai.groq_provider import GroqProvider

class ProviderFactory:
    @staticmethod
    def create(provider_name: str):
        if provider_name == "openai":
            return OpenAIProvider(...)
        elif provider_name == "ollama":
            return OllamaProvider(settings.DEFAULT_MODEL)
        elif provider_name == "dummy":
            return DummyProvider()
        elif provider_name == "groq":
            return GroqProvider(api_key=settings.GROQ_API_KEY)
        return ValueError("Invalid provider")