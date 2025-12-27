"""
Módulo de edición de video.
Cortes, limpieza de audio, normalización y exports.
"""

import subprocess
from pathlib import Path


def extraer_audio(video_path, output_path=None, sample_rate=48000):
    """
    Extrae el audio de un video como WAV mono.
    
    Args:
        video_path: Path al video
        output_path: Path de salida (opcional, se genera automático)
        sample_rate: Sample rate en Hz (default: 48000)
    
    Returns:
        Path del archivo de audio extraído
    """
    video_path = Path(video_path)
    
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}_audio.wav"
    else:
        output_path = Path(output_path)
    
    cmd = [
        'ffmpeg', '-y', '-i', str(video_path),
        '-vn', '-acodec', 'pcm_s16le',
        '-ar', str(sample_rate), '-ac', '1',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def cortar_video(video_path, inicio, fin, output_path=None):
    """
    Corta un segmento del video.
    
    Args:
        video_path: Path al video
        inicio: Tiempo de inicio en segundos o formato HH:MM:SS
        fin: Tiempo de fin en segundos o formato HH:MM:SS
        output_path: Path de salida
    
    Returns:
        Path del video cortado
    """
    video_path = Path(video_path)
    
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}_clip.mp4"
    else:
        output_path = Path(output_path)
    
    # Convertir a string si son números
    if isinstance(inicio, (int, float)):
        inicio = str(inicio)
    if isinstance(fin, (int, float)):
        fin = str(fin)
    
    cmd = [
        'ffmpeg', '-y',
        '-ss', inicio,
        '-to', fin,
        '-i', str(video_path),
        '-c:v', 'libx264', '-c:a', 'aac',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def concatenar_clips(clips_paths, output_path):
    """
    Concatena múltiples clips de video.
    
    Args:
        clips_paths: Lista de paths a los clips
        output_path: Path del video final
    
    Returns:
        Path del video concatenado
    """
    output_path = Path(output_path)
    
    # Crear archivo temporal con lista de clips
    list_file = output_path.parent / "clips_list.txt"
    with open(list_file, 'w') as f:
        for clip in clips_paths:
            f.write(f"file '{Path(clip).absolute()}'\n")
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(list_file),
        '-c', 'copy',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    list_file.unlink()  # Eliminar archivo temporal
    
    return output_path


def normalizar_audio_video(video_path, output_path=None, target_lufs=-14):
    """
    Normaliza el loudness del audio en el video.
    
    Args:
        video_path: Path al video
        output_path: Path de salida
        target_lufs: Target loudness en LUFS (default: -14)
    
    Returns:
        Path del video con audio normalizado
    """
    video_path = Path(video_path)
    
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}_normalized.mp4"
    else:
        output_path = Path(output_path)
    
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-af', f'loudnorm=I={target_lufs}:TP=-1.5:LRA=11',
        '-c:v', 'copy',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def reducir_ruido_basico(video_path, output_path=None):
    """
    Aplica reducción de ruido básica con filtros highpass/lowpass.
    
    Args:
        video_path: Path al video
        output_path: Path de salida
    
    Returns:
        Path del video con audio limpio
    """
    video_path = Path(video_path)
    
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}_clean.mp4"
    else:
        output_path = Path(output_path)
    
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-af', 'highpass=f=80,lowpass=f=12000,afftdn=nf=-25',
        '-c:v', 'copy',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def export_multi_ratio(video_path, output_dir, ratios=['16:9', '9:16', '1:1']):
    """
    Exporta el video en múltiples aspect ratios.
    
    Args:
        video_path: Path al video master
        output_dir: Directorio de salida
        ratios: Lista de ratios a generar
    
    Returns:
        dict con paths de cada variante: {ratio: path}
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = {}
    
    ratio_configs = {
        '16:9': ('scale=1920:1080', '1920x1080'),
        '9:16': ('crop=ih*9/16:ih,scale=1080:1920', '1080x1920'),
        '1:1': ('crop=min(iw\\,ih):min(iw\\,ih),scale=1080:1080', '1080x1080'),
        '4:5': ('crop=ih*4/5:ih,scale=1080:1350', '1080x1350')
    }
    
    for ratio in ratios:
        if ratio not in ratio_configs:
            continue
        
        vf, resolution = ratio_configs[ratio]
        output_path = output_dir / f"{video_path.stem}_{ratio.replace(':', 'x')}.mp4"
        
        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_path),
            '-vf', vf,
            '-c:a', 'copy',
            str(output_path)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        outputs[ratio] = output_path
    
    return outputs

