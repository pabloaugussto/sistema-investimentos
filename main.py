from fastapi import FastAPI
from database import engine, Base
from routes import router as investimentos_router # Importa o router do arquivo routes.py
from fastapi.middleware.cors import CORSMiddleware # <<< linha de importação add

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Sistema de Investimentos API",
    description="API para gerenciar cadastros de investimentos.",
    version="0.1.0"
)

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500", # Para o Live Server
    "null" # Para abrir o HTML localmente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas definidas em routes.py
app.include_router(investimentos_router, prefix="/api/v1") # Adicionando um prefixo opcional

print("Aplicação FastAPI iniciada com CORS habilitado. Acesse a documentação em /api/v1/docs ou /redoc.") # Mensagem atualizada