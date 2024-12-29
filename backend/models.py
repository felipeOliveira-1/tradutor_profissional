from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Campos adicionais para personalização
    formality_level = Column(String(20), nullable=True)  # formal, informal, etc.
    style = Column(String(50), nullable=True)  # literário, técnico, etc.
    context = Column(String(100), nullable=True)  # contexto da tradução
    
    # Campos para feedback e qualidade
    has_been_edited = Column(Integer, default=0)  # contador de edições
    quality_rating = Column(Integer, nullable=True)  # avaliação de 1-5
    feedback_notes = Column(Text, nullable=True)  # notas de feedback
