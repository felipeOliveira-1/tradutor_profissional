from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime
import mimetypes
import logging
import traceback

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

def get_mime_type(filename: str) -> str:
    """Determina o tipo MIME baseado na extensão do arquivo."""
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        # Mapear extensões comuns
        ext = os.path.splitext(filename)[1].lower()
        mime_map = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain'
        }
        mime_type = mime_map.get(ext)
    return mime_type

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = None
    try:
        logger.info(f"Iniciando upload do arquivo: {file.filename}")
        
        # Verificar tipo de arquivo
        mime_type = get_mime_type(file.filename)
        if not mime_type:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível determinar o tipo do arquivo"
            )
        
        logger.info(f"Tipo de arquivo detectado: {mime_type}")
        
        allowed_types = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ]
        
        if mime_type not in allowed_types:
            logger.warning(f"Tipo de arquivo não suportado: {mime_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de arquivo não suportado: {mime_type}. Use PDF, DOCX ou TXT."
            )
        
        # Criar nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        logger.info(f"Salvando arquivo em: {file_path}")
        
        # Salvar arquivo
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info("Arquivo salvo com sucesso")
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {str(e)}")
        
        # Processar documento
        try:
            logger.info("Iniciando processamento do documento")
            processor = DocumentProcessor()
            processed_data = processor.process_document(file_path, mime_type)
            logger.info("Documento processado com sucesso")
            
            # Debug do processed_data
            logger.info(f"Dados processados: {processed_data}")
            
            # Criar entrada no banco de dados
            logger.info("Criando entrada no banco de dados")
            db_document = Document(
                filename=file.filename,
                file_path=file_path,
                mime_type=mime_type,
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
            logger.error(f"Erro ao processar documento: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Erro ao processar documento: {str(e)}")
            
    except Exception as e:
        logger.error(f"Erro durante o upload: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        # Se algo der errado, garantir que o arquivo seja removido
        if file_path and os.path.exists(file_path):
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
        logger.error(f"Erro ao listar documentos: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
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
        
        # Processar o documento para obter os capítulos
        try:
            processor = DocumentProcessor()
            processed_data = processor.process_document(document.file_path, document.mime_type)
            
            # Combinar dados do banco com os dados processados
            response_data = {
                "id": document.id,
                "filename": document.filename,
                "mime_type": document.mime_type,
                "size": document.size,
                "created_at": document.created_at,
                "chapters": processed_data.get("chapters", []),
                "metadata": processed_data.get("metadata", {})
            }
            return response_data
            
        except Exception as e:
            logger.error(f"Erro ao processar documento: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar documento: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar documento {document_id}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar documento: {str(e)}"
        )
