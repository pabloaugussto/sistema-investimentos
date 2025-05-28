 
from fastapi import FastAPI
from database import engine, Base
from routes import router as investimentos_router # Importa o router do arquivo routes.py

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Sistema de Investimentos API",
    description="API para gerenciar cadastros de investimentos.",
    version="0.1.0"
)

# Inclui as rotas definidas em routes.py
app.include_router(investimentos_router, prefix="/api/v1") # Adicionando um prefixo opcional

print("Aplicação FastAPI iniciada. Acesse a documentação em /docs ou /redoc.")