from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar OpenAI API
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para requisição de tradução
class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "pt"

@app.post("/api/translate")
async def translate_text(request: TranslationRequest):
    try:
        # Criar o prompt para o modelo
        prompt = f"""Traduza o seguinte texto de {request.source_lang} para {request.target_lang}. 
        Mantenha o estilo e o tom do texto original:
        
        {request.text}"""
        
        # Fazer a requisição para a API da OpenAI
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um tradutor profissional especializado em manter o estilo e nuances do texto original."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.13
        )
        
        # Extrair a tradução da resposta
        translation = response.choices[0].message.content
        
        return {"translated_text": translation}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Montar arquivos estáticos (frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
