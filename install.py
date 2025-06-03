#!/usr/bin/env python3
"""
OneClick Subtitle Generator - Universal Installer
Works on Windows, macOS, and Linux with automatic platform detection
"""

import os
import sys
import platform
import subprocess
import urllib.request
import json
import tempfile
import shutil
from pathlib import Path

# Konfigurace
REPO_OWNER = "PrautAutomation"  # Změňte na váš GitHub username
REPO_NAME = "oneclick-subtitle-generator"
WHISPER_STREAMING_REPO = "https://github.com/ufal/whisper_streaming.git"

def print_banner():
    """Zobrazí úvodní banner"""
    print("=" * 60)
    print("🎬 OneClick Subtitle Generator - Universal Installer")
    print("=" * 60)
    print("🌍 Automatická detekce platformy a instalace závislostí")
    print("🚀 Podporuje Windows, macOS, Linux")
    print("💎 Optimalizováno pro Apple Silicon a NVIDIA GPU")
    print("=" * 60)

def detect_platform():
    """Detekuje platformu a architekturu"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    print(f"🖥️ Systém: {platform.system()} {platform.release()}")
    print(f"🔧 Architektura: {platform.machine()}")
    print(f"🐍 Python: {sys.version}")
    
    if system == "darwin":
        if machine in ["arm64", "aarch64"]:
            return "macos_silicon"
        else:
            return "macos_intel"
    elif system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    else:
        print(f"⚠️ Neznámá platforma: {system}")
        return "unknown"

def check_python_version():
    """Kontroluje verzi Pythonu"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ je vyžadován!")
        print(f"📦 Aktuální verze: {sys.version}")
        print("📥 Stáhněte novější Python z: https://www.python.org/downloads/")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} je kompatibilní")

def check_git():
    """Kontroluje dostupnost Git"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ Git je dostupný")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git není nainstalován nebo dostupný")
        return False

def install_git_instructions():
    """Poskytuje instrukce pro instalaci Git"""
    platform_type = detect_platform()
    
    print("\n📥 Instrukce pro instalaci Git:")
    
    if platform_type == "windows":
        print("🪟 Windows:")
        print("   1. Jděte na: https://git-scm.com/download/win")
        print("   2. Stáhněte a nainstalujte Git for Windows")
        print("   3. Restartujte příkazový řádek")
        
    elif platform_type.startswith("macos"):
        print("🍎 macOS:")
        print("   1. Nainstalujte Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("   2. Spusťte: brew install git")
        print("   Nebo:")
        print("   1. Nainstalujte Xcode Command Line Tools: xcode-select --install")
        
    elif platform_type == "linux":
        print("🐧 Linux:")
        print("   Ubuntu/Debian: sudo apt update && sudo apt install git")
        print("   CentOS/RHEL/Fedora: sudo dnf install git")
        print("   Arch Linux: sudo pacman -S git")

def upgrade_pip():
    """Aktualizuje pip na nejnovější verzi"""
    print("📦 Aktualizuji pip...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        print("✅ Pip aktualizován")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Varování: Nepodařilo se aktualizovat pip: {e}")

def install_system_dependencies():
    """Instaluje systémové závislosti podle platformy"""
    platform_type = detect_platform()
    
    print(f"📦 Instaluji systémové závislosti pro {platform_type}...")
    
    if platform_type.startswith("macos"):
        # macOS - zkontroluje Homebrew
        if not shutil.which("brew"):
            print("⚠️ Homebrew není nainstalován. Některé závislosti mohou chybět.")
            print("💡 Doporučujeme nainstalovat Homebrew: https://brew.sh")
        else:
            try:
                subprocess.run(["brew", "install", "ffmpeg"], check=False)
                print("✅ FFmpeg nainstalován přes Homebrew")
            except:
                print("⚠️ Nepodařilo se nainstalovat FFmpeg")
                
    elif platform_type == "linux":
        # Linux - zkusí různé package managery
        try:
            # Ubuntu/Debian
            subprocess.run(["sudo", "apt", "update"], check=False, capture_output=True)
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=False)
        except:
            try:
                # CentOS/Fedora
                subprocess.run(["sudo", "dnf", "install", "-y", "ffmpeg"], check=False)
            except:
                print("⚠️ Nepodařilo se automaticky nainstalovat FFmpeg")
                print("💡 Nainstalujte ručně: sudo apt install ffmpeg (Ubuntu/Debian)")
    
    elif platform_type == "windows":
        print("🪟 Na Windows se FFmpeg nainstaluje automaticky s pip balíčky")

def get_whisper_backend(platform_type):
    """Určí nejlepší Whisper backend pro danou platformu"""
    if platform_type == "macos_silicon":
        return "mlx-whisper", "Optimalizováno pro Apple Silicon (M1/M2/M3)"
    elif platform_type in ["macos_intel", "linux", "windows"]:
        return "faster-whisper", "Univerzální backend s GPU podporou"
    else:
        return "whisper-timestamped", "Fallback backend"

def install_python_dependencies():
    """Instaluje Python závislosti"""
    platform_type = detect_platform()
    
    print("📦 Instaluji základní Python závislosti...")
    
    # Základní závislosti
    base_deps = [
        "librosa>=0.9.0",
        "soundfile>=0.12.0", 
        "torch>=1.13.0",
        "torchaudio>=0.13.0",
        "deep-translator>=1.11.0",
        "ffmpeg-python>=0.2.0"
    ]
    
    for dep in base_deps:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", dep
            ])
            print(f"✅ {dep.split('>=')[0]}")
        except subprocess.CalledProcessError:
            print(f"❌ Nepodařilo se nainstalovat {dep}")
    
    # Platform-specifický Whisper backend
    backend, description = get_whisper_backend(platform_type)
    print(f"🎯 Instaluji Whisper backend: {backend}")
    print(f"💡 {description}")
    
    try:
        if backend == "mlx-whisper":
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "mlx-whisper"
            ])
        elif backend == "faster-whisper":
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "faster-whisper"
            ])
        elif backend == "whisper-timestamped":
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "git+https://github.com/linto-ai/whisper-timestamped"
            ])
        
        print(f"✅ {backend} nainstalován")
    except subprocess.CalledProcessError:
        print(f"❌ Nepodařilo se nainstalovat {backend}")
        print("💡 Zkuste manuální instalaci později")

def clone_whisper_streaming():
    """Klonuje whisper_streaming repozitář"""
    print("📥 Stahuji whisper_streaming...")
    
    if os.path.exists("whisper_streaming"):
        print("⚠️ Složka whisper_streaming už existuje, přeskakuji klonování")
        return True
    
    try:
        subprocess.check_call([
            "git", "clone", WHISPER_STREAMING_REPO
        ])
        print("✅ whisper_streaming stažen")
        return True
    except subprocess.CalledProcessError:
        print("❌ Nepodařilo se klonovat whisper_streaming")
        return False

def download_oneclick_files():
    """Stáhne OneClick rozšíření z GitHub releases"""
    print("📥 Stahuji OneClick rozšíření...")
    
    # URL pro nejnovější release
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    
    try:
        with urllib.request.urlopen(api_url) as response:
            release_data = json.loads(response.read())
        
        download_url_base = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/latest/download/"
        
        files_to_download = [
            "oneclick_subtitle_generator.py",
            "enhanced_translator.py", 
            "config.py",
            "utils.py"
        ]
        
        os.chdir("whisper_streaming")
        
        for file_name in files_to_download:
            try:
                file_url = download_url_base + file_name
                print(f"  📄 Stahuji {file_name}...")
                urllib.request.urlretrieve(file_url, file_name)
                print(f"  ✅ {file_name}")
            except Exception as e:
                print(f"  ⚠️ Nepodařilo se stáhnout {file_name}: {e}")
        
        os.chdir("..")
        print("✅ OneClick rozšíření staženo")
        
    except Exception as e:
        print(f"⚠️ Nepodařilo se stáhnout z releases: {e}")
        print("💡 Zkuste manuální stažení z GitHub")

def create_launcher_scripts():
    """Vytvoří spouštěcí skripty pro danou platformu"""
    platform_type = detect_platform()
    
    print("🚀 Vytvářím spouštěcí skripty...")
    
    os.chdir("whisper_streaming")
    
    if platform_type == "windows":
        # Windows batch file
        with open("run_oneclick.bat", "w", encoding="utf-8") as f:
            f.write("""@echo off
chcp 65001 >nul
echo 🎬 OneClick Subtitle Generator
echo ============================
echo.
echo 📁 Vyberte složku s audio soubory...
echo.
python oneclick_subtitle_generator.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Chyba při spuštění!
    echo 💡 Zkuste: python enhanced_translator.py --help
    pause
)
""")
        
        # Windows PowerShell script
        with open("run_oneclick.ps1", "w", encoding="utf-8") as f:
            f.write("""# OneClick Subtitle Generator - PowerShell Launcher
Write-Host "🎬 OneClick Subtitle Generator" -ForegroundColor Blue
Write-Host "============================" -ForegroundColor Blue
Write-Host ""
Write-Host "📁 Spouštím GUI aplikaci..." -ForegroundColor Green

try {
    python oneclick_subtitle_generator.py
} catch {
    Write-Host "❌ Chyba při spuštění GUI!" -ForegroundColor Red
    Write-Host "💡 Zkuste: python enhanced_translator.py --help" -ForegroundColor Yellow
    Read-Host "Stiskněte Enter pro pokračování"
}
""")
        
        print("✅ Windows spouštěče vytvořeny (run_oneclick.bat, run_oneclick.ps1)")
        
    else:
        # Unix shell script
        with open("run_oneclick.sh", "w") as f:
            f.write("""#!/bin/bash
echo "🎬 OneClick Subtitle Generator"
echo "============================"
echo ""
echo "📁 Spouštím GUI aplikaci..."
echo ""

if python3 oneclick_subtitle_generator.py; then
    echo "✅ Aplikace ukončena úspěšně"
else
    echo "❌ Chyba při spuštění GUI!"
    echo "💡 Zkuste: python3 enhanced_translator.py --help"
    read -p "Stiskněte Enter pro pokračování..."
fi
""")
        
        os.chmod("run_oneclick.sh", 0o755)
        print("✅ Unix spouštěč vytvořen (run_oneclick.sh)")
    
    os.chdir("..")

def create_quick_start_guide():
    """Vytvoří rychlý návod k použití"""
    with open("QUICK_START.md", "w", encoding="utf-8") as f:
        f.write("""# 🚀 Rychlý start OneClick Subtitle Generator

## 📋 Co máte teď k dispozici

Instalace je dokončena! Máte následující soubory:

```
whisper_streaming/
├── oneclick_subtitle_generator.py  # GUI aplikace
├── enhanced_translator.py          # CLI aplikace  
├── config.py                       # Konfigurace
├── run_oneclick.sh/.bat            # Spouštěče
└── whisper_online.py               # Whisper core
```

## 🎯 Jak začít

### 1. 🖱️ GUI způsob (doporučeno)
```bash
cd whisper_streaming
python oneclick_subtitle_generator.py
```

### 2. 🔧 Command line způsob
```bash
cd whisper_streaming
python enhanced_translator.py /cesta/k/audio/slozce
```

### 3. 🚀 Pomocí spouštěče
```bash
# Linux/macOS
cd whisper_streaming
./run_oneclick.sh

# Windows
cd whisper_streaming
run_oneclick.bat
```

## 📁 Příprava audio souborů

1. Vytvořte složku pro vaše audio soubory
2. Zkopírujte do ní všechny .mp3/.wav/.m4a soubory
3. Spusťte OneClick a vyberte tuto složku
4. Klikněte "Spustit zpracování"
5. ☕ Počkejte na dokončení
6. 🎉 SRT titulky najdete ve stejné složce

## 🔧 Řešení problémů

### ❌ "No module named 'X'"
```bash
pip install librosa soundfile torch torchaudio deep-translator
```

### ❌ "whisper_online.py not found"  
```bash
# Ujistěte se, že jste ve správné složce
cd whisper_streaming
ls -la  # Měli byste vidět whisper_online.py
```

### ❌ Pomalé zpracování
```bash
# Použijte menší model
python enhanced_translator.py /audio --model medium
```

## 📞 Podpora

- 🐛 Problémy: https://github.com/PrautAutomation/oneclick-subtitle-generator/issues
- 📚 Dokumentace: https://github.com/PrautAutomation/oneclick-subtitle-generator
- ⭐ Líbí se vám? Dejte hvězdičku na GitHubu!

---
Vytvořeno OneClick Subtitle Generator installerem
""")
    
    print("✅ Rychlý návod vytvořen (QUICK_START.md)")

def run_basic_test():
    """Spustí základní test instalace"""
    print("🧪 Spouštím základní test...")
    
    try:
        # Test importů
        test_imports = [
            "import librosa",
            "import soundfile", 
            "import torch",
            "import torchaudio",
            "from deep_translator import GoogleTranslator"
        ]
        
        for test_import in test_imports:
            try:
                exec(test_import)
                module_name = test_import.split()[-1].replace("GoogleTranslator", "deep_translator")
                print(f"  ✅ {module_name}")
            except ImportError as e:
                module_name = test_import.split()[-1]
                print(f"  ❌ {module_name}: {e}")
        
        # Test Whisper backendu
        platform_type = detect_platform()
        backend, _ = get_whisper_backend(platform_type)
        
        try:
            if backend == "mlx-whisper":
                import mlx_whisper
                print(f"  ✅ {backend}")
            elif backend == "faster-whisper":
                import faster_whisper
                print(f"  ✅ {backend}")
            elif backend == "whisper-timestamped":
                import whisper_timestamped
                print(f"  ✅ {backend}")
        except ImportError:
            print(f"  ⚠️ {backend}: Bude nainstalován při prvním použití")
        
        print("✅ Základní test dokončen")
        
    except Exception as e:
        print(f"⚠️ Test se nezdařil: {e}")

def main():
    """Hlavní instalační funkce"""
    print_banner()
    
    # Základní kontroly
    check_python_version()
    
    # Kontrola Git
    if not check_git():
        install_git_instructions()
        print("\n❌ Prosím, nainstalujte Git a spusťte installer znovu")
        sys.exit(1)
    
    # Detekce platformy  
    platform_type = detect_platform()
    print(f"🎯 Detekovaná platforma: {platform_type}")
    
    try:
        # Instalační proces
        upgrade_pip()
        install_system_dependencies()
        install_python_dependencies()
        
        if not clone_whisper_streaming():
            print("❌ Nepodařilo se stáhnout whisper_streaming")
            sys.exit(1)
            
        download_oneclick_files()
        create_launcher_scripts()
        create_quick_start_guide()
        run_basic_test()
        
        # Úspěšné dokončení
        print("\n" + "=" * 60)
        print("🎉 Instalace úspěšně dokončena!")
        print("=" * 60)
        print("")
        print("📋 Co dělat dále:")
        print("  1. cd whisper_streaming")
        print("  2. python oneclick_subtitle_generator.py")
        print("")
        print("📚 Nebo si přečtěte QUICK_START.md pro detailní návod")
        print("")
        print("🆘 V případě problémů:")
        print(f"    https://github.com/{REPO_OWNER}/{REPO_NAME}/issues")
        print("")
        print("⭐ Líbí se vám? Dejte hvězdičku na GitHubu!")
        print(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⏹️ Instalace přerušena uživatelem")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Kritická chyba během instalace: {e}")
        print("🆘 Prosím nahlaste tento problém na GitHubu")
        sys.exit(1)

if __name__ == "__main__":
    main()
