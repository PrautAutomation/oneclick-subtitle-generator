# 🎬 OneClick Subtitle Generator

🎬 OneClick batch subtitle generator for 8 world languages using Whisper AI

[![GitHub release](https://img.shields.io/github/v/release/PrautAutomation/oneclick-subtitle-generator)](https://github.com/PrautAutomation/oneclick-subtitle-generator/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/PrautAutomation/oneclick-subtitle-generator/total)](https://github.com/PrautAutomation/oneclick-subtitle-generator/releases)
[![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](https://github.com/PrautAutomation/oneclick-subtitle-generator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Automaticky vytvoří titulky ze všech audio souborů ve složce do 8 světových jazyků pomocí Whisper AI**

## 📦 Project Structure

```
oneclick-subtitle-generator/
├── .github/                   # GitHub workflows and issue templates
│   └── workflows/
│       └── release.yml        # CI/CD pipeline
├── docs/                      # Documentation
│   ├── installation.md
│   ├── usage.md
│   └── troubleshooting.md
├── examples/                  # Example files
│   └── expected_output/
├── installers/                # Platform-specific installers
│   ├── install_linux.sh
│   ├── install_macos.sh
│   ├── install_windows.bat
│   └── install_windows.ps1
├── src/                      # Source code
│   ├── __init__.py
│   ├── config.py
│   ├── enhanced_translator.py
│   ├── oneclick_subtitle_generator.py
│   └── utils.py
├── tests/                    # Test files
│   ├── __init__.py
│   └── test_basic.py
├── .gitignore
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── install.py
├── LICENSE
├── pyproject.toml            # Modern Python project config
├── QUICK_START.md
├── README.md
├── requirements.txt          # Development dependencies
└── setup.py
```

## 🚀 Jednokliková instalace

### Rychlá instalace (všechny platformy)
```bash
# Stáhněte a spusťte univerzální installer
curl -L https://github.com/PrautAutomation/oneclick-subtitle-generator/releases/latest/download/install.py -o install.py
python install.py
```

### Platform-specifické instalátory

#### 🪟 Windows
```powershell
# PowerShell (doporučeno)
irm https://github.com/PrautAutomation/oneclick-subtitle-generator/releases/latest/download/install_windows.ps1 | iex

# Nebo CMD
curl -L https://github.com/PrautAutomation/oneclick-subtitle-generator/releases/latest/download/install_windows.bat -o install.bat && install.bat
```

#### 🍎 macOS
```bash
# Automatická instalace s Homebrew
/bin/bash -c "$(curl -fsSL https://github.com/PrautAutomation/oneclick-subtitle-generator/releases/latest/download/install_macos.sh)"
```

#### 🐧 Linux
```bash
# Ubuntu/Debian
curl -fsSL https://github.com/PrautAutomation/oneclick-subtitle-generator/releases/latest/download/install_linux.sh | bash
```

## 🎯 Co to dělá

OneClick Subtitle Generator vezme **všechny audio soubory** z vybrané složky a automaticky:

1. 🎙️ **Transkribuje** je z češtiny pomocí Whisper AI
2. 🌍 **Překládá** do 8 nejpoužívanějších světových jazyků  
3. 📝 **Vytvoří SRT titulky** pro každý jazyk každého souboru
4. 🎬 **Produkčně připravené** titulky kompatibilní se všemi video editory

### Příklad výstupu

Z audio souboru `rozhovor.mp3` vzniknou:
```
rozhovor_cs.srt  (čeština - originál)
rozhovor_en.srt  (English)
rozhovor_es.srt  (Español) 
rozhovor_zh.srt  (中文)
rozhovor_ru.srt  (Русский)
rozhovor_de.srt  (Deutsch)
rozhovor_fr.srt  (Français)
rozhovor_id.srt  (Indonesian)
```

## 🎮 Způsoby použití

### 1. 🖱️ GUI Aplikace (Nejjednodušší)
```bash
cd whisper_streaming
python src/oneclick_subtitle_generator.py
```
- ✅ Grafické rozhraní
- ✅ Výběr složky kliknutím
- ✅ Progress bar a live log
- ✅ Výběr jazyků zaškrtáváním

### 2. 🚀 Command Line (Pokročilí)
```bash
cd whisper_streaming
python src/enhanced_translator.py /cesta/k/audio/slozce --languages cs en es zh
```
- ✅ Plná kontrola nad nastavením
- ✅ Batch zpracování
- ✅ Výběr konkrétních jazyků

### 3. 📦 Jako Python knihovna
```python
from src.enhanced_translator import EnhancedSubtitleGenerator

generator = EnhancedSubtitleGenerator()
generator.process_folder('/path/to/audio', ['cs', 'en', 'es'], 'large-v3')
```

## 📱 Podporované formáty

### Audio formáty (vstup)
- `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.wma`

### Jazyky (výstup)
- 🇨🇿 **Čeština** (cs) - originál
- 🇺🇸 **Angličtina** (en)
- 🇪🇸 **Španělština** (es)
- 🇨🇳 **Čínština** (zh)
- 🇷🇺 **Ruština** (ru)
- 🇩🇪 **Němčina** (de)
- 🇫🇷 **Francouzština** (fr)
- 🇮🇩 **Indonéština** (id)

## ⚙️ Systémové požadavky

### Minimální
- **Python 3.8+**
- **4GB RAM**
- **Internetové připojení** (pro stažení modelů a překlad)

### Doporučené  
- **8GB+ RAM** (pro rychlejší zpracování)
- **SSD disk** (pro rychlejší načítání modelů)
- **Apple Silicon (M1/M2/M3)** nebo **NVIDIA GPU** (optimální výkon)

## 🚀 Rychlý start

```bash
# 1. Instalace
python install.py

# 2. Příprava audio souborů  
# Zkopírujte všechny .mp3/.wav soubory do jedné složky

# 3. Spuštění
cd whisper_streaming
python src/oneclick_subtitle_generator.py

# 4. Výběr složky a klik na "Spustit zpracování"

# 5. ☕ Počkejte (cca 2-3 min na 10min audio na jazyk)

# 6. 🎉 Hotové SRT soubory najdete ve stejné složce
```

## 📊 Výkon a rychlost

### Typické časy zpracování

| Hardware | 10min audio | 1h audio |
|----------|-------------|----------|
| Apple M2 | ~2-3 min/jazyk | ~15-20 min/jazyk |
| Intel i7 | ~4-5 min/jazyk | ~25-30 min/jazyk |
| NVIDIA RTX | ~1-2 min/jazyk | ~8-12 min/jazyk |

### Optimalizace rychlosti

```bash
# Rychlejší, ale méně přesné
python src/enhanced_translator.py /audio --model medium

# Nejrychlejší
python src/enhanced_translator.py /audio --model tiny --languages cs en

# Nejpřesnější (výchozí)
python src/enhanced_translator.py /audio --model large-v3
```

## 🔧 Pokročilá konfigurace

### Vlastní jazyky
```python
# Upravte src/config.py
LANGUAGES = {
    'cs': 'Čeština',
    'en': 'English',
    'ja': 'Japanese',  # Přidání japonštiny
    'ko': 'Korean'     # Přidání korejštiny
}
```

### Vlastní Whisper backend
```bash
# Apple Silicon (výchozí)
python src/enhanced_translator.py /audio --backend mlx-whisper

# NVIDIA GPU
python src/enhanced_translator.py /audio --backend faster-whisper

# CPU pouze (pomalé)
python src/enhanced_translator.py /audio --backend whisper_timestamped
```

## 🛠️ Řešení problémů

### ❌ "whisper_online.py not found"
```bash
# Ujistěte se, že jste ve správné složce
cd whisper_streaming
ls -la  # Měli byste vidět whisper_online.py
```

### ❌ "No module named 'mlx_whisper'"
```bash
# Přeinstalujte backend
pip install mlx-whisper
# Nebo pro non-Apple Silicon:
pip install faster-whisper
```

### ❌ "Translation failed" 
```bash
# Zkontrolujte internet a zkuste pouze angličtinu
python src/enhanced_translator.py /audio --languages cs en
```

### ❌ Příliš pomalé
```bash
# Použijte menší model
python src/enhanced_translator.py /audio --model medium
```

Více v [docs/troubleshooting.md](docs/troubleshooting.md)

## 🤝 Přispívání

Vítáme příspěvky! Prosím:

1. 🍴 Forkněte repozitář

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"  # Install package in development mode with dev dependencies
   ```

5. **Run tests**:
   ```bash
   pytest
   ```

6. **Run linters**:
   ```bash
   black .          # Code formatter
   flake8           # Linter
   mypy .           # Type checking
   ```

7. **Build the package**:
   ```bash
   python -m build
   ```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

For more detailed documentation, please see:
- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - For the amazing speech recognition model
- [FFmpeg](https://ffmpeg.org/) - For audio processing
- [PyTorch](https://pytorch.org/) - For deep learning framework
- And all the amazing open source contributors!

## 🙏 Poděkování

- [UFAL whisper_streaming](https://github.com/ufal/whisper_streaming) - základ pro real-time transkripci
- [OpenAI Whisper](https://github.com/openai/whisper) - AI model pro rozpoznávání řeči
- [Deep Translator](https://github.com/nidhaloff/deep-translator) - překlad mezi jazyky

## 📞 Podpora

- 📚 **Dokumentace:** [docs/](docs/)
- 🐛 **Bug reports:** [GitHub Issues](https://github.com/PrautAutomation/oneclick-subtitle-generator/issues)
- 💬 **Diskuze:** [GitHub Discussions](https://github.com/PrautAutomation/oneclick-subtitle-generator/discussions)
- ⭐ **Líbí se vám?** Dejte hvězdičku!

---

<div align="center">

**Vytvořeno s ❤️ pro 🇨🇿 a je určeno pro produkční použití komukoliv kdo tvoří obsah a motivuje svět kolem sebe. Praut s.r.o. je AI startup, který vytváří produkty jako tento.**

[⬆ Zpět nahoru](#-oneclick-subtitle-generator)

</div>
