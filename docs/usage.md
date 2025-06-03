# Process all audio files in folder with default settings
python enhanced_translator.py /path/to/audio

# Specific languages only
python enhanced_translator.py /path/to/audio --languages cs en es

# Different model for speed vs quality
python enhanced_translator.py /path/to/audio --model medium

# Different backend
python enhanced_translator.py /path/to/audio --backend faster-whisper