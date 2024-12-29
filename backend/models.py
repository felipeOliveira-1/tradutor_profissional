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
    filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    size = Column(Integer)
    num_chapters = Column(Integer, default=0)
    total_paragraphs = Column(Integer, default=0)
    document_metadata = Column(JSON, nullable=True)
    is_confidential = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    chapters = relationship("Chapter", back_populates="document", cascade="all, delete-orphan")
    translations = relationship("Translation", back_populates="document", cascade="all, delete-orphan")
    translator_profile = relationship("TranslatorProfile", back_populates="documents")
    translator_profile_id = Column(Integer, ForeignKey("translator_profiles.id"), nullable=True)

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    title = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    content = Column(JSON)  # Armazena parágrafos
    translated_content = Column(JSON, nullable=True)  # Armazena traduções
    translation_status = Column(String, default="pending")  # pending, in_progress, completed
    progress_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    document = relationship("Document", back_populates="chapters")
    translations = relationship("Translation", back_populates="chapter", cascade="all, delete-orphan")

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    formality_level = Column(String)
    tone = Column(String)
    domain_specific = Column(Boolean, default=False)
    preserve_formatting = Column(Boolean, default=True)
    locale_specific = Column(Boolean, default=False)
    quality_score = Column(Float)
    revision_needed = Column(Boolean, default=False)
    has_been_edited = Column(Boolean, default=False)
    edit_distance = Column(Integer)
    translator_feedback = Column(Text)
    improvement_suggestions = Column(JSON)
    learning_flags = Column(JSON)
    project_id = Column(Integer)
    security_level = Column(String, default="normal")
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
    revision_type = Column(String)  # manual, automatic, peer
    revision_comments = Column(Text)
    time_spent = Column(Integer)  # segundos
    quality_improvement = Column(Float)
    accepted_changes = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    translation = relationship("Translation", back_populates="revisions")
