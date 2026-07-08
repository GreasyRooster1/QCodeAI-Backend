from fastapi import APIRouter
from app.models.nn_models import ForwardPassRequest
from app.services.nn_service import calculate_forward_pass

router = APIRouter()

@router.post("/forward")
async def process_forward_pass(request: ForwardPassRequest):
    layers_data = [layer.model_dump() for layer in request.layers]
    result = calculate_forward_pass(request.inputs, layers_data)
    return {
        "success": True,
        "history": result
    }