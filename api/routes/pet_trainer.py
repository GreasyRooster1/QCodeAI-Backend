from fastapi import APIRouter
from app.models.trainer_model import PetTrainerRequest
from app.services.trainer_service import pet_evo

router = APIRouter()

@router.post("/simulate")
async def process_evo(request: PetTrainerRequest):
    result = pet_evo(
        reward_speed=request.reward_speed,
        reward_neatness=request.reward_neatness,
        generations=request.generations
    )
    
    return {
        "success": True,
        "history": result["history"]
    }