#!/usr/bin/env python3
"""
OneClick Subtitle Generator - Utility Functions
"""

import os
import platform
import subprocess
import tempfile
from datetime import timedelta
from pathlib import Path
import logging

def setup_logging(level="INFO"):
    """Nastavení loggingu"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    return logging.getLogger(__name__)

def ms_to_srt_time(milliseconds):
    """Převede milisekundy na SRT časový formát (HH:MM:SS,mmm)"""
    td = timedelta(milliseconds=milliseconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    ms = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"

def detect_audio_files(folder_path, extensions=None):
    """Najde všechny audio soubory ve složce"""
    if extensions is None:
        extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.wma', '.aac']
    
    audio_files = []
    folder = Path(folder_path)
    
    if not folder.exists():
        return []
    
    for ext in extensions:
        audio_files.extend(folder.glob(f"*{ext}"))
        audio_files.extend(folder.glob(f"*{ext.upper()}"))
    
    return sorted(audio_files)

def get_platform_info():
    """Vrátí informace o platformě"""
    return {
        'system': platform.system(),
        'release': platform.release(), 
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'platform': platform.platform()
    }

def detect_optimal_backend():
    """Detekuje optimální Whisper backend pro aktuální platformu"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin" and machine in ["arm64", "aarch64"]:
        return "mlx-whisper", "Apple Silicon optimized"
    elif system in ["windows", "linux"] or (system == "darwin" and machine != "arm64"):
        return "faster-whisper", "GPU accelerated"
    else:
        return "whisper_timestamped", "Universal CPU"

def format_duration(seconds):
    """Formátuje čas v sekundách na čitelný formát"""
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def estimate_processing_time(audio_duration_seconds, num_languages=8, model="large-v3"):
    """Odhadne čas zpracování na základě délky audia a hardwaru"""
    platform_info = get_platform_info()
    
    # Multiplikátory podle modelu
    model_multipliers = {
        'tiny': 0.03,
        'base': 0.06,
        'small': 0.17,
        'medium': 0.5,
        'large-v2': 1.0,
        'large-v3': 1.0
    }
    
    # Multiplikátory podle platformy
    if platform_info['system'] == 'Darwin' and 'arm' in platform_info['machine'].lower():
        platform_multiplier = 0.15  # Apple Silicon
    elif platform_info['system'] == 'Windows':
        platform_multiplier = 0.25  # Windows s možnou GPU
    else:
        platform_multiplier = 0.3   # Linux/ostatní
    
    base_time = audio_duration_seconds * model_multipliers.get(model, 1.0) * platform_multiplier
    total_time = base_time * num_languages
    
    return total_time

def ensure_directory(path):
    """Zajistí, že adresář existuje"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

def clean_filename(filename):
    """Vyčistí název souboru od problematických znaků"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

def get_file_size_mb(file_path):
    """Vrátí velikost souboru v MB"""
    try:
        size_bytes = Path(file_path).stat().st_size
        return round(size_bytes / (1024 * 1024), 2)
    except:
        return 0

def check_disk_space(path, required_mb=1000):
    """Zkontroluje dostupné místo na disku"""
    try:
        import shutil
        total, used, free = shutil.disk_usage(path)
        free_mb = free // (1024 * 1024)
        return free_mb >= required_mb, free_mb
    except:
        return True, 0  # Pokud nejde zjistit, předpokládáme OK

def validate_audio_file(file_path):
    """Validuje audio soubor"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        return False, "Soubor neexistuje"
    
    if file_path.suffix.lower() not in ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.wma', '.aac']:
        return False, "Nepodporovaný formát"
    
    if file_path.stat().st_size == 0:
        return False, "Prázdný soubor"
    
    # Další validace zde...
    return True, "OK"

def get_audio_duration(file_path):
    """Získá délku audio souboru"""
    try:
        import librosa
        duration = librosa.get_duration(filename=str(file_path))
        return duration
    except:
        return 0

def check_dependencies():
    """Zkontroluje dostupnost potřebných závislostí"""
    dependencies = {
        'librosa': False,
        'soundfile': False,
        'torch': False,
        'deep_translator': False
    }
    
    for dep in dependencies:
        try:
            __import__(dep)
            dependencies[dep] = True
        except ImportError:
            pass
    
    return dependencies

def check_whisper_backend(backend_name):
    """Zkontroluje dostupnost Whisper backendu"""
    try:
        if backend_name == "mlx-whisper":
            import mlx_whisper
        elif backend_name == "faster-whisper":
            import faster_whisper
        elif backend_name == "whisper_timestamped":
            import whisper_timestamped
        return True
    except ImportError:
        return False

def create_srt_content(transcript_data):
    """Vytvoří obsah SRT souboru z transkripčních dat"""
    srt_content = []
    
    for i, (start_ms, end_ms, text) in enumerate(transcript_data, 1):
        start_time = ms_to_srt_time(start_ms)
        end_time = ms_to_srt_time(end_ms)
        
        srt_content.append(f"{i}")
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(text.strip())
        srt_content.append("")  # Prázdný řádek
    
    return "\n".join(srt_content)

def save_srt_file(transcript_data, output_path):
    """Uloží SRT soubor"""
    try:
        srt_content = create_srt_content(transcript_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        return True, f"SRT soubor uložen: {output_path}"
    except Exception as e:
        return False, f"Chyba při ukládání SRT: {str(e)}"

def progress_callback(current, total, message=""):
    """Callback funkce pro zobrazení postupu"""
    if total > 0:
        percentage = (current / total) * 100
        print(f"\r[{percentage:6.2f}%] {message}", end="", flush=True)
    else:
        print(f"\r{message}", end="", flush=True)

def batch_process_status(current_file, total_files, current_lang, total_langs, file_name):
    """Zobrazí stav batch zpracování"""
    file_progress = (current_file / total_files) * 100
    lang_progress = (current_lang / total_langs) * 100
    
    print(f"📄 [{current_file}/{total_files}] {file_name}")
    print(f"🌍 [{current_lang}/{total_langs}] Jazyk: {lang_progress:.1f}%")
    print(f"📊 Celkový postup: {file_progress:.1f}%")

# Utility pro testování
if __name__ == "__main__":
    print("🔧 OneClick Subtitle Generator - Utils Test")
    print("=" * 50)
    
    # Test platform detection
    platform_info = get_platform_info()
    print(f"Platform: {platform_info}")
    
    # Test backend detection
    backend, description = detect_optimal_backend()
    print(f"Optimal backend: {backend} ({description})")
    
    # Test dependencies
    deps = check_dependencies()
    print(f"Dependencies: {deps}")
    
    # Test time formatting
    print(f"Duration format: {format_duration(3725)}")  # 1h 2m 5s
    
    # Test SRT time format
    print(f"SRT time: {ms_to_srt_time(125000)}")  # 00:02:05,000
    
    print("✅ Utils test completed")