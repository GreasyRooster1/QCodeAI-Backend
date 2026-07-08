from fastapi import APIRouter, HTTPException
from app.models.prompt_models import PromptBuildRequest
from app.services.prompt_services import get_all_templates, build_prompt

router = APIRouter()

@router.get("/templates")
async def list_templates():
    return {"templates": get_all_templates()}

@router.post("/build")
async def create_prompt(request: PromptBuildRequest):
    try:
        ready_prompts = build_prompt(request.template_id, request.inputs)
        return {
            "success": True,
            "system_prompt": ready_prompts["system_prompt"],
            "prompt": ready_prompts["template"]
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))