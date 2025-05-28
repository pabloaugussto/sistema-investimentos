from pydantic import BaseModel
from datetime import date

# Modelo base para investimento
class InvestimentoBase(BaseModel):
    nome: str
    tipo: str
    valor: float
    data_investimento: date

# Modelo Pydantic para criação de investimento (sem o ID)
class InvestimentoCreate(InvestimentoBase):
    pass

# Modelo Pydantic para leitura de investimento (inclui o ID)
class Investimento(InvestimentoBase):
    id: int

    class Config:
        from_attributes = True  # Substitui orm_mode para from_attributes

# Modelo Pydantic para atualização de investimento (sem o ID, pois será passado como parâmetro na URL)
class InvestimentoUpdate(InvestimentoBase):
    pass


