import time
import uuid
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import StreamingResponse
from app.models.ai_request import AIRequest
from app.services.ai.provider_factory import ProviderFactory
from app.services.interacion_logger import InteractionLogger

router = APIRouter()
logger = InteractionLogger()

@router.post("/generate")
async def generate(request: AIRequest):
    provider = ProviderFactory.create(request.provider)
    
    result = await provider.generate(
        system_prompt=request.system_prompt,
        user_prompt=request.user_prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    
    await logger.log(
        user_id="crashtestdummy",
        prompt=request.user_prompt,
        response=result.output,
        metadata={
            "provider": result.provider,
            "model": result.model,
            "latency": result.latency_ms,
            "token_count": result.token_count,
        }
    )
    
    return result

@router.post("/stream")
async def stream_generate(request: AIRequest):
    provider = ProviderFactory.create(request.provider)
    print(provider)
    word_limit = max(1, int((request.max_tokens * 0.75) - 10))
    length_prompt = f"\nCRITICAL OVERRIDE: You are strictly limited to a maximum of {word_limit} words. You must organically conclude your response before reaching this limit."
    modified_prompt = request.system_prompt + length_prompt
    
    async def token_stream():
        start = time.time()
        total_response = ""
        chunks = []
        try:
            print(request.temperature)
            async for token in provider.stream_generate(
                system_prompt=modified_prompt,
                user_prompt=request.user_prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ):
                # total_response += token
                chunks.append(token)
                yield token
            
            latency = (time.time() - start) * 1000
            token_count = len("".join(chunks).split())
            session_id = str(uuid.uuid4())
            
            await logger.log(
                user_id="crashtestdummy",
                prompt=request.user_prompt,
                response=total_response,
                metadata={
                    "session_id": session_id,
                    "provider": request.provider,
                    "model": provider.model,
                    "latency": latency,
                    "token_count": token_count,
                    "streaming": True,
                    "status": "success",
                }
            )
        except Exception as e:
            latency = (time.time() - start) * 1000
            await logger.log(
                user_id="crashtestdummy",
                prompt=request.user_prompt,
                response=total_response,
                metadata={
                    "provider": request.provider,
                    "model": provider.model,
                    "latency": latency,
                    "streaming": True,
                    "status": "error",
                    "error": str(e)
                }
            )
            raise e
    
    
    return StreamingResponse(
        token_stream(),
        media_type="text/plain",
    )