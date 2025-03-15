from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definindo a Base
Base = declarative_base()

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Você pode alterar o banco para o que for necessário
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Criando a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

