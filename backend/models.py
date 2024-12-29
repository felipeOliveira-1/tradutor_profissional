from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.sql import func
from database import Base

class TranslatorProfile(Base):
    __tablename__ = "translator_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    preferred_style = Column(JSON, nullable=True)  # Configurações detalhadas de estilo
    language_pairs = Column(JSON, nullable=True)   # Pares de idiomas suportados
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Parâmetros de estilo expandidos
    formality_level = Column(String(20), nullable=True)  # formal, informal, neutral
    tone = Column(String(50), nullable=True)  # academic, literary, technical, casual
    domain_specific = Column(String(50), nullable=True)  # legal, medical, literary, etc.
    preserve_formatting = Column(Boolean, default=True)
    locale_specific = Column(String(20), nullable=True)  # pt-BR, pt-PT, etc.
    
    # Métricas de qualidade
    quality_score = Column(Float, nullable=True)  # 0-1 score
    revision_needed = Column(Boolean, default=False)
    has_been_edited = Column(Integer, default=0)
    edit_distance = Column(Integer, nullable=True)  # Distância entre original e editado
    
    # Feedback e aprendizado
    translator_feedback = Column(Text, nullable=True)
    improvement_suggestions = Column(JSON, nullable=True)
    learning_flags = Column(JSON, nullable=True)  # Marcadores para aprendizado
    
    # Segurança e rastreamento
    project_id = Column(String(50), nullable=True)
    security_level = Column(String(20), default="standard")
    is_confidential = Column(Boolean, default=False)
    
    # Relacionamentos
    translator_profile_id = Column(Integer, ForeignKey("translator_profiles.id"), nullable=True)

class TranslationRevision(Base):
    __tablename__ = "translation_revisions"

    id = Column(Integer, primary_key=True, index=True)
    translation_id = Column(Integer, ForeignKey("translations.id"), nullable=False)
    revised_text = Column(Text, nullable=False)
    revision_type = Column(String(50), nullable=True)  # style, grammar, context, etc.
    revision_comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Métricas de revisão
    time_spent = Column(Integer, nullable=True)  # tempo em segundos
    quality_improvement = Column(Float, nullable=True)  # 0-1 score
    accepted_changes = Column(Boolean, nullable=True)
