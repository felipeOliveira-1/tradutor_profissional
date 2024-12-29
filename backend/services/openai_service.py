import os
from openai import AsyncOpenAI
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar OpenAI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def translate_text(
    text: str,
    source_language: str,
    target_language: str,
    formality_level: Optional[str] = "neutral",
    tone: Optional[str] = None
) -> str:
    """
    Traduz texto usando a API GPT da OpenAI.
    """
    try:
        logger.info(f"Iniciando tradução com OpenAI: {text[:50]}...")
        
        # Construir o prompt
        system_prompt = f"""You are a professional translator. 
        Translate the following text from {source_language} to {target_language}.
        Formality level: {formality_level}
        {f'Tone: {tone}' if tone else ''}
        
        Maintain the original formatting and structure.
        Preserve any special characters, numbers, or technical terms as appropriate.
        """
        
        user_prompt = text
        
        # Fazer a chamada à API
        response = await client.chat.completions.create(
            model="gpt-4o",  # ou outro modelo apropriado
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.13,  # menor temperatura para traduções mais precisas
            max_tokens=2000,  # ajuste conforme necessário
        )
        
        translated_text = response.choices[0].message.content.strip()
        logger.info("Tradução concluída com sucesso")
        
        return translated_text
        
    except Exception as e:
        logger.error(f"Erro na tradução com OpenAI: {str(e)}", exc_info=True)
        raise Exception(f"Erro na tradução: {str(e)}")
