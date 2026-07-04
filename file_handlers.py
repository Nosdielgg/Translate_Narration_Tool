# ===============================================
# === FUNÇÕES DE MANIPULAÇÃO DE ARQUIVOS ===
# ===============================================

import os
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

def read_file_text(file_path):
    """Lê o conteúdo de arquivos TXT e DOCX."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".txt":
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == ".docx":
        return read_docx_text(file_path)
    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .docx.")

def read_docx_text(docx_path):
    """Lê texto de arquivos DOCX."""
    doc = Document(docx_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

def read_srt(srt_path):
    """Lê arquivos SRT e extrai o texto."""
    try:
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remove números e timestamps
            content = re.sub(r'^\d+\n', '', content, flags=re.MULTILINE)
            content = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', content, flags=re.MULTILINE)
            text_blocks = [block.strip() for block in content.split('\n\n') if block.strip()]
            return text_blocks
    except Exception as e:
        raise Exception(f"Falha ao ler arquivo SRT: {e}")

def apply_paragraph_formatting(paragraph):
    """Aplica formatação consistente a parágrafos do Word."""
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.line_spacing = 1.0
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(12)
    
    for run in paragraph.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(11)
