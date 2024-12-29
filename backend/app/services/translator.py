import os
import openai
from flask import current_app

class TranslatorService:
    def __init__(self):
        pass
        
    def translate(self, text, source_lang, target_lang):
        try:
            # Configurar a API key dentro do contexto da aplicação
            openai.api_key = current_app.config['OPENAI_API_KEY']
            
            prompt = f"""Traduza o seguinte texto de {source_lang} para {target_lang}. 
            Mantenha o estilo e o tom do texto original:
            
            {text}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um tradutor profissional especializado em manter o estilo e nuances do texto original."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error in translation: {str(e)}")
