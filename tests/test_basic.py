#!/usr/bin/env python3
"""
Basic tests for OneClick Subtitle Generator
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from utils import (
        ms_to_srt_time, detect_audio_files, format_duration,
        clean_filename, validate_audio_file, create_srt_content
    )
    from config import LANGUAGES, AUDIO_EXTENSIONS, validate_config
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running tests from the project root directory")
    sys.exit(1)

class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_ms_to_srt_time(self):
        """Test milliseconds to SRT time conversion"""
        self.assertEqual(ms_to_srt_time(0), "00:00:00,000")
        self.assertEqual(ms_to_srt_time(1000), "00:00:01,000")
        self.assertEqual(ms_to_srt_time(61000), "00:01:01,000")
        self.assertEqual(ms_to_srt_time(3661000), "01:01:01,000")
        self.assertEqual(ms_to_srt_time(125500), "00:02:05,500")
    
    def test_format_duration(self):
        """Test duration formatting"""
        self.assertEqual(format_duration(30), "30s")
        self.assertEqual(format_duration(90), "1m 30s")
        self.assertEqual(format_duration(3665), "1h 1m 5s")
    
    def test_clean_filename(self):
        """Test filename cleaning"""
        self.assertEqual(clean_filename("test<file>.mp3"), "test_file_.mp3")
        self.assertEqual(clean_filename('bad"name|here.wav'), "bad_name_here.wav")
        self.assertEqual(clean_filename("  normal_file.mp3  "), "normal_file.mp3")
    
    def test_detect_audio_files(self):
        """Test audio file detection"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_files = ["test.mp3", "audio.wav", "video.mp4", "music.flac"]
            for file in test_files:
                Path(temp_dir, file).touch()
            
            audio_files = detect_audio_files(temp_dir)
            audio_names = [f.name for f in audio_files]
            
            self.assertIn("test.mp3", audio_names)
            self.assertIn("audio.wav", audio_names) 
            self.assertIn("music.flac", audio_names)
            self.assertNotIn("video.mp4", audio_names)
    
    def test_create_srt_content(self):
        """Test SRT content creation"""
        transcript_data = [
            (0, 2000, "Hello world"),
            (2000, 5000, "This is a test")
        ]
        
        srt_content = create_srt_content(transcript_data)
        lines = srt_content.split('\n')
        
        self.assertEqual(lines[0], "1")
        self.assertEqual(lines[1], "00:00:00,000 --> 00:00:02,000")
        self.assertEqual(lines[2], "Hello world")
        self.assertEqual(lines[4], "2")

class TestConfig(unittest.TestCase):
    """Test configuration"""
    
    def test_languages(self):
        """Test language configuration"""
        self.assertIsInstance(LANGUAGES, dict)
        self.assertIn('cs', LANGUAGES)
        self.assertIn('en', LANGUAGES)
        self.assertEqual(len(LANGUAGES), 8)
    
    def test_audio_extensions(self):
        """Test audio extensions"""
        self.assertIsInstance(AUDIO_EXTENSIONS, list)
        self.assertIn('.mp3', AUDIO_EXTENSIONS)
        self.assertIn('.wav', AUDIO_EXTENSIONS)
    
    def test_config_validation(self):
        """Test configuration validation"""
        errors = validate_config()
        self.assertEqual(len(errors), 0, f"Configuration errors: {errors}")

class TestInstallation(unittest.TestCase):
    """Test installation requirements"""
    
    def test_python_version(self):
        """Test Python version requirement"""
        import sys
        self.assertGreaterEqual(sys.version_info[:2], (3, 8))
    
    def test_core_imports(self):
        """Test that core dependencies can be imported"""
        try:
            import platform
            import os
            import subprocess
            import tempfile
            import json
            from pathlib import Path
        except ImportError as e:
            self.fail(f"Core import failed: {e}")

if __name__ == '__main__':
    print("🧪 Running OneClick Subtitle Generator Tests")
    print("=" * 50)
    
    # Run tests
    unittest.main(verbosity=2)