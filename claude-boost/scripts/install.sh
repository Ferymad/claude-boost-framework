#!/bin/bash
# Claude Code Boost Installation Script
# Usage: curl -LsSf https://claude-boost.dev/install.sh | sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "🚀 Claude Code Boost v1.0 - Installation"
    echo "========================================"
    echo -e "${NC}"
}

error() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect package manager and install method
detect_install_method() {
    if command_exists python3; then
        INSTALL_METHOD="pip"
        INSTALL_CMD="pip install claude-boost"
    elif command_exists node && command_exists npm; then
        INSTALL_METHOD="npm"
        INSTALL_CMD="npm install -g claude-boost"
    elif command_exists node && command_exists npx; then
        INSTALL_METHOD="npx"
        INSTALL_CMD="npx claude-boost@latest init"
    else
        error "No supported package manager found. Please install Python 3 or Node.js first."
    fi
}

# Install Claude Code Boost
install_claude_boost() {
    info "Installing Claude Code Boost using $INSTALL_METHOD..."
    
    case $INSTALL_METHOD in
        "pip")
            if ! python3 -m pip install claude-boost; then
                error "Failed to install via pip"
            fi
            success "Claude Code Boost installed via pip"
            echo ""
            echo "To initialize in your project:"
            echo "  cd your-project/"
            echo "  claude-boost init"
            ;;
        "npm")
            if ! npm install -g claude-boost; then
                error "Failed to install via npm"
            fi
            success "Claude Code Boost installed via npm"
            echo ""
            echo "To initialize in your project:"
            echo "  cd your-project/"
            echo "  claude-boost init"
            ;;
        "npx")
            success "Ready to use Claude Code Boost via npx"
            echo ""
            echo "To initialize in your project:"
            echo "  cd your-project/"
            echo "  npx claude-boost init"
            ;;
    esac
}

# Main installation flow
main() {
    print_header
    
    info "Detecting installation method..."
    detect_install_method
    success "Using $INSTALL_METHOD for installation"
    
    # Check for Claude Code
    if ! command_exists claude; then
        warning "Claude Code not found. Please install Claude Code first:"
        echo "  Visit: https://claude.ai/code"
        echo ""
        echo "You can still install Claude Code Boost now and use it later."
        read -p "Continue installation? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    else
        success "Claude Code detected"
    fi
    
    install_claude_boost
    
    echo ""
    success "Installation complete!"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Navigate to your project directory"
    echo "2. Run: claude-boost init (or npx claude-boost init)"
    echo "3. Follow the interactive setup"
    echo "4. Start using: claude --continue && /fresh"
    echo ""
    echo "📚 Documentation: https://claude-boost.dev"
    echo "💬 Community: https://discord.gg/claude-boost"
}

# Run main function
main "$@"