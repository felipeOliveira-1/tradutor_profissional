from flask import jsonify, request
from app import db
from app.api import bp
from app.models import Translation
from app.services.translator import TranslatorService

@bp.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
        
    source_text = data.get('text')
    source_lang = data.get('source_lang', 'en')
    target_lang = data.get('target_lang', 'pt')
    
    try:
        # Criar o serviço de tradução dentro da rota
        translator_service = TranslatorService()
        
        # Realizar a tradução
        translated_text = translator_service.translate(
            source_text, 
            source_lang, 
            target_lang
        )
        
        # Salvar no banco de dados
        translation = Translation(
            source_text=source_text,
            translated_text=translated_text,
            source_language=source_lang,
            target_language=target_lang
        )
        db.session.add(translation)
        db.session.commit()
        
        return jsonify(translation.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/translations', methods=['GET'])
def get_translations():
    translations = Translation.query.order_by(Translation.created_at.desc()).all()
    return jsonify([t.to_dict() for t in translations])
