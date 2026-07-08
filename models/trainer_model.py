from pydantic import BaseModel
from typing import List

class PetTrainerRequest(BaseModel):
    reward_speed: float
    reward_neatness: float
    generations: int = 100