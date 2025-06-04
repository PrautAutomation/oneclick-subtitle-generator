#!/usr/bin/env python3
"""
OneClick Subtitle Generator - Configuration
"""

import platform
import os
from pathlib import Path

# Version information
VERSION = "1.0.0"
APP_NAME = "OneClick Subtitle Generator"
REPO_URL = "https://github.com/PrautAutomation/oneclick-subtitle-generator"

# Supported languages for subtitle generation
LANGUAGES = {
    'cs': 'Čeština',
    'en': 'English', 
    'es': 'Español',
    'zh': '中文',
    'ru': 'Русский',
    'de': 'Deutsch',
    'fr': 'Français',
    'id': 'Indonesian'
}

# Google Translate language codes mapping
GOOGLE_TRANSLATE_CODES = {
    'cs': 'cs',
    'en': 'en',
    'es': 'es', 
    'zh': 'zh',
    'ru': 'ru',
    'de': 'de',
    'fr': 'fr',
    'id': 'id'
}

# Supported audio file extensions
AUDIO_EXTENSIONS = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.wma', '.aac']

# Whisper model options
WHISPER_MODELS = [
    'tiny',    # ~39 MB, ~32x realtime
    'base',    # ~74 MB, ~16x realtime
    'small',   # ~244 MB, ~6x realtime
    'medium',  # ~769 MB, ~2x realtime
    'large-v2', # ~1550 MB, ~1x realtime
    'large-v3', # ~1550 MB, ~1x realtime (improved)
    'large-v3-turbo'  # ~809 MB, ~8x realtime (faster large)
]

# Default settings
DEFAULT_MODEL = "large-v3"
DEFAULT_MIN_CHUNK_SIZE = 1
DEFAULT_BUFFER_TRIMMING_SEC = 15

# Platform detection and backend selection
def detect_platform():
    """Detects the current platform and returns optimized backend"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin" and machine in ["arm64", "aarch64"]:
        return "macos_silicon"
    elif system == "darwin":
        return "macos_intel"
    elif system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def get_optimal_backend():
    """Returns the optimal Whisper backend for current platform"""
    platform_type = detect_platform()
    
    if platform_type == "macos_silicon":
        return "mlx-whisper"
    else:
        return "faster-whisper"

# Backend configurations
BACKENDS = {
    'mlx-whisper': {
        'name': 'MLX Whisper',
        'description': 'Optimized for Apple Silicon (M1/M2/M3)',
        'platforms': ['macos_silicon'],
        'install_command': 'pip install mlx-whisper',
        'supports_gpu': True
    },
    'faster-whisper': {
        'name': 'Faster Whisper', 
        'description': 'GPU-accelerated, good for NVIDIA cards',
        'platforms': ['windows', 'linux', 'macos_intel'],
        'install_command': 'pip install faster-whisper',
        'supports_gpu': True
    },
    'whisper_timestamped': {
        'name': 'Whisper Timestamped',
        'description': 'CPU-only, universal compatibility',
        'platforms': ['all'],
        'install_command': 'pip install git+https://github.com/linto-ai/whisper-timestamped',
        'supports_gpu': False
    },
    'openai-api': {
        'name': 'OpenAI API',
        'description': 'Cloud-based, requires API key and internet',
        'platforms': ['all'],
        'install_command': 'pip install openai',
        'supports_gpu': False,
        'requires_api_key': True
    }
}

# Default backend based on platform
DEFAULT_BACKEND = get_optimal_backend()

# File paths and directories
def get_app_data_dir():
    """Returns the application data directory"""
    if platform.system() == "Windows":
        return Path(os.environ.get("APPDATA", "")) / APP_NAME
    elif platform.system() == "Darwin":
        return Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        return Path.home() / f".{APP_NAME.lower().replace(' ', '-')}"

def get_cache_dir():
    """Returns the cache directory"""
    app_data = get_app_data_dir()
    return app_data / "cache"

def get_models_dir():
    """Returns the models cache directory"""
    cache_dir = get_cache_dir()
    return cache_dir / "models"

# GUI settings
GUI_SETTINGS = {
    'window_size': '800x600',
    'window_title': f'{APP_NAME} v{VERSION}',
    'theme': 'default',
    'font_size': 10,
    'log_max_lines': 1000
}

# Processing settings
PROCESSING_SETTINGS = {
    'max_workers': 4,  # For parallel processing
    'timeout_seconds': 3600,  # 1 hour timeout per file
    'retry_attempts': 3,
    'chunk_overlap_seconds': 1,
    'vad_threshold': 0.5,
    'energy_threshold': 300
}

# Translation settings
TRANSLATION_SETTINGS = {
    'batch_size': 10,  # Segments to translate at once
    'max_text_length': 500,  # Max characters per translation request
    'timeout_seconds': 30,  # Timeout per translation request
    'retry_attempts': 3,
    'rate_limit_delay': 0.1  # Delay between requests to avoid rate limiting
}

# Output settings
OUTPUT_SETTINGS = {
    'srt_encoding': 'utf-8',
    'srt_line_length': 42,  # Max characters per subtitle line
    'srt_max_duration': 7,  # Max seconds per subtitle
    'srt_min_duration': 1,  # Min seconds per subtitle
    'timestamp_precision': 3  # Decimal places for timestamps
}

# Debug and logging
DEBUG_MODE = os.environ.get('ONECLICK_DEBUG', '').lower() in ['1', 'true', 'yes']
LOG_LEVEL = os.environ.get('ONECLICK_LOG_LEVEL', 'INFO').upper()

# Environment variables for configuration
def get_env_or_default(key, default):
    """Get environment variable or return default"""
    return os.environ.get(f'ONECLICK_{key}', default)

# Override defaults with environment variables
DEFAULT_MODEL = get_env_or_default('MODEL', DEFAULT_MODEL)
DEFAULT_BACKEND = get_env_or_default('BACKEND', DEFAULT_BACKEND)

# Validation functions
def validate_model(model):
    """Validates if model is supported"""
    return model in WHISPER_MODELS

def validate_backend(backend):
    """Validates if backend is supported"""
    return backend in BACKENDS

def validate_language(language):
    """Validates if language is supported"""
    return language in LANGUAGES

def validate_audio_file(file_path):
    """Validates if file is supported audio format"""
    file_path = Path(file_path)
    return file_path.suffix.lower() in AUDIO_EXTENSIONS

# Configuration validation
def validate_config():
    """Validates current configuration"""
    errors = []
    
    if not validate_model(DEFAULT_MODEL):
        errors.append(f"Invalid default model: {DEFAULT_MODEL}")
    
    if not validate_backend(DEFAULT_BACKEND):
        errors.append(f"Invalid default backend: {DEFAULT_BACKEND}")
    
    return errors

# Initialize app directories
def init_app_directories():
    """Creates necessary application directories"""
    directories = [
        get_app_data_dir(),
        get_cache_dir(),
        get_models_dir()
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Platform-specific settings
PLATFORM_SETTINGS = {
    'macos_silicon': {
        'preferred_backend': 'mlx-whisper',
        'memory_efficient': True,
        'gpu_acceleration': True
    },
    'macos_intel': {
        'preferred_backend': 'faster-whisper',
        'memory_efficient': False,
        'gpu_acceleration': False
    },
    'windows': {
        'preferred_backend': 'faster-whisper',
        'memory_efficient': False,
        'gpu_acceleration': True
    },
    'linux': {
        'preferred_backend': 'faster-whisper', 
        'memory_efficient': False,
        'gpu_acceleration': True
    }
}

def get_platform_settings():
    """Returns settings for current platform"""
    platform_type = detect_platform()
    return PLATFORM_SETTINGS.get(platform_type, PLATFORM_SETTINGS['linux'])

# Export main configuration
CONFIG = {
    'version': VERSION,
    'app_name': APP_NAME,
    'repo_url': REPO_URL,
    'languages': LANGUAGES,
    'audio_extensions': AUDIO_EXTENSIONS,
    'whisper_models': WHISPER_MODELS,
    'default_model': DEFAULT_MODEL,
    'default_backend': DEFAULT_BACKEND,
    'backends': BACKENDS,
    'gui_settings': GUI_SETTINGS,
    'processing_settings': PROCESSING_SETTINGS,
    'translation_settings': TRANSLATION_SETTINGS,
    'output_settings': OUTPUT_SETTINGS,
    'platform_settings': get_platform_settings(),
    'debug_mode': DEBUG_MODE,
    'log_level': LOG_LEVEL
}

if __name__ == "__main__":
    # Test configuration
    print(f"OneClick Subtitle Generator Configuration")
    print(f"Version: {VERSION}")
    print(f"Platform: {detect_platform()}")
    print(f"Optimal Backend: {get_optimal_backend()}")
    print(f"Supported Languages: {list(LANGUAGES.keys())}")
    
    # Validate configuration
    errors = validate_config()
    if errors:
        print(f"Configuration errors: {errors}")
    else:
        print("Configuration is valid")
    
    # Initialize directories
    init_app_directories()
    print(f"App data directory: {get_app_data_dir()}")