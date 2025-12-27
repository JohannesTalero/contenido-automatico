import os
import sys
import subprocess
import json
from pathlib import Path
import click
import torch
from faster_whisper import WhisperModel

# Intentar import relativo (para python -m src.ingest) o absoluto (para Colab)
try:
    from .utils import get_device_info, clear_gpu_memory
except ImportError:
    try:
        from src.utils import get_device_info, clear_gpu_memory
    except ImportError:
        # Fallback para ejecución directa si el path está mal configurado
        sys.path.append(str(Path(__file__).parent.parent))
        from src.utils import get_device_info, clear_gpu_memory

def transcribe_audio(audio_path):
    """
    Genera transcripción con timestamps a nivel de palabra usando faster-whisper.
    Usa GPU automáticamente si está disponible, con fallback a CPU si hay problemas.
    """
    device_info = get_device_info()
    device = device_info["device"]
    compute_type = device_info["compute_type"]
    
    # Limpiar memoria GPU antes de empezar
    clear_gpu_memory()
    
    if device == "cuda":
        click.echo(f"[*] Transcribiendo audio con faster-whisper (GPU: {device_info['gpu_name']})...")
    else:
        click.echo("[*] Transcribiendo audio con faster-whisper (CPU)...")
    
    # Usamos base para rapidez, se puede cambiar a small/medium para mejor calidad
    model_size = "base"
    
    # Intentar con GPU primero, si falla usar CPU
    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        segments, info = model.transcribe(str(audio_path), word_timestamps=True)
    except (RuntimeError, Exception) as e:
        if device == "cuda" and ("cublas" in str(e).lower() or "cuda" in str(e).lower()):
            click.echo(f"[!] Error con GPU: {e}")
            click.echo("[*] Cambiando a CPU para transcripción...")
            device = "cpu"
            compute_type = "int8"
            model = WhisperModel(model_size, device=device, compute_type=compute_type)
            segments, info = model.transcribe(str(audio_path), word_timestamps=True)
        else:
            raise
    
    words_data = []
    for segment in segments:
        for word in segment.words:
            words_data.append({
                "word": word.word,
                "start": word.start,
                "end": word.end,
                "probability": word.probability
            })
    
    # Limpiar memoria después de usar
    clear_gpu_memory()
            
    return words_data, info.language

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--start', default=None, help='Start time (HH:MM:SS or seconds)')
@click.option('--end', default=None, help='End time (HH:MM:SS or seconds)')
@click.option('--output_dir', default='output', help='Output directory')
@click.option('--narrative', default='Fail & Fix', help='Narrative type')
@click.option('--skip-clean', is_flag=True, help='Skip DeepFilterNet cleaning')
def ingest(input_file, start, end, output_dir, narrative, skip_clean):
    """
    Fase 0/1: Ingesta de video/audio, limpieza con DeepFilterNet, transcripción y recorte.
    """
    input_path = Path(input_file)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Extraer audio si es video
    audio_temp = out_path / f"{input_path.stem}_temp.wav"
    click.echo(f"[*] Extrayendo audio de {input_file}...")
    
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', str(input_path),
        '-vn', '-acodec', 'pcm_s16le', '-ar', '48000', '-ac', '1',
        str(audio_temp)
    ]
    subprocess.run(ffmpeg_cmd, check=True, capture_output=True)

    audio_to_transcribe = audio_temp

    # 2. Limpieza con DeepFilterNet (SIEMPRE se ejecuta si no se omite)
    audio_clean = None
    if not skip_clean:
        device_info = get_device_info()
        use_gpu = device_info["device"] == "cuda"
        limpieza_exitosa = False
        
        # Limpiar memoria GPU antes de DeepFilterNet
        clear_gpu_memory()
        
        from df.enhance import enhance, init_df, load_audio, save_audio
        import os
        
        # Intentar primero con GPU si está disponible
        if use_gpu:
            click.echo(f"[*] Limpiando audio con DeepFilterNet (GPU: {device_info['gpu_name']})...")
            try:
                model, df_state, _ = init_df()
                audio, info = load_audio(audio_temp, sr=df_state.sr())
                enhanced_audio = enhance(model, df_state, audio)
                limpieza_exitosa = True
                click.echo("[+] Limpieza completada en GPU")
            except RuntimeError as e:
                if "out of memory" in str(e).lower() or "cuda" in str(e).lower():
                    click.echo(f"[!] Error de memoria GPU: {e}")
                    click.echo("[*] Cambiando a CPU para limpieza...")
                    clear_gpu_memory()
                    try:
                        del model, df_state
                    except:
                        pass
                    torch.cuda.empty_cache()
                else:
                    click.echo(f"[!] Error en GPU: {e}")
                    click.echo("[*] Cambiando a CPU para limpieza...")
                    clear_gpu_memory()
                    try:
                        del model, df_state
                    except:
                        pass
        
        # Si no se usó GPU o falló, usar CPU
        if not limpieza_exitosa:
            click.echo("[*] Limpiando audio con DeepFilterNet (CPU)...")
            # Forzar CPU ocultando CUDA
            original_cuda_visible = os.environ.get('CUDA_VISIBLE_DEVICES')
            os.environ['CUDA_VISIBLE_DEVICES'] = ''
            
            try:
                model, df_state, _ = init_df()
                audio, info = load_audio(audio_temp, sr=df_state.sr())
                enhanced_audio = enhance(model, df_state, audio)
                limpieza_exitosa = True
                click.echo("[+] Limpieza completada en CPU")
            except Exception as cpu_error:
                click.echo(f"[!] Error crítico en limpieza (CPU): {cpu_error}")
                click.echo("[!] La limpieza de audio es obligatoria. Abortando...")
                raise
            finally:
                if original_cuda_visible is not None:
                    os.environ['CUDA_VISIBLE_DEVICES'] = original_cuda_visible
                elif 'CUDA_VISIBLE_DEVICES' in os.environ:
                    del os.environ['CUDA_VISIBLE_DEVICES']
        
        if limpieza_exitosa:
            audio_clean = out_path / f"{input_path.stem}_clean.wav"
            save_audio(audio_clean, enhanced_audio, df_state.sr())
            audio_to_transcribe = audio_clean
            clear_gpu_memory()
        else:
            raise RuntimeError("La limpieza de audio falló y es obligatoria")
    else:
        audio_clean = audio_temp

    # 3. Transcripción con faster-whisper
    words, lang = transcribe_audio(audio_to_transcribe)

    # 4. Recorte
    video_cut = out_path / f"{input_path.stem}_cut.mp4"
    if start or end:
        click.echo(f"[*] Recortando video: {start or '0'} -> {end or 'fin'}...")
        cut_cmd = ['ffmpeg', '-y']
        if start:
            cut_cmd += ['-ss', start]
        cut_cmd += ['-i', str(input_path)]
        if end:
            cut_cmd += ['-to', end]
        cut_cmd += ['-c:v', 'copy', '-c:a', 'copy', str(video_cut)]
        subprocess.run(cut_cmd, check=True, capture_output=True)
    else:
        click.echo("[!] No se especificó recorte. Copiando video original...")
        video_cut = out_path / f"{input_path.stem}_orig.mp4"
        import shutil
        shutil.copy2(input_path, video_cut)

    # 5. Generar JSON de metadatos
    metadata = {
        "source": str(input_path),
        "language": lang,
        "clean_audio": str(audio_clean) if audio_clean else str(audio_temp),
        "cut_video": str(video_cut),
        "narrativa": narrative,
        "tipo_debate": "tecnico",
        "segments": [
            {
                "start": start or "00:00:00",
                "end": end or "fin",
                "label": "SUCCESS"
            }
        ],
        "palabras": words
    }
    
    json_path = out_path / f"{input_path.stem}_meta.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    if not skip_clean and audio_temp.exists() and audio_clean and audio_temp != audio_clean:
        os.remove(audio_temp)

    click.echo(f"[+] Proceso completado. Resultados en: {output_dir}")

if __name__ == '__main__':
    ingest()
