# 🚀 Rychlý start OneClick Subtitle Generator

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
