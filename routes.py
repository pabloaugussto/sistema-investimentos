from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, get_db  # Import get_db
from .models import Investimento as InvestimentoDB
from .schemas import InvestimentoCreate, Investimento, InvestimentoUpdate

router = APIRouter()

# Rota para criar um novo investimento
@router.post("/investimentos/", response_model=Investimento, tags=["Investimentos"])
def criar_investimento(investimento: InvestimentoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo investimento no banco de dados.
    """
    db_investimento = InvestimentoDB(
        nome=investimento.nome,
        tipo=investimento.tipo,
        valor=investimento.valor,
        data_investimento=investimento.data_investimento
    )
    db.add(db_investimento)
    db.commit()
    db.refresh(db_investimento)
    return db_investimento

# Rota para listar todos os investimentos
@router.get("/investimentos/", response_model=list[Investimento], tags=["Investimentos"])
def listar_investimentos(db: Session = Depends(get_db)):
    """
    Lista todos os investimentos cadastrados.
    """
    investimentos = db.query(InvestimentoDB).all()
    return investimentos

# Rota para buscar um investimento específico
@router.get("/investimentos/{investimento_id}", response_model=Investimento, tags=["Investimentos"])
def buscar_investimento(investimento_id: int, db: Session = Depends(get_db)):
    """
    Busca um investimento pelo seu ID.
    """
    db_investimento = db.query(InvestimentoDB).filter(InvestimentoDB.id == investimento_id).first()
    if db_investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    return db_investimento

# Rota para atualizar um investimento
@router.put("/investimentos/{investimento_id}", response_model=Investimento, tags=["Investimentos"])
def atualizar_investimento(investimento_id: int, investimento: InvestimentoUpdate, db: Session = Depends(get_db)):
    """
    Atualiza um investimento existente pelo seu ID.
    """
    db_investimento = db.query(InvestimentoDB).filter(InvestimentoDB.id == investimento_id).first()
    if db_investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")

    # Atualiza os dados (considerando PUT - substituição completa)
    db_investimento.nome = investimento.nome
    db_investimento.tipo = investimento.tipo
    db_investimento.valor = investimento.valor
    db_investimento.data_investimento = investimento.data_investimento

    db.commit()
    db.refresh(db_investimento)
    return db_investimento

# Rota para deletar um investimento
@router.delete("/investimentos/{investimento_id}", tags=["Investimentos"])
def excluir_investimento(investimento_id: int, db: Session = Depends(get_db)):
    """
    Exclui um investimento pelo seu ID.
    """
    db_investimento = db.query(InvestimentoDB).filter(InvestimentoDB.id == investimento_id).first()
    if db_investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    db.delete(db_investimento)
    db.commit()
    return {"message": "Investimento excluído com sucesso"}

