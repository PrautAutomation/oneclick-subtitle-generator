# 📦 Installation Guide

## 🚀 Quick Installation (Recommended)

### Universal Installer (All Platforms)
```bash
curl -L https://github.com/YOUR_USERNAME/oneclick-subtitle-generator/releases/latest/download/install.py -o install.py
python install.py
```

### Platform-Specific Installers

#### 🪟 Windows
```powershell
# PowerShell (recommended)
irm https://github.com/YOUR_USERNAME/oneclick-subtitle-generator/releases/latest/download/install_windows.ps1 | iex

# Or using CMD
curl -L https://github.com/YOUR_USERNAME/oneclick-subtitle-generator/releases/latest/download/install_windows.bat -o install.bat && install.bat
```

#### 🍎 macOS
```bash
curl -fsSL https://github.com/YOUR_USERNAME/oneclick-subtitle-generator/releases/latest/download/install_macos.sh | bash
```

#### 🐧 Linux
```bash
curl -fsSL https://github.com/YOUR_USERNAME/oneclick-subtitle-generator/releases/latest/download/install_linux.sh | bash
```

## 📋 Prerequisites

### All Platforms
- **Python 3.8 or higher**
- **Git**
- **Internet connection** (for downloading models and dependencies)
- **4GB+ RAM** (8GB recommended)

### Platform-Specific Requirements

#### Windows
- Windows 10/11
- PowerShell 5.0+ or Command Prompt
- [Python from python.org](https://www.python.org/downloads/)

#### macOS
- macOS 10.15 (Catalina) or later
- Xcode Command Line Tools: `xcode-select --install`
- Homebrew (optional but recommended): [brew.sh](https://brew.sh)

#### Linux
- Ubuntu 20.04+, Debian 10+, CentOS 8+, or equivalent
- Python development headers: `python3-dev`
- FFmpeg: `sudo apt install ffmpeg`

## 🔧 Manual Installation

If automatic installation fails, follow these steps:

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/oneclick-subtitle-generator.git
cd oneclick-subtitle-generator
```

### 2. Clone Whisper Streaming
```bash
git clone https://github.com/ufal/whisper_streaming.git
```

### 3. Copy OneClick Files
```bash
cp src/*.py whisper_streaming/
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt

# Platform-specific Whisper backend
# Apple Silicon:
pip install mlx-whisper

# Others:
pip install faster-whisper
```

### 5. Test Installation
```bash
cd whisper_streaming
python oneclick_subtitle_generator.py
```

## 🐳 Docker Installation (Coming Soon)

```bash
docker pull YOUR_USERNAME/oneclick-subtitles
docker run -it -v /path/to/audio:/audio oneclick-subtitles
```

## 🔄 Updating

### Using Installer
```bash
# Just run the installer again
python install.py
```

### Manual Update
```bash
cd oneclick-subtitle-generator
git pull
cp src/*.py whisper_streaming/
pip install -r requirements.txt --upgrade
```

## ✅ Verify Installation

Run this test script:
```python
python -c "
import librosa
import soundfile
import torch
from deep_translator import GoogleTranslator
print('✅ All dependencies installed successfully!')
"
```

## 🗑️ Uninstallation

### Windows
```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\OneClick-Subtitles"
# Remove desktop shortcut
Remove-Item "$env:USERPROFILE\Desktop\OneClick Subtitles.lnk"
```

### macOS/Linux
```bash
rm -rf ~/OneClick-Subtitles
# Remove alias from .bashrc/.zshrc
```

## 🆘 Installation Failed?

See [Troubleshooting Guide](troubleshooting.md) or:
1. Check [GitHub Issues](https://github.com/YOUR_USERNAME/oneclick-subtitle-generator/issues)
2. Create new issue with:
   - Your OS and version
   - Python version: `python --version`
   - Error message
   - Installation method used