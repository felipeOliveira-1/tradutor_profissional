from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from database import engine, Base
from routers import document_router, translation_router

# Criar as tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Carregar variáveis de ambiente
load_dotenv()

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar routers
app.include_router(document_router.router, prefix="/api/documents", tags=["documents"])
app.include_router(translation_router.router, prefix="/api/translations", tags=["translations"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Tradutor Profissional"}
