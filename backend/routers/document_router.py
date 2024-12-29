from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime
import magic
import logging

from database import get_db
from models import Document
from document_processor import DocumentProcessor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Configurar diretório para upload
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Iniciando upload do arquivo: {file.filename}")
        
        # Verificar tipo de arquivo
        content = await file.read(2048)
        content_type = magic.from_buffer(content, mime=True)
        await file.seek(0)  # Resetar o cursor do arquivo
        
        logger.info(f"Tipo de arquivo detectado: {content_type}")
        
        allowed_types = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ]
        
        if content_type not in allowed_types:
            logger.warning(f"Tipo de arquivo não suportado: {content_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de arquivo não suportado: {content_type}. Use PDF, DOCX ou TXT."
            )
        
        # Criar nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        logger.info(f"Salvando arquivo em: {file_path}")
        
        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info("Arquivo salvo com sucesso")
        
        # Processar documento
        logger.info("Iniciando processamento do documento")
        processor = DocumentProcessor()
        processed_data = await processor.process_document(file_path, content_type)
        logger.info("Documento processado com sucesso")
        
        # Criar entrada no banco de dados
        logger.info("Criando entrada no banco de dados")
        db_document = Document(
            filename=file.filename,
            file_path=file_path,
            mime_type=content_type,
            size=os.path.getsize(file_path),
            num_chapters=len(processed_data.get("chapters", [])),
            total_paragraphs=sum(len(chapter.get("paragraphs", [])) 
                               for chapter in processed_data.get("chapters", [])),
            document_metadata=processed_data.get("metadata", {}),
            is_confidential=False  # Default
        )
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        logger.info(f"Documento {db_document.id} criado com sucesso")
        
        return {
            "id": db_document.id,
            "filename": db_document.filename,
            "size": db_document.size,
            "num_chapters": db_document.num_chapters,
            "total_paragraphs": db_document.total_paragraphs,
            "created_at": db_document.created_at
        }
        
    except Exception as e:
        logger.error(f"Erro durante o upload: {str(e)}", exc_info=True)
        # Se algo der errado, garantir que o arquivo seja removido
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Arquivo removido: {file_path}")
            except Exception as cleanup_error:
                logger.error(f"Erro ao remover arquivo: {str(cleanup_error)}")
        
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar o arquivo: {str(e)}"
        )

@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    try:
        logger.info("Listando documentos")
        documents = db.query(Document).order_by(Document.created_at.desc()).all()
        return documents
    except Exception as e:
        logger.error(f"Erro ao listar documentos: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar documentos: {str(e)}"
        )

@router.get("/{document_id}")
def get_document(document_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando documento {document_id}")
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            logger.warning(f"Documento {document_id} não encontrado")
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        return document
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar documento {document_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar documento: {str(e)}"
        )
