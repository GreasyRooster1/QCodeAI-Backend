from pydantic import BaseModel, Field

class AIRequest(BaseModel):
    provider: str
    system_prompt: str
    user_prompt: str
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.95, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=-0.3, ge=-2.0, le=2.0)
    max_tokens: int = Field(default=150, gt=0, le=500)