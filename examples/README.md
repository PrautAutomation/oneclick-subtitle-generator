# 📁 Examples

This directory contains example files for testing OneClick Subtitle Generator.

## 🎵 Sample Audio Files

Due to copyright restrictions, we cannot include actual audio files. Please use your own audio files for testing.

### Recommended Test Files:
1. **Short clip** (30-60 seconds) - For quick testing
2. **Medium file** (5-10 minutes) - For performance testing  
3. **Multiple files** - For batch processing testing

### Where to Get Test Audio:
- Your own recordings
- Royalty-free audio from [Freesound.org](https://freesound.org)
- YouTube Audio Library (for YouTube creators)
- Generated speech using text-to-speech

## 📝 Expected Output Structure

When you process `example.mp3`, you should get:
```
example_cs.srt  # Czech (original)
example_en.srt  # English
example_es.srt  # Spanish
example_zh.srt  # Chinese
example_ru.srt  # Russian
example_de.srt  # German
example_fr.srt  # French
example_id.srt  # Indonesian
```

## 🧪 Testing Commands

### Basic Test
```bash
python enhanced_translator.py /path/to/audio --languages cs en
```

### Full Test
```bash
python enhanced_translator.py /path/to/audio
```

### Performance Test
```bash
python enhanced_translator.py /path/to/audio --model tiny --languages cs en
```