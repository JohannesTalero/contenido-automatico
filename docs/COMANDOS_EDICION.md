# Comandos de Edición - FFmpeg y MoviePy

Referencia rápida de comandos para las operaciones más comunes en el flujo de edición.

---

## 1. Cortes y Recortes

### FFmpeg

```bash
# Extraer clip desde inicio hasta fin (sin recodificar - rápido)
ffmpeg -ss 00:01:30 -to 00:02:45 -i input.mp4 -c copy output_clip.mp4

# Extraer clip con recodificación (más preciso en los cortes)
ffmpeg -ss 00:01:30 -to 00:02:45 -i input.mp4 -c:v libx264 -c:a aac output_clip.mp4

# Extraer múltiples clips y concatenar
# Primero crear archivo clips.txt con:
# file 'clip1.mp4'
# file 'clip2.mp4'
# file 'clip3.mp4'
ffmpeg -f concat -safe 0 -i clips.txt -c copy output_final.mp4
```

### MoviePy

```python
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Cargar video
video = VideoFileClip("input.mp4")

# Extraer subclip (segundos)
clip1 = video.subclip(90, 165)  # 1:30 a 2:45

# Concatenar múltiples clips
clips = [
    video.subclip(10, 30),
    video.subclip(45, 60),
    video.subclip(120, 180)
]
final = concatenate_videoclips(clips)
final.write_videofile("output.mp4")
```

---

## 2. Eliminación de Silencios

### FFmpeg (detección de silencios)

```bash
# Detectar silencios (silencio = -30dB por más de 0.5s)
ffmpeg -i input.mp4 -af silencedetect=noise=-30dB:d=0.5 -f null - 2>&1 | grep silence

# Salida ejemplo:
# [silencedetect] silence_start: 10.5
# [silencedetect] silence_end: 12.3 | silence_duration: 1.8
```

### Python - Remover silencios automáticamente

```python
from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np

def detect_silence(audio_clip, threshold=0.01, chunk_duration=0.1):
    """Detecta segmentos de silencio en el audio."""
    silences = []
    duration = audio_clip.duration
    current_time = 0
    
    while current_time < duration:
        end_time = min(current_time + chunk_duration, duration)
        chunk = audio_clip.subclip(current_time, end_time)
        # Obtener volumen promedio del chunk
        samples = chunk.to_soundarray()
        volume = np.abs(samples).mean()
        
        if volume < threshold:
            silences.append((current_time, end_time))
        current_time = end_time
    
    return silences

def remove_long_silences(video_path, min_silence_duration=0.8, output_path="output.mp4"):
    """Remueve silencios mayores a min_silence_duration segundos."""
    video = VideoFileClip(video_path)
    silences = detect_silence(video.audio)
    
    # Agrupar silencios consecutivos
    # ... (lógica de agrupación)
    
    # Crear clips excluyendo silencios largos
    # ... (lógica de corte)
    
    final.write_videofile(output_path)
```

---

## 3. Audio - Normalización y Limpieza

### FFmpeg - Normalizar Loudness

```bash
# Normalizar a -14 LUFS (estándar streaming)
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v copy output.mp4

# Análisis de loudness primero (2-pass para mejor resultado)
# Pass 1: Analizar
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -

# Pass 2: Aplicar con valores medidos
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-23:measured_TP=-2:measured_LRA=8:measured_thresh=-34:offset=0.5:linear=true -c:v copy output.mp4
```

### FFmpeg - Reducción de Ruido

```bash
# Paso 1: Extraer muestra de ruido (segmento de silencio con ruido de fondo)
ffmpeg -i input.mp4 -ss 00:00:01 -t 00:00:02 -vn noise_sample.wav

# Paso 2: Crear perfil de ruido con sox
sox noise_sample.wav -n noiseprof noise.prof

# Paso 3: Aplicar reducción de ruido
ffmpeg -i input.mp4 -af "afftdn=nf=-25" -c:v copy output_clean.mp4

# Alternativa: highpass + lowpass para voz
ffmpeg -i input.mp4 -af "highpass=f=80,lowpass=f=12000" -c:v copy output.mp4
```

### FFmpeg - Ajustar Volumen

```bash
# Aumentar volumen 50%
ffmpeg -i input.mp4 -af "volume=1.5" -c:v copy output.mp4

# Aumentar 6dB
ffmpeg -i input.mp4 -af "volume=6dB" -c:v copy output.mp4

# Normalización simple (peak normalization)
ffmpeg -i input.mp4 -af "dynaudnorm" -c:v copy output.mp4
```

### MoviePy - Audio

```python
from moviepy.editor import VideoFileClip

video = VideoFileClip("input.mp4")

# Ajustar volumen
video = video.volumex(1.5)  # 150% del volumen original

# Fade in/out de audio
video = video.audio_fadein(1).audio_fadeout(1)

video.write_videofile("output.mp4")
```

---

## 4. Video - Correcciones Básicas

### FFmpeg - Color y Brillo

```bash
# Ajustar brillo y contraste
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:contrast=1.2" output.mp4

# Ajustar saturación
ffmpeg -i input.mp4 -vf "eq=saturation=1.3" output.mp4

# Corrección de color completa
ffmpeg -i input.mp4 -vf "eq=brightness=0.05:contrast=1.1:saturation=1.2:gamma=1.1" output.mp4
```

### FFmpeg - Escalar y Crop

```bash
# Escalar a 1080p manteniendo aspect ratio
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4

# Crop para 9:16 (vertical) desde centro
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih" output_vertical.mp4

# Crop para 1:1 (cuadrado) desde centro
ffmpeg -i input.mp4 -vf "crop=min(iw\,ih):min(iw\,ih)" output_square.mp4
```

---

## 5. Transiciones y Efectos

### MoviePy - Transiciones

```python
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip

clip1 = VideoFileClip("clip1.mp4")
clip2 = VideoFileClip("clip2.mp4")

# Fade out del primero, fade in del segundo
clip1 = clip1.fadeout(0.5)
clip2 = clip2.fadein(0.5)

# Crossfade entre clips
clip1 = clip1.crossfadeout(1)
clip2 = clip2.crossfadein(1)

# Concatenar con crossfade
final = concatenate_videoclips([clip1, clip2], method="compose")
final.write_videofile("output.mp4")
```

### FFmpeg - Fade In/Out

```bash
# Fade in de video (primeros 2 segundos)
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=2" -c:a copy output.mp4

# Fade out de video (últimos 2 segundos)
ffmpeg -i input.mp4 -vf "fade=t=out:st=58:d=2" -c:a copy output.mp4

# Fade in de audio
ffmpeg -i input.mp4 -af "afade=t=in:st=0:d=2" -c:v copy output.mp4

# Combinar fade de video y audio
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=2,fade=t=out:st=58:d=2" -af "afade=t=in:st=0:d=2,afade=t=out:st=58:d=2" output.mp4
```

---

## 6. Export Final

### FFmpeg - Export de Alta Calidad

```bash
# Export para YouTube/Web (H.264)
ffmpeg -i input.mp4 \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 320k \
  -movflags +faststart \
  output_final.mp4

# Export para archiving (ProRes - muy pesado pero sin pérdida)
ffmpeg -i input.mp4 \
  -c:v prores_ks -profile:v 3 \
  -c:a pcm_s16le \
  output_master.mov
```

### FFmpeg - Export Multi-Ratio

```bash
# 16:9 (horizontal)
ffmpeg -i master.mp4 -vf "scale=1920:1080" -c:a copy output_16x9.mp4

# 9:16 (vertical - TikTok/Reels)
ffmpeg -i master.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:a copy output_9x16.mp4

# 1:1 (cuadrado - Instagram)
ffmpeg -i master.mp4 -vf "crop=min(iw\,ih):min(iw\,ih),scale=1080:1080" -c:a copy output_1x1.mp4

# 4:5 (Instagram feed)
ffmpeg -i master.mp4 -vf "crop=ih*4/5:ih,scale=1080:1350" -c:a copy output_4x5.mp4
```

### MoviePy - Export

```python
from moviepy.editor import VideoFileClip

video = VideoFileClip("input.mp4")

# Export con configuración específica
video.write_videofile(
    "output.mp4",
    codec="libx264",
    audio_codec="aac",
    bitrate="10M",
    fps=30,
    preset="slow",
    threads=4
)

# Export solo audio
video.audio.write_audiofile("audio.mp3")
```

---

## 7. Utilidades

### Obtener Información del Video

```bash
# Info completa
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Solo duración
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4
```

### Extraer Audio

```bash
# Extraer audio como WAV
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 48000 output.wav

# Extraer audio como MP3
ffmpeg -i input.mp4 -vn -acodec libmp3lame -b:a 320k output.mp3
```

### Agregar Audio a Video

```bash
# Reemplazar audio
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 output.mp4

# Mezclar audio original con música de fondo
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[a]" -map 0:v -map "[a]" -c:v copy output.mp4
```

---

## Notas

- Siempre hacer backup del archivo original antes de editar
- `-c copy` = sin recodificar (rápido pero menos preciso en cortes)
- `-c:v libx264` = recodificar video (más lento pero preciso)
- CRF más bajo = mejor calidad, archivo más grande (18-23 recomendado)
- Para MoviePy: cerrar clips con `clip.close()` para liberar memoria

