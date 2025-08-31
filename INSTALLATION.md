# 🚀 Claude Boost Installation Guide

## Quick Installation (Beta)

```bash
# NPM Installation (Recommended)
npm install -g claude-boost@beta

# Initialize in your project
claude-boost init
```

---

## Installation Methods

### Method 1: NPM (Recommended) 📦

**Prerequisites:**
- Node.js 14+ and npm

**Installation:**
```bash
# Install globally
npm install -g claude-boost@beta

# Or install locally in project
npm install claude-boost@beta

# Verify installation
claude-boost --version
```

**Usage:**
```bash
# Initialize Claude Code enhancements
claude-boost init

# Follow the interactive setup wizard
```

### Method 2: Python Package 🐍

**Prerequisites:**
- Python 3.8+ and pip

**Installation:**
```bash
# From source (current method)
git clone https://github.com/Ferymad/claude-boost-framework
cd claude-boost-framework
pip install ./claude-boost

# Verify installation
claude-boost --version
```

### Method 3: Manual Setup 🛠️

**For Advanced Users:**
```bash
# Clone repository
git clone https://github.com/Ferymad/claude-boost-framework
cd claude-boost-framework

# Run setup script
python claude-boost/claude_boost/cli.py init
```

---

## Platform-Specific Instructions

### Windows 🪟

**Prerequisites Check:**
```cmd
# Check Node.js
node --version

# Check Python (optional)
python --version
```

**Installation:**
```cmd
# Install via npm
npm install -g claude-boost@beta

# Or use PowerShell for Python method
pip install git+https://github.com/Ferymad/claude-boost-framework.git#subdirectory=claude-boost
```

**Troubleshooting Windows:**
- If `claude-boost` command not found, check PATH includes npm global bin directory
- For Python installation, ensure Python Scripts directory is in PATH
- Use Windows Terminal or PowerShell for best experience

### macOS 🍎

**Prerequisites Installation:**
```bash
# Install Node.js via Homebrew
brew install node

# Or install Python if needed
brew install python@3.11
```

**Installation:**
```bash
# NPM method
npm install -g claude-boost@beta

# Python method
pip3 install git+https://github.com/Ferymad/claude-boost-framework.git#subdirectory=claude-boost
```

**Troubleshooting macOS:**
- If permission denied, use `sudo npm install -g claude-boost@beta`
- For Zsh users, ensure npm global bin is in PATH: `echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.zshrc`

### Linux 🐧

**Prerequisites Installation:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install nodejs npm python3-pip

# RHEL/CentOS/Fedora
sudo dnf install nodejs npm python3-pip

# Arch Linux
sudo pacman -S nodejs npm python-pip
```

**Installation:**
```bash
# NPM method (preferred)
npm install -g claude-boost@beta

# Python method
pip3 install git+https://github.com/Ferymad/claude-boost-framework.git#subdirectory=claude-boost --user
```

**Troubleshooting Linux:**
- Add npm global bin to PATH: `echo 'PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc`
- For Python user installs, ensure `~/.local/bin` is in PATH

---

## Post-Installation Setup

### 1. Verify Installation
```bash
# Check version and basic functionality
claude-boost --version
claude-boost --help

# Verify templates are available
claude-boost init --dry-run
```

### 2. Initialize Project
```bash
# Navigate to your project directory
cd your-project

# Run initialization wizard
claude-boost init

# Follow interactive prompts for:
# - Project type detection
# - Feature selection
# - Template customization
```

### 3. Verify Setup
```bash
# Check that files were created
ls -la .claude/

# Verify PROJECT_INDEX.json generation
ls -la PROJECT_INDEX.json

# Test a basic command
claude
> /fresh
```

---

## What Gets Installed

### Files Created in Your Project:
```
your-project/
├── .claude/
│   ├── CLAUDE.md              # Project memory & conventions
│   ├── agents/                # 9 specialized AI agents
│   │   ├── blind-validator.md
│   │   ├── code-reviewer.md
│   │   ├── debugger.md
│   │   ├── test-runner.md
│   │   └── [5 more...]
│   ├── commands/              # Custom slash commands
│   │   ├── cleanup.md
│   │   ├── fresh.md
│   │   └── validate.md
│   └── hooks/                 # Automation scripts
│       ├── project-indexer.py
│       └── session-manager.py
├── PROJECT_INDEX.json         # Auto-generated (gitignored)
└── .gitignore                # Updated with Claude Code entries
```

### Global CLI Tool:
- `claude-boost` command available system-wide
- Supports `init`, `update`, `status`, and other commands
- Automatic fallback from Node.js to Python if needed

---

## Configuration Options

### Interactive Setup
The `claude-boost init` wizard will ask about:

1. **Project Type**
   - Python, JavaScript/TypeScript, Go, Rust, etc.
   - Multi-language projects
   - Framework-specific optimizations

2. **Features to Enable**
   - Project indexing system
   - Blind validation pattern  
   - Session continuity
   - Advanced hook workflows

3. **Team Settings**
   - Shared agent configurations
   - Team conventions
   - Git integration preferences

### Manual Configuration
Edit `.claude/settings.json` after installation:
```json
{
  "project": {
    "name": "My Project",
    "type": "javascript",
    "indexing": {
      "enabled": true,
      "excludePatterns": ["node_modules", "dist"]
    }
  },
  "features": {
    "blindValidation": true,
    "sessionContinuity": true,
    "autoHooks": true
  }
}
```

---

## Updating

### NPM Updates
```bash
# Check for updates
npm outdated -g claude-boost

# Update to latest beta
npm update -g claude-boost@beta

# Update project templates
claude-boost update
```

### Python Updates
```bash
# Reinstall from latest source
pip install --upgrade git+https://github.com/Ferymad/claude-boost-framework.git#subdirectory=claude-boost
```

---

## Troubleshooting

### Common Issues

#### "command not found: claude-boost"
**Solution:**
```bash
# Check if npm global bin is in PATH
echo $PATH | grep -o "$(npm config get prefix)/bin" || echo "Missing from PATH"

# Add to PATH (bash/zsh)
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### "Permission denied" during npm install
**Solution:**
```bash
# Configure npm to use different directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile

# Then install
npm install -g claude-boost@beta
```

#### Templates not copying correctly
**Solution:**
```bash
# Verify package contents
npm ls -g claude-boost@beta

# Manually reinitialize
claude-boost init --force

# Check file permissions
ls -la .claude/
```

#### Python fallback not working
**Solution:**
```bash
# Verify Python installation
python3 --version
which python3

# Check if cli.py is executable
ls -la $(npm root -g)/claude-boost/claude_boost/cli.py

# Manual Python execution
python3 $(npm root -g)/claude-boost/claude_boost/cli.py init
```

### Getting Help

#### Built-in Help
```bash
# General help
claude-boost --help

# Command-specific help
claude-boost init --help
claude-boost update --help
```

#### Community Support
- **GitHub Issues**: [Report bugs or request features](https://github.com/Ferymad/claude-boost-framework/issues)
- **Discussions**: [Community discussions and Q&A](https://github.com/Ferymad/claude-boost-framework/discussions)
- **Documentation**: [Full documentation](https://github.com/Ferymad/claude-boost-framework#readme)

#### Debug Mode
```bash
# Run with debug information
DEBUG=claude-boost* claude-boost init

# Verbose output
claude-boost init --verbose

# Dry run to see what would be done
claude-boost init --dry-run
```

---

## Beta Testing Feedback

We're actively collecting feedback to improve Claude Boost. Please help us by:

### Reporting Issues
1. **Installation Problems**: Platform, Node.js/Python versions, error messages
2. **Template Issues**: Which templates, what went wrong, expected behavior
3. **Performance Concerns**: Slow operations, memory usage, responsiveness
4. **Feature Requests**: What would make your workflow better

### Success Stories
- **Productivity Improvements**: Time saved, workflow enhancements
- **Quality Benefits**: Fewer bugs, better code organization
- **Team Collaboration**: How it helps your team work together

### Testing Checklist
- [ ] Installation works on your platform
- [ ] Templates generate correctly
- [ ] Basic Claude Code integration functions
- [ ] Project indexing system works with your codebase
- [ ] Commands and hooks execute successfully

**Feedback Methods:**
- GitHub Issues (preferred for bugs)
- GitHub Discussions (for general feedback)
- Email: beta@claude-boost-framework.dev (coming soon)

---

## Next Steps

After installation:

1. **Read the Quick Start**: Check the README.md for workflow examples
2. **Try the Commands**: Use `/fresh`, `/cleanup`, `/validate` in Claude Code
3. **Explore Agents**: Try the code-reviewer and validator agents
4. **Join the Community**: Participate in discussions and provide feedback
5. **Share Your Experience**: Help others by documenting your setup process

**Happy coding with Claude Boost!** 🚀

---

*Installation guide updated: 2025-08-31*  
*Version: 0.9.0-beta*  
*For the latest instructions, visit: https://github.com/Ferymad/claude-boost-framework*