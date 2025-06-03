#!/usr/bin/env python3
"""
Rozšířená verze s Google Translate API pro skutečný překlad
"""

import os
import sys
import subprocess
import tempfile
import glob
from pathlib import Path
from datetime import timedelta
import argparse

# Pro Google Translate
try:
    from googletrans import Translator
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

# Alternativně můžete použít bezplatnou knihovnu deep-translator
try:
    from deep_translator import GoogleTranslator
    DEEP_TRANSLATOR_AVAILABLE = True
except ImportError:
    DEEP_TRANSLATOR_AVAILABLE = False

class EnhancedSubtitleGenerator:
    def __init__(self):
        self.languages = {
            'cs': 'czech',
            'en': 'english', 
            'es': 'spanish',
            'zh': 'chinese',
            'ru': 'russian',
            'de': 'german',
            'fr': 'french',
            'id': 'indonesian'
        }
        
        # Google Translate kódy
        self.google_lang_codes = {
            'cs': 'cs',
            'en': 'en',
            'es': 'es', 
            'zh': 'zh',
            'ru': 'ru',
            'de': 'de',
            'fr': 'fr',
            'id': 'id'
        }
        
        self.audio_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.wma']
        
        # Inicializace překladače
        self.translator = None
        self.init_translator()
    
    def init_translator(self):
        """Inicializuje překladač"""
        if DEEP_TRANSLATOR_AVAILABLE:
            print("✅ Používám deep-translator pro překlad")
            self.translator_type = "deep"
        elif GOOGLE_TRANSLATE_AVAILABLE:
            print("✅ Používám googletrans pro překlad")
            self.translator = Translator()
            self.translator_type = "google"
        else:
            print("⚠️ Žádný překladač není dostupný. Nainstalujte: pip install deep-translator")
            self.translator_type = None
    
    def find_audio_files(self, folder):
        """Najde všechny audio soubory ve složce"""
        audio_files = []
        for ext in self.audio_extensions:
            audio_files.extend(glob.glob(os.path.join(folder, f"*{ext}")))
            audio_files.extend(glob.glob(os.path.join(folder, f"*{ext.upper()}")))
        return audio_files
    
    def transcribe_audio(self, audio_file, model="large-v3", backend="mlx-whisper"):
        """Transkribuje audio soubor do češtiny"""
        print(f"🎙️ Transkribuji: {os.path.basename(audio_file)}")
        
        try:
            # Vytvoříme dočasný soubor pro výstup
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_output = temp_file.name
            
            # Spustíme whisper_online.py
            cmd = [
                "python3", "whisper_online.py",
                audio_file,
                "--language", "cs",
                "--model", model,
                "--backend", backend,
                "--min-chunk-size", "1",
                "--vac"
            ]
            
            print(f"📝 Spouštím: {' '.join(cmd)}")
            
            with open(temp_output, 'w', encoding='utf-8') as output_file:
                process = subprocess.run(cmd, stdout=output_file, stderr=subprocess.PIPE, 
                                       text=True, timeout=3600)
            
            if process.returncode != 0:
                print(f"❌ Whisper chyba: {process.stderr}")
                return None
            
            # Načteme a zparsujeme výstup
            transcript_data = []
            with open(temp_output, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split(' ', 3)
                    if len(parts) >= 4:
                        try:
                            start_ms = int(parts[1])
                            end_ms = int(parts[2])
                            text = parts[3]
                            transcript_data.append((start_ms, end_ms, text))
                        except ValueError:
                            continue
            
            # Vyčistíme dočasný soubor
            os.unlink(temp_output)
            
            print(f"✅ Transkripce dokončena: {len(transcript_data)} segmentů")
            return transcript_data
            
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout při zpracování {os.path.basename(audio_file)}")
            return None
        except Exception as e:
            print(f"❌ Chyba při transkripci: {str(e)}")
            return None
    
    def translate_text(self, text, target_lang):
        """Přeloží text do cílového jazyka"""
        if target_lang == 'cs':
            return text  # Už je v češtině
        
        if not self.translator_type:
            print(f"⚠️ Překladač není dostupný, vracím původní text")
            return text
        
        try:
            if self.translator_type == "deep":
                translated = GoogleTranslator(source='cs', target=self.google_lang_codes[target_lang]).translate(text)
                return translated
            elif self.translator_type == "google":
                result = self.translator.translate(text, src='cs', dest=self.google_lang_codes[target_lang])
                return result.text
        except Exception as e:
            print(f"❌ Chyba při překladu: {str(e)}")
            return text
    
    def translate_transcript(self, transcript_data, target_lang):
        """Přeloží celou transkripci"""
        if target_lang == 'cs':
            return transcript_data
        
        print(f"🌍 Překládám do jazyka: {self.languages[target_lang]}")
        
        translated_data = []
        total_segments = len(transcript_data)
        
        for i, (start_ms, end_ms, text) in enumerate(transcript_data):
            if i % 10 == 0:  # Progress každých 10 segmentů
                print(f"   📊 Progress: {i+1}/{total_segments}")
            
            translated_text = self.translate_text(text, target_lang)
            translated_data.append((start_ms, end_ms, translated_text))
        
        return translated_data
    
    def create_srt_file(self, transcript_data, output_file):
        """Vytvoří SRT soubor z transkripčních dat"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for i, (start_ms, end_ms, text) in enumerate(transcript_data, 1):
                    start_time = self.ms_to_srt_time(start_ms)
                    end_time = self.ms_to_srt_time(end_ms)
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            print(f"✅ Vytvořen SRT: {os.path.basename(output_file)}")
        except Exception as e:
            print(f"❌ Chyba při vytváření SRT: {str(e)}")
    
    def ms_to_srt_time(self, milliseconds):
        """Převede milisekundy na SRT časový formát"""
        td = timedelta(milliseconds=milliseconds)
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        ms = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"
    
    def process_folder(self, folder, selected_languages=None, model="large-v3", backend="mlx-whisper"):
        """Zpracuje všechny audio soubory ve složce"""
        if selected_languages is None:
            selected_languages = list(self.languages.keys())
        
        audio_files = self.find_audio_files(folder)
        
        if not audio_files:
            print("❌ Žádné audio soubory nebyly nalezeny!")
            return
        
        print(f"📁 Nalezeno {len(audio_files)} audio souborů")
        print(f"🌍 Vybrané jazyky: {', '.join(selected_languages)}")
        print(f"🎯 Celkem úkolů: {len(audio_files) * len(selected_languages)}")
        
        completed = 0
        total = len(audio_files) * len(selected_languages)
        
        for i, audio_file in enumerate(audio_files):
            file_name = Path(audio_file).stem
            print(f"\n{'='*60}")
            print(f"📄 Zpracovávám soubor {i+1}/{len(audio_files)}: {os.path.basename(audio_file)}")
            print(f"{'='*60}")
            
            # Transkripce do češtiny
            transcript_data = self.transcribe_audio(audio_file, model, backend)
            
            if not transcript_data:
                print(f"❌ Přeskakuji soubor kvůli chybě transkripce")
                completed += len(selected_languages)
                continue
            
            # Vytvoření titulků pro každý jazyk
            for lang_code in selected_languages:
                completed += 1
                progress = (completed / total) * 100
                
                print(f"\n🔄 [{completed}/{total}] ({progress:.1f}%) Jazyk: {self.languages[lang_code]} ({lang_code})")
                
                # Překlad
                translated_data = self.translate_transcript(transcript_data, lang_code)
                
                # Vytvoření SRT souboru
                output_file = os.path.join(folder, f"{file_name}_{lang_code}.srt")
                self.create_srt_file(translated_data, output_file)
        
        print(f"\n🎉 Zpracování dokončeno!")
        print(f"📊 Vytvořeno {completed} SRT souborů")

def main():
    parser = argparse.ArgumentParser(description='OneClick Subtitle Generator - Batch zpracování')
    parser.add_argument('folder', help='Složka s audio soubory')
    parser.add_argument('--languages', nargs='+', 
                       choices=['cs', 'en', 'es', 'zh', 'ru', 'de', 'fr', 'id'],
                       default=['cs', 'en', 'es', 'zh', 'ru', 'de', 'fr', 'id'],
                       help='Jazyky pro titulky (default: všechny)')
    parser.add_argument('--model', default='large-v3',
                       choices=['tiny', 'base', 'small', 'medium', 'large-v2', 'large-v3'],
                       help='Whisper model (default: large-v3)')
    parser.add_argument('--backend', default='mlx-whisper',
                       choices=['mlx-whisper', 'faster-whisper', 'whisper_timestamped'],
                       help='Whisper backend (default: mlx-whisper)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.folder):
        print(f"❌ Složka {args.folder} neexistuje!")
        sys.exit(1)
    
    generator = EnhancedSubtitleGenerator()
    generator.process_folder(args.folder, args.languages, args.model, args.backend)

if __name__ == "__main__":
    main()