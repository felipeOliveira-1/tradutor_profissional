from pydantic import BaseModel
from typing import Optional
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
