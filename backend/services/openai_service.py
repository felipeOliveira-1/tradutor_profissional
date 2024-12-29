import os
import logging
import json
from typing import Dict, List, Optional
import traceback
from openai import OpenAI
import asyncio
from functools import partial

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def translate_text(text: str, source_language: str, target_language: str, formality: str = 'neutral', style: str = 'general') -> str:
    """
    Traduz um texto de um idioma para outro usando a API da OpenAI.
    
    Args:
        text (str): Texto a ser traduzido
        source_language (str): Idioma de origem
        target_language (str): Idioma de destino
        formality (str): Nível de formalidade (formal, neutral, informal)
        style (str): Estilo da tradução (general, technical, literary, academic)
    """
    try:
        logger.info(f"Iniciando tradução de {source_language} para {target_language} (Formalidade: {formality}, Estilo: {style})")
        
        # Criar o prompt para a tradução com instruções específicas de formalidade e estilo
        system_prompt = f"""You are a professional translator. Translate the following text from {source_language} to {target_language}.
Follow these specific guidelines:
- Formality: Use a {formality} tone (e.g. {
    'formal language, avoiding colloquialisms' if formality == 'formal'
    else 'balanced and natural language' if formality == 'neutral'
    else 'casual and conversational language'
})
- Style: Follow a {style} style (e.g. {
    'clear and straightforward language' if style == 'general'
    else 'precise technical terminology and clear structure' if style == 'technical'
    else 'elegant and expressive language' if style == 'literary'
    else 'scholarly and methodical approach' if style == 'academic'
    else 'clear and straightforward language'
})
Maintain the original meaning while adapting the translation according to these requirements."""

        user_prompt = f"Text to translate:\n{text}"
        
        # Criar uma função parcial para a chamada da API
        api_call = partial(
            client.chat.completions.create,
            model="gpt-4o",  # ou "gpt-3.5-turbo" para um modelo mais rápido e econômico
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.13,  # Menor temperatura para traduções mais precisas
            max_tokens=2000,  # Ajustar conforme necessário
        )
        
        # Executar a chamada da API em um thread separado
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, api_call)
        
        # Extrair a tradução da resposta
        translated_text = response.choices[0].message.content.strip()
        
        logger.info("Tradução concluída com sucesso")
        return translated_text
        
    except Exception as e:
        logger.error(f"Erro durante a tradução: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise
