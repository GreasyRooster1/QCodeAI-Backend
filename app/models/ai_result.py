from pydantic import BaseModel

class AIResult(BaseModel):
    output: str
    provider: str
    model: str
    latency_ms: float
    token_count: int