# ===============================================
# === INTERFACE GRÁFICA ===
# ===============================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from .constants import LANGUAGES, NEURAL_VOICES, BLUE_COLOR, GREEN_COLOR, WHITE_COLOR, W_FULL_FIT
from .translators import translate_file
from .narrators import generate_narration_from_text, generate_narration_from_srt
from .utils import extract_voice_code, update_status

class TranslateNarrateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Translate & Narration Tool")
        self.root.geometry("600x700")
        
        # Variáveis
        self.var_target_language = tk.StringVar(value="English")
        self.var_voice = tk.StringVar()
        
        # Configurar interface
        self.setup_ui()
        
        # Atualizar vozes inicialmente
        self.update_voices()
    
    def setup_ui(self):
        """Configura a interface gráfica."""
        # Frame principal com scroll
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas e Scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Título
        title_label = tk.Label(scrollable_frame, text="Translate & Narration Tool", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # === SEÇÃO 1: SELEÇÃO DE IDIOMA E VOZ ===
        section_lang = ttk.LabelFrame(scrollable_frame, text="1. Language & Neural Voice", padding=15)
        section_lang.pack(fill=tk.X, pady=10)
        
        # Idioma Alvo
        tk.Label(section_lang, text="Target Language:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        self.cb_language = ttk.Combobox(
            section_lang,
            textvariable=self.var_target_language,
            values=list(LANGUAGES.keys()),
            state="readonly",
            width=50
        )
        self.cb_language.pack(fill=tk.X, pady=5)
        self.cb_language.bind("<<ComboboxSelected>>", self.update_voices)
        
        # Voz Neural
        tk.Label(section_lang, text="Neural Voice:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        self.cb_voice = ttk.Combobox(
            section_lang,
            textvariable=self.var_voice,
            state="readonly",
            width=50
        )
        self.cb_voice.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(scrollable_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # === SEÇÃO 2: FERRAMENTAS DE TRADUÇÃO ===
        section_translate = ttk.LabelFrame(scrollable_frame, text="2. Translation Tools", padding=15)
        section_translate.pack(fill=tk.X, pady=10)
        
        # Botão Traduzir Arquivo
        btn_translate_file = tk.Button(
            section_translate,
            text="Translate File (.SRT/.DOCX/.TXT → DOCX)",
            command=self.start_file_translation_process,
            bg=BLUE_COLOR,
            fg=WHITE_COLOR,
            font=("Arial", 10, "bold"),
            width=W_FULL_FIT,
            pady=10
        )
        btn_translate_file.pack(pady=8, fill=tk.X)
        
        # Separador
        ttk.Separator(scrollable_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # === SEÇÃO 3: FERRAMENTAS DE NARRAÇÃO ===
        section_narration = ttk.LabelFrame(scrollable_frame, text="3. Narration Tools (Text-to-Speech)", padding=15)
        section_narration.pack(fill=tk.X, pady=10)
        
        # Botão Narração de Texto
        btn_text_narration = tk.Button(
            section_narration,
            text="Generate Narration from Text File (.TXT/.DOCX)",
            command=self.start_text_narration_process,
            bg=GREEN_COLOR,
            fg=WHITE_COLOR,
            font=("Arial", 10, "bold"),
            width=W_FULL_FIT,
            pady=10
        )
        btn_text_narration.pack(pady=8, fill=tk.X)
        
        # Botão Narração de SRT
        btn_srt_narration = tk.Button(
            section_narration,
            text="Generate Narration from SRT File",
            command=self.start_srt_narration_process,
            bg=GREEN_COLOR,
            fg=WHITE_COLOR,
            font=("Arial", 10, "bold"),
            width=W_FULL_FIT,
            pady=10
        )
        btn_srt_narration.pack(pady=8, fill=tk.X)
        
        # Separador
        ttk.Separator(scrollable_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # === SEÇÃO 4: BARRA DE STATUS ===
        section_status = ttk.LabelFrame(scrollable_frame, text="Status", padding=10)
        section_status.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(
            section_status, 
            text="Ready to start...", 
            font=("Arial", 9),
            anchor=tk.W,
            justify=tk.LEFT,
            wraplength=550
        )
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Barra de progresso
        self.progress_bar = ttk.Progressbar(
            section_status, 
            orient=tk.HORIZONTAL, 
            length=100, 
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
    
    def update_status(self, message, color="black"):
        """Atualiza a barra de status."""
        def update():
            self.status_label.config(text=message, fg=color)
            if color == "blue":
                self.progress_bar.config(mode='indeterminate')
                self.progress_bar.start(10)
            elif color == "green" or color == "red":
                self.progress_bar.stop()
                self.progress_bar.config(mode='determinate', value=0)
        
        self.root.after(0, update)
    
    def update_voices(self, event=None):
        """Atualiza as vozes disponíveis com base no idioma selecionado."""
        lang = self.var_target_language.get()
        voices = NEURAL_VOICES.get(lang, [])
        self.cb_voice['values'] = voices
        if voices:
            self.cb_voice.set(voices[0])
    
    def start_file_translation_process(self):
        """Inicia o processo de tradução de arquivo."""
        input_path = filedialog.askopenfilename(
            title="1. Select SRT, DOCX or TXT file to translate",
            filetypes=[("Translatable Files", "*.srt;*.docx;*.txt"), ("All Files", "*.*")]
        )
        if not input_path:
            return
        
        output_folder = filedialog.askdirectory(title="2. Choose destination folder for translated file (DOCX)")
        if not output_folder:
            return

        target_language_key = self.var_target_language.get()
        
        from .translators import translate_file
        threading.Thread(
            target=lambda: translate_file(
                input_path, output_folder, target_language_key, self.update_status
            ), 
            daemon=True
        ).start()
    
    def start_text_narration_process(self):
        """Inicia narração a partir de arquivo de texto."""
        file_path = filedialog.askopenfilename(
            title="Select text file for narration",
            filetypes=[("Text or Word Files", "*.txt;*.docx")]
        )
        if not file_path:
            return
            
        output_folder = filedialog.askdirectory(title="Select destination folder for MP3")
        if not output_folder:
            return
            
        voice_code = extract_voice_code(self.var_voice.get())
        
        threading.Thread(
            target=lambda: generate_narration_from_text(
                file_path, output_folder, "NarracaoTexto", voice_code, self.update_status
            ), 
            daemon=True
        ).start()
    
    def start_srt_narration_process(self):
        """Inicia narração a partir de arquivo SRT."""
        file_path = filedialog.askopenfilename(
            title="Select SRT file for narration",
            filetypes=[("SRT Files", "*.srt")]
        )
        if not file_path:
            return
            
        output_folder = filedialog.askdirectory(title="Select destination folder for MP3")
        if not output_folder:
            return
            
        voice_code = extract_voice_code(self.var_voice.get())
        
        threading.Thread(
            target=lambda: generate_narration_from_srt(
                file_path, output_folder, "NarracaoSRT", voice_code, self.update_status
            ), 
            daemon=True
        ).start()
