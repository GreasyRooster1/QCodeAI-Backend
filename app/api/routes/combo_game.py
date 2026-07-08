import json
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai.provider_factory import ProviderFactory

router = APIRouter()

BASIC_RECIPES = {
    ("fire", "water"): 
        {"element": "Steam", "emoji": "💨", "reasoning": "Fire heats up water until it boils and evaporates into steam."},
    ("air", "water"): 
        {"element": "Rain", "emoji": "🌧️", "reasoning": "Water vapor condenses in the air and falls back down as rain."},
    ("earth", "water"): 
        {"element": "Mud", "emoji": "🤎", "reasoning": "Mixing dry earth with water creates thick, wet mud."},
    ("air", "fire"): 
        {"element": "Energy", "emoji": "⚡", "reasoning": "The rapid heating and expansion of air creates energetic storms and lightning."},
    ("earth", "fire"): 
        {"element": "Lava", "emoji": "🌋", "reasoning": "Intense fire melts the solid earth and rock into molten lava."},
    ("air", "earth"): 
        {"element": "Daisy", "emoji": "🌼", "reasoning": "Seeds carried by the wind plant themselves in the earth to grow flowers."},
    ("earth", "earth"): 
        {"element": "Mountain", "emoji": "🏔️", "reasoning": "Piling earth on top of more earth builds a towering mountain."},
    ("fire", "fire"): 
        {"element": "Volcano", "emoji": "🌋", "reasoning": "Combining massive amounts of fire creates an explosive volcanic eruption."},
    ("water", "water"): 
        {"element": "Lake", "emoji": "🌊", "reasoning": "Accumulating water together forms a large, deep lake."},
    ("air", "air"): 
        {"element": "Tornado", "emoji": "🌪️", "reasoning": "Swirling air currents combine to form a massive, destructive tornado."}
}

class CombinationRequest(BaseModel):
    element1: str
    element2: str
    provider: str = "ollama"

@router.post("/combine")
async def combine_elements(request: CombinationRequest):
    combo_key = tuple(sorted([request.element1.lower(), request.element2.lower()]))
    if combo_key in BASIC_RECIPES:
        recipe = BASIC_RECIPES[combo_key]
        return {
            "success": True,
            "recipe": [request.element1, request.element2],
            "result": recipe,
            "source": "dictionary"
        }

    system_prompt = """
    You are a logic engine for an infinite crafting game. The user will give you
    two elements. You must combine them into a single, logical evolution of the elements and provide a
    fitting emoji. The evolutions should always be a FUN AND CONSEQUENTIAL combination of the two elements
    (e.g. Sand + Fire = Glass, Earth + Rain = Rainbow). Inventing elements is not allowed, instead get creative.
    AVOID ALL REFERENCES TO ADULT THEMES AND TOPICS, ESPECIALLY DRUGS AND ALCOHOL.
    Respond ONLY in valid JSON format. Do not include markdown formatting or explanations.
    Format: {"reasoning": "Brief 1-sentence step-by-step logic of how A and B become C", "element": "New Element", "emoji": "🔥"}
    """
    # system_prompt = """
    # You are a logic engine for an infinite crafting game. The user will give you
    # two elements. You must combine them into a single, logical evolution of the elements and provide a
    # fitting emoji. The evolutions should follow logic (e.g. Fire + Daisy should be destructive, Daisy + Wind should be constructive)
    # and should always be a FUN AND CONSEQUENTIAL combination of the two elements (e.g. Sand + Fire = Glass, Earth + Rain = Rainbow).
    # Elements are allowed to get abstract if absolutely necessary.
    # AVOID ALL REFERENCES TO ADULT THEMES AND TOPICS, ESPECIALLY DRUGS AND ALCOHOL.
    # Respond ONLY in valid JSON format. Do not include markdown formatting or explanations.
    # Format: {"element": "New Element", "emoji": "🔥"}
    # """
    
    user_prompt = f"""
    User elements: {request.element1} + {request.element2}
    
    CRITICAL REMINDERS:
        1. Respond ONLY in valid JSON format. Do not include markdown formatting or explanations.
        2. Remember to put the "" around each item, especially the emoji!
        3. FUN AND CONSISTENCY IS VALUED OVER ALL!
    """
    
    # Cache combos here
        # Firebase storage for all combinations kids create to prevent token waste
    
    provider = ProviderFactory.create(request.provider)
    
    result = await provider.generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.5,
        max_tokens=150
    )
    
    try:
        # Hopefully larger models from openai will handle json output more consistently
            # UPDATE: Sandwich prompting seems to have helped a great deal!
        print(result.output)
        clean = re.sub(r"```json|```", "", result.output).strip()
        print(clean)
        data = json.loads(clean)
        
        return {
            "success": True,
            "recipe": [request.element1, request.element2],
            "result": {
                "element": data.get("element"),
                "emoji": data.get("emoji"),
                "reasoning": data.get("reasoning", "The AI combined these mysteriously...")
            }
        }
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse response. {result.output}"
        )
    