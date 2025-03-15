 
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Investimento as InvestimentoDB
from database import SessionLocal, engine
from schemas import InvestimentoCreate, Investimento, InvestimentoUpdate

# Criando a tabela no banco de dados se não existir
InvestimentoDB.metadata.create_all(bind=engine)

app = FastAPI()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um novo investimento
@app.post("/investimentos/", response_model=Investimento)
def criar_investimento(investimento: InvestimentoCreate, db: Session = Depends(get_db)):
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
@app.get("/investimentos/", response_model=list[Investimento])
def listar_investimentos(db: Session = Depends(get_db)):
    investimentos = db.query(InvestimentoDB).all()
    return investimentos

@app.put("/investimentos/{investimento_id}", response_model=Investimento)
def atualizar_investimento(investimento_id: int, investimento: InvestimentoUpdate, db: Session = Depends(get_db)):
    db_investimento = db.query(InvestimentoDB).filter(InvestimentoDB.id == investimento_id).first()
    if db_investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    
    # Atualiza os dados do investimento com os dados da requisição
    db_investimento.nome = investimento.nome
    db_investimento.tipo = investimento.tipo
    db_investimento.valor = investimento.valor
    db_investimento.data_investimento = investimento.data_investimento
    
    # Commit e refresh
    db.commit()
    db.refresh(db_investimento)
    
    # Retorna o investimento atualizado
    return db_investimento


# Rota para deletar um investimento
@app.delete("/investimentos/{investimento_id}")
def excluir_investimento(investimento_id: int, db: Session = Depends(get_db)):
    db_investimento = db.query(InvestimentoDB).filter(InvestimentoDB.id == investimento_id).first()
    if db_investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    db.delete(db_investimento)
    db.commit()
    return {"message": "Investimento excluído com sucesso"}
