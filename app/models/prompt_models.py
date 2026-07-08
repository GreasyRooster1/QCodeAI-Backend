from pydantic import BaseModel
from typing import List, Dict

class PromptTemplate(BaseModel):
    id: str
    name: str
    description: str
    system_prompt: str
    template: str
    variables: List[str]

class PromptBuildRequest(BaseModel):
    template_id: str
    inputs: Dict[str, str]