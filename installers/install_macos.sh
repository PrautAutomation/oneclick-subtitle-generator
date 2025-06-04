#!/bin/bash
set -e

# OneClick Subtitle Generator - macOS Installer
# Supports macOS 10.15+ with automatic Homebrew and dependency installation

echo "🍎 OneClick Subtitle Generator - macOS Installer"
echo "==============================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Installation directory
INSTALL_DIR="$HOME/OneClick-Subtitles"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️ $1${NC}"
}

# Detect macOS version
macos_version=$(sw_vers -productVersion)
echo -e "${BLUE}🖥️ macOS Version: $macos_version${NC}"

# Detect chip architecture
chip_arch=$(uname -m)
if [[ "$chip_arch" == "arm64" ]]; then
    echo -e "${BLUE}🚀 Detected: Apple Silicon (M1/M2/M3)${NC}"
    WHISPER_BACKEND="mlx-whisper"
else
    echo -e "${BLUE}⚡ Detected: Intel processor${NC}"
    WHISPER_BACKEND="faster-whisper"
fi

# Check for Command Line Tools
print_info "Checking for Xcode Command Line Tools..."
if ! xcode-select -p &> /dev/null; then
    print_warning "Xcode Command Line Tools not found"
    echo "📦 Installing Xcode Command Line Tools..."
    xcode-select --install
    echo "⏳ Please complete the installation and run this script again"
    exit 1
else
    print_status "Xcode Command Line Tools are installed"
fi

# Check for Homebrew
print_info "Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    print_warning "Homebrew not found"
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon
    if [[ "$chip_arch" == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    print_status "Homebrew installed"
else
    print_status "Homebrew is available"
    echo "📦 Updating Homebrew..."
    brew update
fi

# Install system dependencies
print_info "Installing system dependencies..."
brew_packages=(
    "python@3.11"
    "git"
    "ffmpeg"
)

for package in "${brew_packages[@]}"; do
    if brew list "$package" &> /dev/null; then
        print_status "$package is already installed"
    else
        echo "📦 Installing $package..."
        brew install "$package"
        print_status "$package installed"
    fi
done

# Ensure Python 3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found after installation"
    exit 1
fi

python_version=$(python3 --version)
print_status "Python found: $python_version"

# Create installation directory
print_info "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download universal installer
print_info "Downloading universal installer..."
curl -L https://github.com/PrautAutomation/oneclick-subtitle-generator/releases/latest/download/install.py -o install.py

if [[ ! -f "install.py" ]]; then
    print_error "Failed to download installer"
    exit 1
fi

print_status "Universal installer downloaded"

# Run universal installer
print_info "Running universal installer..."
python3 install.py

# Create alias for easy access
print_info "Creating command line alias..."
cat >> ~/.zshrc << 'EOF'

# OneClick Subtitle Generator alias
alias oneclick-subtitles='cd ~/OneClick-Subtitles/whisper_streaming && python3 oneclick_subtitle_generator.py'
EOF

# Create desktop app (if Automator is available)
if command -v automator &> /dev/null; then
    print_info "Creating macOS application..."
    
    app_path="$HOME/Desktop/OneClick Subtitles.app"
    mkdir -p "$app_path/Contents/MacOS"
    
    # Create app script
    cat > "$app_path/Contents/MacOS/OneClick Subtitles" << EOF
#!/bin/bash
cd "$INSTALL_DIR/whisper_streaming"
python3 oneclick_subtitle_generator.py
EOF
    
    chmod +x "$app_path/Contents/MacOS/OneClick Subtitles"
    
    # Create Info.plist
    cat > "$app_path/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>OneClick Subtitles</string>
    <key>CFBundleIdentifier</key>
    <string>com.oneclick.subtitles</string>
    <key>CFBundleName</key>
    <string>OneClick Subtitles</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
EOF
    
    print_status "macOS application created on Desktop"
fi

echo ""
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo -e "${CYAN}📋 Next steps:${NC}"
echo "   1. Double-click 'OneClick Subtitles' on your desktop"
echo "   2. Or run: oneclick-subtitles (new terminal session)"
echo "   3. Or navigate to: $INSTALL_DIR/whisper_streaming"
echo ""
echo -e "${CYAN}📚 Documentation: https://github.com/PrautAutomation/oneclick-subtitle-generator${NC}"
echo -e "${CYAN}🆘 Support: https://github.com/PrautAutomation/oneclick-subtitle-generator/issues${NC}"