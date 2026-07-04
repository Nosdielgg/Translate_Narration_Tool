# ===============================================
# === FUNÇÕES AUXILIARES ===
# ===============================================

import re
import os

def safe_filename(name):
    """Remove caracteres inválidos para nomes de arquivo."""
    return re.sub(r'[\\/:"*?<>|]', "_", name)

def extract_voice_code(voice_name):
    """Extrai o código da voz do nome completo."""
    return voice_name.split(' ')[0]

def update_status(status_label, progress_bar, message, color="black"):
    """Atualiza a barra de status de forma thread-safe."""
    def update():
        status_label.config(text=message, fg=color)
        if color == "blue":
            progress_bar.config(mode='indeterminate')
            progress_bar.start(10)
        elif color == "green" or color == "red":
            progress_bar.stop()
            progress_bar.config(mode='determinate', value=0)
    
    return update
