# OneClick Subtitle Generator - Windows PowerShell Installer
# Supports Windows 10/11 with automatic Python and Git installation

param(
    [switch]$SkipPythonCheck,
    [switch]$SkipGitCheck,
    [string]$InstallPath = "$env:USERPROFILE\OneClick-Subtitles"
)

# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🪟 OneClick Subtitle Generator - Windows Installer" -ForegroundColor Blue
Write-Host "=================================================" -ForegroundColor Blue

# Check execution policy
$executionPolicy = Get-ExecutionPolicy -Scope CurrentUser
if ($executionPolicy -eq "Restricted") {
    Write-Host "⚙️ Setting PowerShell execution policy..." -ForegroundColor Yellow
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Host "✅ Execution policy updated" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to set execution policy: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Function to check if command exists
function Test-Command($command) {
    try {
        Get-Command $command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Function to install Chocolatey
function Install-Chocolatey {
    if (!(Test-Command "choco")) {
        Write-Host "📦 Installing Chocolatey package manager..." -ForegroundColor Green
        try {
            Set-ExecutionPolicy Bypass -Scope Process -Force
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
            Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
            Write-Host "✅ Chocolatey installed" -ForegroundColor Green
            
            # Refresh environment
            refreshenv
            Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
        } catch {
            Write-Host "❌ Failed to install Chocolatey: $($_.Exception.Message)" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✅ Chocolatey is already installed" -ForegroundColor Green
    }
    return $true
}

# Check Python
if (!$SkipPythonCheck) {
    Write-Host "🐍 Checking Python installation..." -ForegroundColor Cyan
    
    if (Test-Command "python") {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
        
        # Check version
        $version = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        if ([version]$version -lt [version]"3.8") {
            Write-Host "❌ Python 3.8+ is required, found $version" -ForegroundColor Red
            Write-Host "📥 Installing Python via Microsoft Store..." -ForegroundColor Yellow
            start "ms-windows-store://pdp/?ProductId=9NRWMJP3717K"
            Write-Host "Please install Python and run this script again." -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "❌ Python not found" -ForegroundColor Red
        Write-Host "📦 Installing Python via Chocolatey..." -ForegroundColor Yellow
        
        if (Install-Chocolatey) {
            try {
                choco install python3 -y
                refreshenv
                Write-Host "✅ Python installed via Chocolatey" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to install Python via Chocolatey" -ForegroundColor Red
                Write-Host "📥 Please install Python manually from: https://www.python.org/downloads/" -ForegroundColor Yellow
                exit 1
            }
        }
    }
}

# Check Git
if (!$SkipGitCheck) {
    Write-Host "📥 Checking Git installation..." -ForegroundColor Cyan
    
    if (!(Test-Command "git")) {
        Write-Host "❌ Git not found" -ForegroundColor Red
        Write-Host "📦 Installing Git..." -ForegroundColor Yellow
        
        if (Install-Chocolatey) {
            try {
                choco install git -y
                refreshenv
                Write-Host "✅ Git installed" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to install Git via Chocolatey" -ForegroundColor Red
                Write-Host "📥 Please install Git manually from: https://git-scm.com/download/win" -ForegroundColor Yellow
                exit 1
            }
        }
    } else {
        Write-Host "✅ Git is available" -ForegroundColor Green
    }
}

# Create installation directory
Write-Host "📁 Creating installation directory: $InstallPath" -ForegroundColor Cyan
if (!(Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
}
Set-Location $InstallPath

# Download and run universal installer
Write-Host "📥 Downloading universal installer..." -ForegroundColor Cyan
try {
    $installerUrl = "https://github.com/PrautAutomation/oneclick-subtitle-generator/releases/latest/download/install.py"
    Invoke-WebRequest -Uri $installerUrl -OutFile "install.py"
    Write-Host "✅ Universal installer downloaded" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to download installer: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Run universal installer
Write-Host "🚀 Running universal installer..." -ForegroundColor Cyan
try {
    python install.py
    Write-Host "✅ Installation completed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Installation failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Create desktop shortcut
Write-Host "🔗 Creating desktop shortcut..." -ForegroundColor Cyan
try {
    $shortcutPath = "$env:USERPROFILE\Desktop\OneClick Subtitles.lnk"
    $targetPath = "$InstallPath\whisper_streaming\run_oneclick.bat"
    
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $targetPath
    $shortcut.WorkingDirectory = "$InstallPath\whisper_streaming"
    $shortcut.Description = "OneClick Subtitle Generator"
    $shortcut.Save()
    
    Write-Host "✅ Desktop shortcut created" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Failed to create desktop shortcut: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Installation completed successfully!" -ForegroundColor Green
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Double-click 'OneClick Subtitles' on your desktop" -ForegroundColor White
Write-Host "   2. Or navigate to: $InstallPath\whisper_streaming" -ForegroundColor White
Write-Host "   3. Run: python oneclick_subtitle_generator.py" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation: https://github.com/PrautAutomation/oneclick-subtitle-generator" -ForegroundColor Cyan
Write-Host "🆘 Support: https://github.com/PrautAutomation/oneclick-subtitle-generator/issues" -ForegroundColor Cyan

Read-Host "Press Enter to exit"