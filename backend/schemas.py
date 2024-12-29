from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class TranslationBase(BaseModel):
    original_text: str
    source_language: str = "en"
    target_language: str = "pt"
    formality_level: Optional[str] = None
    style: Optional[str] = None
    context: Optional[str] = None

class TranslationCreate(TranslationBase):
    pass

class TranslationUpdate(BaseModel):
    translated_text: str
    has_been_edited: Optional[int] = None
    quality_rating: Optional[int] = None
    feedback_notes: Optional[str] = None

class Translation(TranslationBase):
    id: int
    translated_text: str
    created_at: datetime
    has_been_edited: int
    quality_rating: Optional[int] = None
    feedback_notes: Optional[str] = None

    class Config:
        from_attributes = True

# Novos schemas para documentos
class DocumentMetadata(BaseModel):
    filename: str
    mime_type: str
    size: int
    num_chapters: int
    total_paragraphs: int

class ChapterContent(BaseModel):
    chapter_title: str
    paragraphs: List[str]

class DocumentContent(BaseModel):
    metadata: DocumentMetadata
    chapters: Dict[str, List[str]]

class DocumentTranslationRequest(BaseModel):
    document_id: str
    chapter_title: Optional[str] = None
    start_paragraph: Optional[int] = None
    end_paragraph: Optional[int] = None
    source_language: str = "en"
    target_language: str = "pt"
    formality_level: Optional[str] = None
    style: Optional[str] = None

class DocumentTranslationResponse(BaseModel):
    document_id: str
    chapter_title: Optional[str]
    original_paragraphs: List[str]
    translated_paragraphs: List[str]
    translation_status: str
    progress_percentage: float
