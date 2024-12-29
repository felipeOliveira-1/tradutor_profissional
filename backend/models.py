from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship, Session
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

    # Relacionamentos
    documents = relationship("Document", back_populates="translator_profile")
    translations = relationship("Translation", back_populates="translator_profile")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_path = Column(String)
    processed_path = Column(String, nullable=True)
    mime_type = Column(String)
    size = Column(Integer)
    num_chapters = Column(Integer, default=0)
    total_paragraphs = Column(Integer, default=0)
    document_metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_confidential = Column(Boolean, default=False)
    translator_profile_id = Column(Integer, ForeignKey("translator_profiles.id"), nullable=True)

    # Relacionamentos
    translator_profile = relationship("TranslatorProfile", back_populates="documents")
    chapters = relationship("Chapter", back_populates="document", cascade="all, delete-orphan")
    translations = relationship("Translation", back_populates="document")

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    title = Column(String)
    order = Column(Integer)
    content = Column(JSON)  # Armazena parágrafos e metadados
    translated_content = Column(JSON, nullable=True)  # Versão traduzida
    translation_status = Column(String, default="pending")  # pending, in_progress, completed
    progress_percentage = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    document = relationship("Document", back_populates="chapters")
    translations = relationship("Translation", back_populates="chapter")

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    formality_level = Column(String(20), nullable=True)  # formal, informal, neutral
    tone = Column(String(50), nullable=True)  # academic, literary, technical, casual
    domain_specific = Column(String(50), nullable=True)  # legal, medical, literary, etc.
    preserve_formatting = Column(Boolean, default=True)
    locale_specific = Column(String(20), nullable=True)  # pt-BR, pt-PT, etc.
    quality_score = Column(Float, nullable=True)  # 0-1 score
    revision_needed = Column(Boolean, default=False)
    has_been_edited = Column(Integer, default=0)
    edit_distance = Column(Integer, nullable=True)  # Distância entre original e editado
    translator_feedback = Column(Text, nullable=True)
    improvement_suggestions = Column(JSON, nullable=True)
    learning_flags = Column(JSON, nullable=True)  # Marcadores para aprendizado
    project_id = Column(String(50), nullable=True)
    security_level = Column(String(20), default="standard")
    is_confidential = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Chaves estrangeiras
    translator_profile_id = Column(Integer, ForeignKey("translator_profiles.id"), nullable=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)

    # Relacionamentos
    translator_profile = relationship("TranslatorProfile", back_populates="translations")
    document = relationship("Document", back_populates="translations")
    chapter = relationship("Chapter", back_populates="translations")
    revisions = relationship("TranslationRevision", back_populates="translation", cascade="all, delete-orphan")

class TranslationRevision(Base):
    __tablename__ = "translation_revisions"

    id = Column(Integer, primary_key=True, index=True)
    translation_id = Column(Integer, ForeignKey("translations.id"), nullable=False)
    revised_text = Column(Text, nullable=False)
    revision_type = Column(String(50), nullable=True)  # style, grammar, context, etc.
    revision_comments = Column(Text, nullable=True)
    time_spent = Column(Integer, nullable=True)  # tempo em segundos
    quality_improvement = Column(Float, nullable=True)  # 0-1 score
    accepted_changes = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    translation = relationship("Translation", back_populates="revisions")
