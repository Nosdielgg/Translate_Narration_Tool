# ===============================================
# === FUNÇÕES DE TRADUÇÃO ===
# ===============================================

import time
import re
from deep_translator import GoogleTranslator

def translate_text_in_segments(text, target_language_code, status_callback=None):
    """Traduz texto segmentado usando GoogleTranslator."""
    segments = [s.strip() for s in text.split('\n') if s.strip()]
    translated_texts = []
    
    if status_callback:
        status_callback("Preparando tradução...", "blue")
    
    try:
        translator = GoogleTranslator(source='auto', target=target_language_code)
        total_segments = len(segments)
        
        for i, segment in enumerate(segments):
            progress = int(((i + 1) / total_segments) * 100)
            if status_callback:
                status_callback(f"Traduzindo segmento {i+1}/{total_segments} ({progress}%)...", "blue")
            
            # Limpeza do texto
            cleaned_segment = re.sub(r'[^\w\s.,!?;:()\'"áéíóúÁÉÍÓÚãõñÃÕÑçÇ]', ' ', segment).strip()
            
            if not cleaned_segment:
                translated_texts.append("")
                continue

            # Tentativas de tradução com retry
            translation_result = None
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    translation_result = translator.translate(cleaned_segment)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(1 + attempt * 0.5)
                        continue
                    else:
                        translation_result = segment  # Fallback para texto original
            
            translated_texts.append(translation_result if translation_result else segment)

        if status_callback:
            status_callback("Tradução concluída!", "green")
        return translated_texts
    
    except Exception as e:
        if status_callback:
            status_callback("Erro na tradução.", "red")
        raise Exception(f"Falha na tradução: {e}")
