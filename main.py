# ===============================================
# === PONTO DE ENTRADA DA APLICAÇÃO ===
# ===============================================

import tkinter as tk
from tkinter import messagebox
from .app import TranslateNarrateApp

def check_dependencies():
    """Verifica se todas as dependências estão instaladas."""
    try:
        import edge_tts
    except ImportError:
        messagebox.showerror("Dependency Error", 
                           "The 'edge-tts' library is required. Install with: pip install edge-tts")
        return False
    
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        messagebox.showerror("Dependency Error", 
                           "The 'deep-translator' library is required. Install with: pip install deep-translator")
        return False
    
    try:
        from docx import Document
    except ImportError:
        messagebox.showerror("Dependency Error", 
                           "The 'python-docx' library is required. Install with: pip install python-docx")
        return False
    
    return True

def main():
    """Função principal para iniciar a aplicação."""
    if not check_dependencies():
        return
    
    root = tk.Tk()
    app = TranslateNarrateApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
