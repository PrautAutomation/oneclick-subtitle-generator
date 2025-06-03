@echo off
REM OneClick Subtitle Generator - Windows Batch Installer
REM Fallback installer for systems without PowerShell execution rights

echo ========================================
echo OneClick Subtitle Generator - Windows Installer
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
echo.

REM Create installation directory
set INSTALL_DIR=%USERPROFILE%\OneClick-Subtitles
echo Creating installation directory: %INSTALL_DIR%
mkdir "%INSTALL_DIR%" 2>nul
cd /d "%INSTALL_DIR%"

REM Download universal installer
echo Downloading universal installer...
curl -L https://github.com/YOUR_USERNAME/oneclick-subtitle-generator/releases/latest/download/install.py -o install.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to download installer
    echo Please check your internet connection
    pause
    exit /b 1
)

echo.
echo Running universal installer...
python install.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Navigate to: %INSTALL_DIR%\whisper_streaming
echo 2. Run: python oneclick_subtitle_generator.py
echo.
pause
