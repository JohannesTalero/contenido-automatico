"""
Módulo de transcripción con Whisper.
"""

import torch
from faster_whisper import WhisperModel


def obtener_device():
    """
    Detecta el mejor device disponible.
    
    Returns:
        tuple (device, compute_type)
    """
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        if gpu_memory < 6:
            return "cuda", "int8_float16"
        else:
            return "cuda", "float16"
    else:
        return "cpu", "int8"


def transcribir_audio(audio_path, model_size="base", language=None):
    """
    Transcribe audio usando faster-whisper con timestamps a nivel de palabra.
    
    Args:
        audio_path: Path al archivo de audio
        model_size: Tamaño del modelo (tiny, base, small, medium, large)
        language: Código de idioma (es, en, etc.) o None para autodetección
    
    Returns:
        dict con:
            - palabras: lista de {word, start, end, probability}
            - idioma: código del idioma detectado
            - texto_completo: transcripción completa
    """
    device, compute_type = obtener_device()
    
    print(f"[*] Transcribiendo con faster-whisper ({device})...")
    
    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        segments, info = model.transcribe(
            str(audio_path), 
            word_timestamps=True,
            language=language
        )
        
        palabras = []
        for segment in segments:
            if hasattr(segment, 'words') and segment.words:
                for word in segment.words:
                    palabras.append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end,
                        "probability": word.probability
                    })
        
        texto_completo = " ".join([w['word'].strip() for w in palabras])
        
        return {
            'palabras': palabras,
            'idioma': info.language,
            'texto_completo': texto_completo
        }
        
    except Exception as e:
        if device == "cuda":
            print(f"[!] Error con GPU: {e}")
            print("[*] Reintentando con CPU...")
            model = WhisperModel(model_size, device="cpu", compute_type="int8")
            segments, info = model.transcribe(
                str(audio_path),
                word_timestamps=True,
                language=language
            )
            
            palabras = []
            for segment in segments:
                if hasattr(segment, 'words') and segment.words:
                    for word in segment.words:
                        palabras.append({
                            "word": word.word,
                            "start": word.start,
                            "end": word.end,
                            "probability": word.probability
                        })
            
            texto_completo = " ".join([w['word'].strip() for w in palabras])
            
            return {
                'palabras': palabras,
                'idioma': info.language,
                'texto_completo': texto_completo
            }
        else:
            raise

