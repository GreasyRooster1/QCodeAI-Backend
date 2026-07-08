from pydantic import BaseModel
from typing import List

class LayerData(BaseModel):
    weights: List[List[float]]
    biases: List[float]

class ForwardPassRequest(BaseModel):
    inputs: List[float]
    layers: List[LayerData]