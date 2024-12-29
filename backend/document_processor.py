import os
import PyPDF2
from docx import Document as DocxDocument
import logging
import json
from typing import Dict, List, Optional
import traceback
import re

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.supported_types = {
            'application/pdf': self._process_pdf,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': self._process_docx,
            'text/plain': self._process_txt
        }

    def process_document(self, file_path: str, mime_type: str) -> Dict:
        """
        Processa um documento e retorna seus metadados e conteúdo estruturado.
        """
        try:
            if mime_type not in self.supported_types:
                raise ValueError(f"Tipo de arquivo não suportado: {mime_type}")

            logger.info(f"Processando documento: {file_path}")
            logger.info(f"Tipo MIME: {mime_type}")

            processor = self.supported_types[mime_type]
            result = processor(file_path)

            logger.info(f"Documento processado com sucesso: {len(result['chapters'])} capítulos encontrados")
            return result

        except Exception as e:
            logger.error(f"Erro ao processar documento: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def _process_pdf(self, file_path: str) -> Dict:
        """
        Processa um arquivo PDF e extrai seu conteúdo estruturado.
        """
        try:
            chapters = []
            metadata = {}

            with open(file_path, 'rb') as file:
                try:
                    reader = PyPDF2.PdfReader(file)
                    logger.info(f"PDF aberto com sucesso: {len(reader.pages)} páginas")
                    
                    # Extrair metadados
                    metadata = {
                        'num_pages': len(reader.pages),
                        'author': reader.metadata.get('/Author', ''),
                        'creator': reader.metadata.get('/Creator', ''),
                        'producer': reader.metadata.get('/Producer', ''),
                        'subject': reader.metadata.get('/Subject', ''),
                        'title': reader.metadata.get('/Title', ''),
                    }
                    logger.info(f"Metadados extraídos: {metadata}")

                    current_chapter = {
                        'title': 'Chapter 1',
                        'paragraphs': []
                    }

                    # Processar cada página
                    for page_num in range(len(reader.pages)):
                        try:
                            page = reader.pages[page_num]
                            text = page.extract_text()
                            
                            if not text or not text.strip():
                                logger.warning(f"Página {page_num + 1} está vazia")
                                continue

                            # Dividir o texto em parágrafos
                            paragraphs = []
                            current_paragraph = []
                            
                            for line in text.split('\n'):
                                line = line.strip()
                                if not line:
                                    if current_paragraph:
                                        paragraphs.append(' '.join(current_paragraph))
                                        current_paragraph = []
                                else:
                                    current_paragraph.append(line)
                            
                            if current_paragraph:
                                paragraphs.append(' '.join(current_paragraph))

                            # Filtrar parágrafos vazios
                            paragraphs = [p for p in paragraphs if p.strip()]
                            
                            # Detectar possíveis títulos de capítulo
                            for p in paragraphs:
                                # Padrões para títulos de capítulo
                                chapter_patterns = [
                                    r'^chapter\s+\d+',
                                    r'^capítulo\s+\d+',
                                    r'^\d+\.\s+',
                                    r'^part\s+\d+',
                                    r'^section\s+\d+',
                                ]
                                
                                is_chapter = any(re.match(pattern, p.lower()) for pattern in chapter_patterns)
                                
                                if is_chapter or (len(p) < 100 and p.isupper()):
                                    # Se encontrarmos um novo capítulo, salvamos o atual e começamos um novo
                                    if current_chapter['paragraphs']:
                                        chapters.append(current_chapter)
                                    current_chapter = {
                                        'title': p,
                                        'paragraphs': []
                                    }
                                else:
                                    current_chapter['paragraphs'].append(p)

                        except Exception as e:
                            logger.error(f"Erro ao processar página {page_num + 1}: {str(e)}")
                            logger.error(traceback.format_exc())
                            continue

                    # Adicionar o último capítulo
                    if current_chapter['paragraphs']:
                        chapters.append(current_chapter)

                    logger.info(f"Processamento do PDF concluído: {len(chapters)} capítulos encontrados")

                except Exception as e:
                    logger.error(f"Erro ao ler o PDF: {str(e)}")
                    logger.error(traceback.format_exc())
                    raise

            # Se nenhum capítulo foi encontrado, criar um capítulo padrão
            if not chapters:
                logger.warning("Nenhum capítulo encontrado, criando capítulo padrão")
                chapters = [{
                    'title': 'Document Content',
                    'paragraphs': ['Não foi possível extrair o conteúdo do documento.']
                }]

            return {
                'metadata': metadata,
                'chapters': chapters
            }

        except Exception as e:
            logger.error(f"Erro ao processar PDF: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def _process_docx(self, file_path: str) -> Dict:
        """
        Processa um arquivo DOCX e extrai seu conteúdo estruturado.
        """
        try:
            doc = DocxDocument(file_path)
            chapters = []
            current_chapter = {
                'title': 'Chapter 1',
                'paragraphs': []
            }

            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if not text:
                    continue

                # Detectar possíveis títulos de capítulo
                if len(text) < 100 and ('chapter' in text.lower() or 'capítulo' in text.lower()):
                    if current_chapter['paragraphs']:
                        chapters.append(current_chapter)
                    current_chapter = {
                        'title': text,
                        'paragraphs': []
                    }
                else:
                    current_chapter['paragraphs'].append(text)

            # Adicionar o último capítulo
            if current_chapter['paragraphs']:
                chapters.append(current_chapter)

            # Extrair metadados
            metadata = {
                'author': doc.core_properties.author or '',
                'created': str(doc.core_properties.created) if doc.core_properties.created else '',
                'modified': str(doc.core_properties.modified) if doc.core_properties.modified else '',
                'title': doc.core_properties.title or '',
            }

            return {
                'metadata': metadata,
                'chapters': chapters
            }

        except Exception as e:
            logger.error(f"Erro ao processar DOCX: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def _process_txt(self, file_path: str) -> Dict:
        """
        Processa um arquivo TXT e extrai seu conteúdo estruturado.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Dividir em parágrafos
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

            # Criar um único capítulo com todos os parágrafos
            chapters = [{
                'title': 'Text Content',
                'paragraphs': paragraphs
            }]

            # Metadados básicos
            metadata = {
                'size': os.path.getsize(file_path),
                'modified': str(os.path.getmtime(file_path)),
                'created': str(os.path.getctime(file_path)),
            }

            return {
                'metadata': metadata,
                'chapters': chapters
            }

        except Exception as e:
            logger.error(f"Erro ao processar TXT: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
