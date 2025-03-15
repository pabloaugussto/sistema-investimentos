from fastapi import APIRouter
from .schemas import Investimento

router = APIRouter()

# Rota para listar investimentos
@router.get("/investimentos")
async def get_investimentos():
    return {"message": "Aqui estarão os investimentos"}

