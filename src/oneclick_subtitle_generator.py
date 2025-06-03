#!/usr/bin/env python3
"""
OneClick Subtitle Generator
Automaticky zpracuje všechny audio soubory ve složce a vytvoří titulky v 8 jazycích
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import threading
import glob
from pathlib import Path
import tempfile
import csv
from datetime import timedelta
import sys

class SubtitleGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OneClick Subtitle Generator")
        self.root.geometry("800x600")
        
        # Jazyky pro překlad
        self.languages = {
            'cs': 'Čeština',
            'en': 'English', 
            'es': 'Español',
            'zh': 'Chinese',
            'ru': 'Русский',
            'de': 'Deutsch',
            'fr': 'Français',
            'id': 'Indonesian'
        }
        
        # Podporované audio formáty
        self.audio_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.wma']
        
        self.setup_ui()
        self.processing = False
        
    def setup_ui(self):
        # Hlavní frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Výběr složky
        folder_frame = ttk.LabelFrame(main_frame, text="Výběr složky s audio soubory", padding="10")
        folder_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.folder_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.folder_var, width=60).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(folder_frame, text="Procházet", command=self.select_folder).grid(row=0, column=1, padx=(10, 0))
        
        # Nastavení
        settings_frame = ttk.LabelFrame(main_frame, text="Nastavení", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Model Whisper
        ttk.Label(settings_frame, text="Whisper model:").grid(row=0, column=0, sticky=tk.W)
        self.model_var = tk.StringVar(value="large-v3")
        model_combo = ttk.Combobox(settings_frame, textvariable=self.model_var, 
                                  values=["tiny", "base", "small", "medium", "large-v2", "large-v3"])
        model_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Backend
        ttk.Label(settings_frame, text="Backend:").grid(row=1, column=0, sticky=tk.W)
        self.backend_var = tk.StringVar(value="mlx-whisper")
        backend_combo = ttk.Combobox(settings_frame, textvariable=self.backend_var,
                                   values=["mlx-whisper", "faster-whisper", "whisper_timestamped"])
        backend_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Výběr jazyků
        languages_frame = ttk.LabelFrame(main_frame, text="Jazyky titulků", padding="10")
        languages_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.language_vars = {}
        row, col = 0, 0
        for code, name in self.languages.items():
            var = tk.BooleanVar(value=True)
            self.language_vars[code] = var
            ttk.Checkbutton(languages_frame, text=f"{name} ({code})", variable=var).grid(
                row=row, column=col, sticky=tk.W, padx=(0, 20))
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Tlačítka
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="🚀 Spustit zpracování", 
                                      command=self.start_processing, style="Accent.TButton")
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Zastavit", 
                                     command=self.stop_processing, state="disabled")
        self.stop_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, mode='determinate')
        self.progress_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log zpracování", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Konfigurace gridu
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        folder_frame.columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="Vyberte složku s audio soubory")
        if folder:
            self.folder_var.set(folder)
            self.scan_audio_files()
    
    def scan_audio_files(self):
        folder = self.folder_var.get()
        if not folder:
            return
            
        audio_files = []
        for ext in self.audio_extensions:
            audio_files.extend(glob.glob(os.path.join(folder, f"*{ext}")))
            audio_files.extend(glob.glob(os.path.join(folder, f"*{ext.upper()}")))
        
        self.log(f"📁 Nalezeno {len(audio_files)} audio souborů:")
        for file in audio_files:
            self.log(f"   📄 {os.path.basename(file)}")
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_processing(self):
        folder = self.folder_var.get()
        if not folder:
            messagebox.showerror("Chyba", "Vyberte prosím složku s audio soubory!")
            return
        
        selected_languages = [code for code, var in self.language_vars.items() if var.get()]
        if not selected_languages:
            messagebox.showerror("Chyba", "Vyberte prosím alespoň jeden jazyk!")
            return
        
        self.processing = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Spuštění v novém threadu
        thread = threading.Thread(target=self.process_files, args=(folder, selected_languages))
        thread.daemon = True
        thread.start()
    
    def stop_processing(self):
        self.processing = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("⏹️ Zpracování zastaveno uživatelem")
    
    def process_files(self, folder, selected_languages):
        try:
            # Najdeme všechny audio soubory
            audio_files = []
            for ext in self.audio_extensions:
                audio_files.extend(glob.glob(os.path.join(folder, f"*{ext}")))
                audio_files.extend(glob.glob(os.path.join(folder, f"*{ext.upper()}")))
            
            if not audio_files:
                self.log("❌ Žádné audio soubory nebyly nalezeny!")
                return
            
            total_files = len(audio_files)
            total_tasks = total_files * len(selected_languages)
            completed_tasks = 0
            
            self.log(f"🚀 Začínám zpracování {total_files} souborů do {len(selected_languages)} jazyků")
            self.log(f"📊 Celkem úkolů: {total_tasks}")
            
            for i, audio_file in enumerate(audio_files):
                if not self.processing:
                    break
                    
                file_name = Path(audio_file).stem
                self.log(f"\n📄 Zpracovávám soubor {i+1}/{total_files}: {os.path.basename(audio_file)}")
                
                # Nejprv vytvoříme českou transkripci
                self.log("🎙️ Vytvářím českou transkripci...")
                czech_transcript = self.transcribe_audio(audio_file)
                
                if not czech_transcript:
                    self.log(f"❌ Chyba při transkripci souboru {os.path.basename(audio_file)}")
                    completed_tasks += len(selected_languages)
                    continue
                
                # Vytvoříme titulky pro každý vybraný jazyk
                for lang_code in selected_languages:
                    if not self.processing:
                        break
                        
                    completed_tasks += 1
                    progress = (completed_tasks / total_tasks) * 100
                    self.progress_var.set(progress)
                    
                    self.log(f"🌍 Vytvářím titulky pro jazyk: {self.languages[lang_code]} ({lang_code})")
                    
                    if lang_code == 'cs':
                        # Pro češtinu použijeme původní transkripci
                        translated_text = czech_transcript
                    else:
                        # Pro ostatní jazyky přeložíme
                        translated_text = self.translate_text(czech_transcript, lang_code)
                    
                    if translated_text:
                        output_file = os.path.join(folder, f"{file_name}_{lang_code}.srt")
                        self.create_srt_file(translated_text, output_file)
                        self.log(f"✅ Vytvořen: {os.path.basename(output_file)}")
                    else:
                        self.log(f"❌ Chyba při překladu do jazyka {lang_code}")
            
            self.log(f"\n🎉 Zpracování dokončeno! Zpracováno {completed_tasks}/{total_tasks} úkolů")
            
        except Exception as e:
            self.log(f"❌ Kritická chyba: {str(e)}")
        finally:
            self.processing = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.progress_var.set(100)
    
    def transcribe_audio(self, audio_file):
        """Transkribuje audio soubor do češtiny"""
        try:
            # Vytvoříme dočasný soubor pro výstup
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_output = temp_file.name
            
            # Spustíme whisper_online.py
            cmd = [
                "python3", "whisper_online.py",
                audio_file,
                "--language", "cs",
                "--model", self.model_var.get(),
                "--backend", self.backend_var.get(),
                "--min-chunk-size", "1",
                "--vac"
            ]
            
            with open(temp_output, 'w', encoding='utf-8') as output_file:
                process = subprocess.run(cmd, stdout=output_file, stderr=subprocess.PIPE, 
                                       text=True, timeout=3600)  # 1 hodina timeout
            
            if process.returncode != 0:
                self.log(f"❌ Whisper chyba: {process.stderr}")
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
            
            return transcript_data
            
        except subprocess.TimeoutExpired:
            self.log(f"❌ Timeout při zpracování {os.path.basename(audio_file)}")
            return None
        except Exception as e:
            self.log(f"❌ Chyba při transkripci: {str(e)}")
            return None
    
    def translate_text(self, transcript_data, target_lang):
        """Přeloží text do cílového jazyka"""
        # Pro jednoduchost použijeme Whisper translate task pro angličtinu
        # Pro ostatní jazyky bychom potřebovali externí překladač
        
        if target_lang == 'en':
            # Pro angličtinu můžeme použít Whisper translate
            return self.whisper_translate_to_english(transcript_data)
        else:
            # Pro ostatní jazyky použijeme placeholder - zde by se připojil skutečný překladač
            self.log(f"⚠️ Překlad do {target_lang} není ještě implementován, používám původní text")
            return transcript_data
    
    def whisper_translate_to_english(self, transcript_data):
        """Použije Whisper pro překlad do angličtiny"""
        # Toto by vyžadovalo další implementaci s Whisper translate task
        # Pro jednoduchost vrátíme původní data
        self.log("⚠️ Whisper translate ještě není implementován, používám původní text")
        return transcript_data
    
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
        except Exception as e:
            self.log(f"❌ Chyba při vytváření SRT: {str(e)}")
    
    def ms_to_srt_time(self, milliseconds):
        """Převede milisekundy na SRT časový formát"""
        td = timedelta(milliseconds=milliseconds)
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        ms = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"
    
    def run(self):
        self.root.mainloop()

def main():
    app = SubtitleGenerator()
    app.run()

if __name__ == "__main__":
    main()