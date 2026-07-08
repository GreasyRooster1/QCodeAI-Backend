from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import ai, combo_game, prompts, nn, pet_trainer

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://ai.esporterz.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["*"],
)

app.include_router(ai.router, prefix="/api/ai", tags=["Generation"])
app.include_router(combo_game.router, prefix="/api/combo_game", tags=['Combo Game'])
app.include_router(prompts.router, prefix="/api/prompts", tags=["Prompt Builder"])
app.include_router(nn.router, prefix="/api/nn", tags=["Neural Network Sim"])
app.include_router(pet_trainer.router, prefix="/api/pet_trainer", tags=["Pet Trainer - Reinforcement Learning"])

@app.get("/")
async def root():
    return {"status": "running"}
