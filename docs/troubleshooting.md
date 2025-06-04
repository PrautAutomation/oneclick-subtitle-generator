# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 🐍 Python Issues

#### ❌ "Python is not recognized as an internal or external command"
**Solution:**
- Reinstall Python and check "Add Python to PATH" during installation
- Or manually add Python to PATH: `C:\Users\YOUR_USER\AppData\Local\Programs\Python\Python3X\`

#### ❌ "No module named 'tkinter'"
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (should be included)
# If missing, reinstall Python from python.org

# Windows (should be included)
# If missing, reinstall Python with tkinter option checked
```

### 📦 Installation Issues

#### ❌ "No module named 'librosa'" or other missing modules
**Solution:**
```bash
pip install -r requirements.txt
# Or individually:
pip install librosa soundfile torch torchaudio deep-translator ffmpeg-python
```

#### ❌ "whisper_online.py not found"
**Solution:**
1. Make sure you're in the correct directory:
   ```bash
   cd whisper_streaming
   ls  # Should show whisper_online.py
   ```
2. If missing, the installer didn't complete. Run:
   ```bash
   git clone https://github.com/ufal/whisper_streaming.git
   ```

#### ❌ "Git is not recognized"
**Solution:**
- Windows: Install Git from https://git-scm.com/download/win
- macOS: Install Xcode Command Line Tools: `xcode-select --install`
- Linux: `sudo apt install git` (Ubuntu/Debian) or equivalent

### 🎯 Whisper Backend Issues

#### ❌ "No module named 'mlx_whisper'" (Apple Silicon)
**Solution:**
```bash
pip install mlx-whisper
```

#### ❌ "No module named 'faster_whisper'" (Windows/Linux)
**Solution:**
```bash
pip install faster-whisper
```

#### ❌ "CUDA out of memory" (NVIDIA GPU)
**Solution:**
- Use smaller model: `--model medium` or `--model small`
- Close other GPU-intensive applications
- Use CPU backend: `--backend whisper_timestamped`

### 🎙️ Audio Processing Issues

#### ❌ "ffmpeg not found"
**Solution:**
- Windows: `pip install ffmpeg-python` should handle it
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

#### ❌ "Audio file not supported"
**Solution:**
- Supported formats: .wav, .mp3, .m4a, .flac, .ogg, .wma
- Convert unsupported formats using ffmpeg:
  ```bash
  ffmpeg -i input.avi -vn -acodec mp3 output.mp3
  ```

### 🌍 Translation Issues

#### ❌ "Translation failed" or empty translations
**Solution:**
1. Check internet connection
2. Install translation library:
   ```bash
   pip install deep-translator
   ```
3. For now, only English translation works fully. Other languages coming soon!

### ⚡ Performance Issues

#### ❌ Processing is very slow
**Solutions:**
1. Use smaller model:
   ```bash
   python enhanced_translator.py /path --model medium
   # Or even smaller:
   python enhanced_translator.py /path --model tiny
   ```

2. Process fewer languages:
   ```bash
   python enhanced_translator.py /path --languages cs en
   ```

3. Check system resources:
   - Close unnecessary applications
   - Ensure at least 4GB RAM available
   - For large files, use SSD instead of HDD

#### ❌ GUI freezes during processing
**Solution:**
- This is normal - processing happens in background
- Check the log window for progress
- Don't click multiple times - be patient

### 🖥️ Platform-Specific Issues

#### macOS: "App can't be opened because it is from an unidentified developer"
**Solution:**
- Right-click the app and select "Open"
- Or: System Preferences > Security & Privacy > "Open Anyway"

#### Windows: "Execution of scripts is disabled on this system"
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Linux: Permission denied
**Solution:**
```bash
chmod +x run_oneclick.sh
./run_oneclick.sh
```

### 📝 Output Issues

#### ❌ SRT files are not created
**Check:**
1. Look in the same folder as audio files
2. Check log for errors
3. Ensure write permissions in the folder

#### ❌ SRT files have wrong encoding
**Solution:**
- Files are saved as UTF-8
- Open with modern text editor (VS Code, Sublime Text)
- In VLC: Subtitles > Subtitle Track > Open File

### 🆘 Still Having Issues?

1. **Check the logs** - GUI shows detailed error messages
2. **Run in debug mode**:
   ```bash
   export ONECLICK_DEBUG=1
   python oneclick_subtitle_generator.py
   ```
3. **Report issue on GitHub**:
   - Include error message
   - Your OS and Python version
   - Steps to reproduce
   - https://github.com/PrautAutomation/oneclick-subtitle-generator/issues

### 💡 Pro Tips

1. **Test with small file first** - Use 1-2 minute audio
2. **Start with one language** - Add more once working
3. **Keep audio files under 1 hour** - Split longer files
4. **Use WAV for best quality** - Convert MP3 if issues
5. **Run from command line** - More detailed error messages
