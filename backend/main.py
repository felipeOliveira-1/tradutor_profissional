from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

from database import engine, get_db
import models
import schemas

# Criar as tabelas do banco de dados
models.Base.metadata.create_all(bind=engine)

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

@app.post("/api/translate", response_model=schemas.Translation)
async def translate_text(request: schemas.TranslationCreate, db: Session = Depends(get_db)):
    try:
        # Criar o prompt para o modelo
        prompt = f"""Traduza o seguinte texto de {request.source_language} para {request.target_language}. 
        Mantenha o estilo e o tom do texto original:
        
        {request.original_text}"""
        
        # Fazer a requisição para a API da OpenAI
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um tradutor profissional especializado em manter o estilo e nuances do texto original."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.13
        )
        
        # Extrair a tradução da resposta
        translated_text = response.choices[0].message.content
        
        # Criar objeto de tradução no banco de dados
        db_translation = models.Translation(
            original_text=request.original_text,
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language,
            formality_level=request.formality_level,
            style=request.style,
            context=request.context
        )
        
        db.add(db_translation)
        db.commit()
        db.refresh(db_translation)
        
        return db_translation
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/translations", response_model=list[schemas.Translation])
def get_translations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    translations = db.query(models.Translation).offset(skip).limit(limit).all()
    return translations

@app.get("/api/translations/{translation_id}", response_model=schemas.Translation)
def get_translation(translation_id: int, db: Session = Depends(get_db)):
    translation = db.query(models.Translation).filter(models.Translation.id == translation_id).first()
    if translation is None:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation

@app.put("/api/translations/{translation_id}", response_model=schemas.Translation)
def update_translation(translation_id: int, translation: schemas.TranslationUpdate, db: Session = Depends(get_db)):
    db_translation = db.query(models.Translation).filter(models.Translation.id == translation_id).first()
    if db_translation is None:
        raise HTTPException(status_code=404, detail="Translation not found")
    
    for field, value in translation.dict(exclude_unset=True).items():
        setattr(db_translation, field, value)
    
    if translation.translated_text != db_translation.translated_text:
        db_translation.has_been_edited += 1
    
    db.commit()
    db.refresh(db_translation)
    return db_translation
