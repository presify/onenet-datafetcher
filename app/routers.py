from fastapi import APIRouter,Depends
from app.dependencies.load import load
from app.dependencies.generation import generation
from app.dependencies.transmission import transmission
from app.dependencies.balancing import balancing
router = APIRouter()

@router.get("/api/presify-onenet/load")
async def load(data: dict = Depends(load)):
    return data
@router.get("/api/presify-onenet/generation")
async def generation(data: dict = Depends(generation)):
    return data
@router.get("/api/presify-onenet/transmission")
async def transmission(data: dict = Depends(transmission)):
    return data
@router.get("/api/presify-onenet/balancing")
async def balancing(data: dict = Depends(balancing)):
    return data


