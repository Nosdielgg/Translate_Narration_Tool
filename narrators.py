# ===============================================
# === FUNÇÕES DE NARRAÇÃO (TEXT-TO-SPEECH) ===
# ===============================================

import asyncio
import os
import edge_tts
from .file_handlers import read_file_text, read_srt
from .utils import safe_filename

async def async_generate_narration(full_text, final_mp3_path, voice_code):
    """Gera narração assíncrona usando Edge TTS."""
    communicate = edge_tts.Communicate(full_text, voice_code)
    await communicate.save(final_mp3_path)

def generate_narration_from_text(file_path, output_folder, base_name, voice_code, status_callback=None):
    """Gera narração a partir de arquivo de texto."""
    if status_callback:
        status_callback("Lendo arquivo de texto...", "blue")
    
    try:
        full_text = read_file_text(file_path)
    except Exception as e:
        if status_callback:
            status_callback("Erro de leitura.", "red")
        raise Exception(f"Falha ao ler o arquivo: {e}")
        
    if status_callback:
        status_callback(f"Gerando áudio de narração com voz {voice_code}...", "blue")

    try:
        os.makedirs(output_folder, exist_ok=True)
        safe_name = safe_filename(base_name)
        
        base_mp3_path = os.path.join(output_folder, f"{safe_name}_Narration_{voice_code}.mp3")
        final_mp3_path = base_mp3_path
        
        counter = 1
        while os.path.exists(final_mp3_path):
            final_mp3_path = os.path.join(output_folder, f"{safe_name}_Narration_{voice_code}({counter}).mp3")
            counter += 1

        asyncio.run(async_generate_narration(full_text, final_mp3_path, voice_code))

        if status_callback:
            status_callback("Narração concluída. MP3 salvo!", "green")
        return final_mp3_path
    
    except Exception as e:
        if status_callback:
            status_callback("Erro gerando narração.", "red")
        raise Exception(f"Falha ao gerar áudio TTS: {e}")

def generate_narration_from_srt(srt_path, output_folder, base_name, voice_code, status_callback=None):
    """Gera narração a partir de arquivo SRT."""
    if status_callback:
        status_callback("Lendo arquivo SRT e extraindo texto...", "blue")
    
    text_segments = read_srt(srt_path)
    if not text_segments:
        raise Exception("Erro lendo texto do SRT.")
        
    full_text = '\n\n'.join(text_segments)
    
    if status_callback:
        status_callback(f"Gerando narração a partir de SRT com voz {voice_code}...", "blue")

    try:
        os.makedirs(output_folder, exist_ok=True)
        safe_name = safe_filename(base_name)
        
        base_mp3_path = os.path.join(output_folder, f"{safe_name}_SRT_Narration_{voice_code}.mp3")
        final_mp3_path = base_mp3_path
        
        counter = 1
        while os.path.exists(final_mp3_path):
            final_mp3_path = os.path.join(output_folder, f"{safe_name}_SRT_Narration_{voice_code}({counter}).mp3")
            counter += 1

        asyncio.run(async_generate_narration(full_text, final_mp3_path, voice_code))

        if status_callback:
            status_callback("Narração SRT concluída!", "green")
        return final_mp3_path
    
    except Exception as e:
        if status_callback:
            status_callback("Erro gerando narração SRT.", "red")
        raise Exception(f"Falha ao gerar áudio TTS do SRT: {e}")
