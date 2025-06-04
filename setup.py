#!/usr/bin/env python3
"""
OneClick Subtitle Generator - Setup Script
Allows installation via pip install
"""

from setuptools import setup, find_packages
from setuptools.config import read_configuration
import platform
import sys
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
def read_requirements(section=''):
    """Read requirements from requirements.txt"""
    requirements_file = this_directory / "requirements.txt"
    if not requirements_file.exists():
        return []
        
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = []
        in_section = not section  # If no section specified, read all non-section lines
        
        for line in f:
            line = line.strip()
            
            # Handle section headers
            if line.startswith('[') and line.endswith(']'):
                in_section = (line[1:-1] == section)
                continue
                
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            # Only add if in the right section or no section specified
            if in_section:
                requirements.append(line)
                
    return requirements

# Platform-specific dependencies
def get_platform_dependencies():
    """Get platform-specific Whisper backends"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    deps = []
    
    if system == "darwin" and machine in ["arm64", "aarch64"]:
        # Apple Silicon - prefer MLX Whisper
        deps.append("mlx-whisper==0.1.0")
    else:
        # Other platforms - use faster-whisper
        deps.append("faster-whisper==0.9.0")
    
    # Fallback option
    deps.append("whisper-timestamped==1.14.0")
    
    return deps

# Base requirements
base_requirements = read_requirements()

# Development requirements
extras_require = {
    'dev': read_requirements('dev'),
    'test': read_requirements('test'),
    'doc': read_requirements('doc'),
    'all': read_requirements('all'),
}

# Combine all extras for 'all' option
extras_require['all'] = list(set(
    dep 
    for deps in extras_require.values() 
    for dep in deps
    if dep not in base_requirements
))

# Platform specific dependencies
platform_deps = get_platform_dependencies()

# Add platform-specific dependencies to all extras
for key in extras_require:
    extras_require[key].extend(platform_deps)

# All requirements
all_requirements = base_requirements + platform_deps

# Add additional optional dependencies
extras_require.update({
    'gui': [
        # tkinter is usually built-in, but for some Docker images
        'tkinter; platform_system!="Darwin"'
    ],
    'openai': [
        'openai>=1.0.0'
    ]
})

# Update 'all' to include all optional dependencies
extras_require['all'].extend([
    'openai>=1.0.0',
    'tkinter; platform_system!="Darwin"'
])

setup(
    name="oneclick-subtitle-generator",
    version="1.0.0",
    author="Martin Švanda",
    author_email="martin.k.svanda@gmail.com",
    description="OneClick batch subtitle generator for 8 world languages using Whisper AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PrautAutomation/oneclick-subtitle-generator",
    project_urls={
        "Bug Tracker": "https://github.com/PrautAutomation/oneclick-subtitle-generator/issues",
        "Documentation": "https://github.com/PrautAutomation/oneclick-subtitle-generator#readme",
        "Source Code": "https://github.com/PrautAutomation/oneclick-subtitle-generator",
        "Discussions": "https://github.com/PrautAutomation/oneclick-subtitle-generator/discussions"
    },
    
    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Dependencies
    python_requires=">=3.8",
    install_requires=all_requirements,
    extras_require=extras_require,
    
    # Entry points for command line
    entry_points={
        "console_scripts": [
            "oneclick-subtitles=enhanced_translator:main",
            "oneclick-subtitles-gui=oneclick_subtitle_generator:main",
            "oneclick-batch=enhanced_translator:main",
        ],
    },
    
    # Package data
    include_package_data=True,
    package_data={
        "": [
            "*.md", 
            "*.txt", 
            "*.yml", 
            "*.yaml",
            "config.py"
        ],
    },
    
    # Metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux", 
        "Operating System :: MacOS",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
    ],
    
    keywords=[
        "whisper", "subtitle", "transcription", "translation", 
        "ai", "speech-to-text", "batch-processing", "multilingual",
        "srt", "video", "audio", "automatic", "oneclick"
    ],
    
    # Zip safety
    zip_safe=False,
    
    # Platform specific
    platforms=["any"],
    
    # License
    license="MIT",
    
    # Additional metadata
    maintainer="Martin Švanda",
    maintainer_email="martin.k.svanda@gmail.com",
    
    # CLI help
    options={
        'build_scripts': {
            'executable': '/usr/bin/env python3',
        },
    },
)

# Post-install message
if __name__ == "__main__":
    print("""
    🎉 OneClick Subtitle Generator installed successfully!
    
    📋 Usage:
       oneclick-subtitles-gui          # GUI application
       oneclick-subtitles /path        # CLI batch processing
       
    📚 Documentation:
       https://github.com/PrautAutomation/oneclick-subtitle-generator
       
    🆘 Support:
       https://github.com/PrautAutomation/oneclick-subtitle-generator/issues
    """)
