"""
Módulo de análisis de transcripciones.
Detecta segmentos útiles, conceptos clave y brechas.
"""

def analizar_transcripcion(palabras, metadata=None):
    """
    Analiza la transcripción palabra por palabra.
    
    Args:
        palabras: Lista de diccionarios con {word, start, end, probability}
        metadata: Diccionario opcional con información adicional
    
    Returns:
        dict con análisis: {
            'texto_completo': str,
            'duracion_total': float,
            'num_palabras': int,
            'segmentos_silencio': list,
            'palabras': list
        }
    """
    if not palabras:
        return {
            'texto_completo': '',
            'duracion_total': 0,
            'num_palabras': 0,
            'segmentos_silencio': [],
            'palabras': []
        }
    
    texto = " ".join([w['word'].strip() for w in palabras])
    duracion = palabras[-1]['end'] - palabras[0]['start']
    
    # Detectar silencios entre palabras (> 1.5 segundos)
    silencios = []
    for i in range(len(palabras) - 1):
        gap = palabras[i+1]['start'] - palabras[i]['end']
        if gap > 1.5:
            silencios.append({
                'inicio': palabras[i]['end'],
                'fin': palabras[i+1]['start'],
                'duracion': gap
            })
    
    return {
        'texto_completo': texto,
        'duracion_total': duracion,
        'num_palabras': len(palabras),
        'segmentos_silencio': silencios,
        'palabras': palabras
    }


def crear_shotlist(palabras, cortes=None):
    """
    Crea una shotlist básica a partir de las palabras y cortes opcionales.
    
    Args:
        palabras: Lista de palabras con timestamps
        cortes: Lista opcional de tuplas (inicio, fin) en segundos
    
    Returns:
        list de clips: [{inicio, fin, texto, duracion}]
    """
    if not palabras:
        return []
    
    clips = []
    
    if cortes:
        # Usar cortes manuales
        for idx, (inicio, fin) in enumerate(cortes):
            palabras_clip = [
                w for w in palabras 
                if w['start'] >= inicio and w['end'] <= fin
            ]
            texto = " ".join([w['word'].strip() for w in palabras_clip])
            
            clips.append({
                'orden': idx + 1,
                'inicio': inicio,
                'fin': fin,
                'duracion': fin - inicio,
                'texto': texto,
                'num_palabras': len(palabras_clip)
            })
    else:
        # Un solo clip con todo el contenido
        clips.append({
            'orden': 1,
            'inicio': palabras[0]['start'],
            'fin': palabras[-1]['end'],
            'duracion': palabras[-1]['end'] - palabras[0]['start'],
            'texto': " ".join([w['word'].strip() for w in palabras]),
            'num_palabras': len(palabras)
        })
    
    return clips

