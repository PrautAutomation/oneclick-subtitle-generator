#!/bin/bash
set -e

# OneClick Subtitle Generator - Linux Installer
# Supports Ubuntu, Debian, CentOS, RHEL, Fedora, Arch Linux

echo "🐧 OneClick Subtitle Generator - Linux Installer"
echo "==============================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Installation directory
INSTALL_DIR="$HOME/OneClick-Subtitles"

print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
print_info() { echo -e "${CYAN}ℹ️ $1${NC}"; }

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    VERSION=$VERSION_ID
elif [ -f /etc/lsb-release ]; then
    . /etc/lsb-release
    DISTRO=$DISTRIB_ID
    VERSION=$DISTRIB_RELEASE
else
    DISTRO="unknown"
fi

echo -e "${BLUE}🖥️ Detected: $PRETTY_NAME${NC}"

# Function to install packages based on distribution
install_packages() {
    case $DISTRO in
        ubuntu|debian)
            print_info "Using apt package manager..."
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv git ffmpeg curl
            ;;
        centos|rhel|fedora)
            if command -v dnf &> /dev/null; then
                print_info "Using dnf package manager..."
                sudo dnf install -y python3 python3-pip git ffmpeg curl
            elif command -v yum &> /dev/null; then
                print_info "Using yum package manager..."
                sudo yum install -y python3 python3-pip git ffmpeg curl
            fi
            ;;
        arch|manjaro)
            print_info "Using pacman package manager..."
            sudo pacman -Sy --noconfirm python python-pip git ffmpeg curl
            ;;
        opensuse*)
            print_info "Using zypper package manager..."
            sudo zypper install -y python3 python3-pip git ffmpeg curl
            ;;
        *)
            print_warning "Unknown distribution: $DISTRO"
            print_info "Please install manually: python3, python3-pip, git, ffmpeg, curl"
            echo "Then run this script again."
            exit 1
            ;;
    esac
}

# Check for required commands
check_command() {
    if ! command -v $1 &> /dev/null; then
        return 1
    fi
    return 0
}

# Install system packages
print_info "Installing system dependencies..."
install_packages
print_status "System dependencies installed"

# Verify installations
print_info "Verifying installations..."

if check_command python3; then
    python_version=$(python3 --version)
    print_status "Python found: $python_version"
else
    print_error "Python 3 not found after installation"
    exit 1
fi

if check_command git; then
    print_status "Git is available"
else
    print_error "Git not found after installation"
    exit 1
fi

if check_command ffmpeg; then
    print_status "FFmpeg is available"
else
    print_warning "FFmpeg not found, audio processing may be limited"
fi

# Check Python version
python_version_check=$(python3 -c "import sys; print(sys.version_info >= (3, 8))")
if [ "$python_version_check" != "True" ]; then
    print_error "Python 3.8+ is required"
    exit 1
fi

# Create installation directory
print_info "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download universal installer
print_info "Downloading universal installer..."
if curl -L https://github.com/YOUR_USERNAME/oneclick-subtitle-generator/releases/latest/download/install.py -o install.py; then
    print_status "Universal installer downloaded"
else
    print_error "Failed to download installer"
    exit 1
fi

# Run universal installer
print_info "Running universal installer..."
python3 install.py

# Create desktop entry (if desktop environment is available)
if [ -n "$XDG_CURRENT_DESKTOP" ] && [ -d "$HOME/.local/share/applications" ]; then
    print_info "Creating desktop entry..."
    
    cat > "$HOME/.local/share/applications/oneclick-subtitles.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=OneClick Subtitles
Comment=Generate subtitles in 8 languages from audio files
Exec=python3 $INSTALL_DIR/whisper_streaming/oneclick_subtitle_generator.py
Icon=audio-x-generic
Terminal=false
Categories=AudioVideo;Audio;
StartupNotify=true
EOF
    
    chmod +x "$HOME/.local/share/applications/oneclick-subtitles.desktop"
    print_status "Desktop entry created"
fi

# Create command line alias
print_info "Creating command line alias..."
shell_rc=""
if [ -n "$ZSH_VERSION" ]; then
    shell_rc="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    shell_rc="$HOME/.bashrc"
fi

if [ -n "$shell_rc" ]; then
    echo "" >> "$shell_rc"
    echo "# OneClick Subtitle Generator alias" >> "$shell_rc"
    echo "alias oneclick-subtitles='cd $INSTALL_DIR/whisper_streaming && python3 oneclick_subtitle_generator.py'" >> "$shell_rc"
    print_status "Command line alias added to $shell_rc"
fi

echo ""
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo -e "${CYAN}📋 Next steps:${NC}"
echo "   1. Look for 'OneClick Subtitles' in your applications menu"
echo "   2. Or run: oneclick-subtitles (new terminal session)"
echo "   3. Or navigate to: $INSTALL_DIR/whisper_streaming"
echo ""
echo -e "${CYAN}📚 Documentation: https://github.com/YOUR_USERNAME/oneclick-subtitle-generator${NC}"
echo -e "${CYAN}🆘 Support: https://github.com/YOUR_USERNAME/oneclick-subtitle-generator/issues${NC}"