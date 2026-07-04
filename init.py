# Pacote src
from .app import TranslateNarrateApp
from .constants import LANGUAGES, NEURAL_VOICES
from .translators import translate_file
from .narrators import generate_narration_from_text, generate_narration_from_srt

__version__ = "1.0.0"
__all__ = [
    'TranslateNarrateApp',
    'LANGUAGES',
    'NEURAL_VOICES',
    'translate_file',
    'generate_narration_from_text',
    'generate_narration_from_srt'
]
