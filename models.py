from sqlalchemy import Column, Integer, String, Float, Date
from database import Base  # Importando a Base corretamente

class Investimento(Base):
    __tablename__ = "investimentos"  # Nome da tabela no banco de dados
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    tipo = Column(String)
    valor = Column(Float)
    data_investimento = Column(Date)

    