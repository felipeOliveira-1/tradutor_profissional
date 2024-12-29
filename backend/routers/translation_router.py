from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime
from pydantic import BaseModel
import traceback

from database import get_db
from models import Translation, Document, Chapter
from services.openai_service import translate_text

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Schema para requisição de tradução
class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str
    formality_level: Optional[str] = "neutral"
    tone: Optional[str] = None

# Schema para resposta de tradução
class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    created_at: datetime

# Endpoint para tradução rápida (sem salvar no banco)
@router.post("/quick")
async def translate_quick(
    request: TranslationRequest,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Iniciando tradução rápida de {request.source_language} para {request.target_language}")
        logger.info(f"Texto a ser traduzido: {request.text[:100]}...")  # Log apenas os primeiros 100 caracteres
        
        translated_text = await translate_text(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language
        )
        
        logger.info("Tradução concluída com sucesso")
        
        return {
            "translated_text": translated_text,
            "source_language": request.source_language,
            "target_language": request.target_language
        }
        
    except Exception as e:
        logger.error(f"Erro durante a tradução: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao traduzir texto: {str(e)}"
        )

# Endpoint para tradução com histórico
@router.post("/", response_model=TranslationResponse)
async def translate(
    request: TranslationRequest,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Iniciando tradução: {request.text[:50]}...")
        
        # Realizar a tradução
        translated_text = await translate_text(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language,
            formality_level=request.formality_level,
            tone=request.tone
        )
        
        # Criar registro da tradução
        translation = Translation(
            original_text=request.text,
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language,
            formality_level=request.formality_level,
            tone=request.tone,
            created_at=datetime.utcnow()
        )
        
        db.add(translation)
        db.commit()
        db.refresh(translation)
        
        logger.info(f"Tradução concluída e salva com ID: {translation.id}")
        
        return TranslationResponse(
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language,
            created_at=translation.created_at
        )
        
    except Exception as e:
        logger.error(f"Erro durante a tradução: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a tradução: {str(e)}"
        )

@router.get("/", response_model=List[TranslationResponse])
def list_translations(db: Session = Depends(get_db)):
    try:
        logger.info("Listando traduções")
        translations = db.query(Translation).order_by(Translation.created_at.desc()).all()
        return [
            TranslationResponse(
                translated_text=t.translated_text,
                source_language=t.source_language,
                target_language=t.target_language,
                created_at=t.created_at
            ) for t in translations
        ]
    except Exception as e:
        logger.error(f"Erro ao listar traduções: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar traduções: {str(e)}"
        )

@router.get("/{translation_id}", response_model=TranslationResponse)
def get_translation(translation_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando tradução {translation_id}")
        translation = db.query(Translation).filter(Translation.id == translation_id).first()
        if not translation:
            raise HTTPException(status_code=404, detail="Tradução não encontrada")
            
        return TranslationResponse(
            translated_text=translation.translated_text,
            source_language=translation.source_language,
            target_language=translation.target_language,
            created_at=translation.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar tradução: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar tradução: {str(e)}"
        )
