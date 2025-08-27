# Claude Code Boost Installation Script for Windows
# Usage: irm https://claude-boost.dev/install.ps1 | iex

$ErrorActionPreference = "Stop"

# Colors for output
$Red = [System.ConsoleColor]::Red
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Blue = [System.ConsoleColor]::Blue

function Print-Header {
    Write-Host ""
    Write-Host "🚀 Claude Code Boost v1.0 - Installation" -ForegroundColor $Blue
    Write-Host "========================================" -ForegroundColor $Blue
    Write-Host ""
}

function Write-Error-Message {
    param([string]$Message)
    Write-Host "❌ Error: $Message" -ForegroundColor $Red
    exit 1
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor $Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor $Blue
}

# Check if command exists
function Test-Command {
    param([string]$Command)
    try {
        if (Get-Command $Command -ErrorAction SilentlyContinue) {
            return $true
        }
        return $false
    } catch {
        return $false
    }
}

# Detect package manager and install method
function Get-InstallMethod {
    if (Test-Command "python") {
        return @{
            Method = "pip"
            Command = "pip install claude-boost"
            Description = "Python/pip"
        }
    } elseif (Test-Command "node") {
        if (Test-Command "npm") {
            return @{
                Method = "npm"
                Command = "npm install -g claude-boost"
                Description = "Node.js/npm"
            }
        } elseif (Test-Command "npx") {
            return @{
                Method = "npx"
                Command = "npx claude-boost@latest init"
                Description = "Node.js/npx"
            }
        }
    }
    
    Write-Error-Message "No supported package manager found. Please install Python 3 or Node.js first."
}

# Install Claude Code Boost
function Install-ClaudeBoost {
    param($InstallInfo)
    
    Write-Info "Installing Claude Code Boost using $($InstallInfo.Description)..."
    
    try {
        switch ($InstallInfo.Method) {
            "pip" {
                python -m pip install claude-boost
                if ($LASTEXITCODE -ne 0) { throw "pip install failed" }
                Write-Success "Claude Code Boost installed via pip"
                Write-Host ""
                Write-Host "To initialize in your project:"
                Write-Host "  cd your-project\"
                Write-Host "  claude-boost init"
            }
            "npm" {
                npm install -g claude-boost
                if ($LASTEXITCODE -ne 0) { throw "npm install failed" }
                Write-Success "Claude Code Boost installed via npm"
                Write-Host ""
                Write-Host "To initialize in your project:"
                Write-Host "  cd your-project\"
                Write-Host "  claude-boost init"
            }
            "npx" {
                Write-Success "Ready to use Claude Code Boost via npx"
                Write-Host ""
                Write-Host "To initialize in your project:"
                Write-Host "  cd your-project\"
                Write-Host "  npx claude-boost init"
            }
        }
    } catch {
        Write-Error-Message "Failed to install Claude Code Boost: $_"
    }
}

# Main installation flow
function Main {
    Print-Header
    
    Write-Info "Detecting installation method..."
    $InstallInfo = Get-InstallMethod
    Write-Success "Using $($InstallInfo.Description) for installation"
    
    # Check for Claude Code
    if (-not (Test-Command "claude")) {
        Write-Warning "Claude Code not found. Please install Claude Code first:"
        Write-Host "  Visit: https://claude.ai/code"
        Write-Host ""
        Write-Host "You can still install Claude Code Boost now and use it later."
        $response = Read-Host "Continue installation? (y/N)"
        if ($response -notmatch "^[Yy]$") {
            exit 0
        }
    } else {
        Write-Success "Claude Code detected"
    }
    
    Install-ClaudeBoost $InstallInfo
    
    Write-Host ""
    Write-Success "Installation complete!"
    Write-Host ""
    Write-Host "🎯 Next steps:"
    Write-Host "1. Navigate to your project directory"
    Write-Host "2. Run: claude-boost init (or npx claude-boost init)"
    Write-Host "3. Follow the interactive setup"
    Write-Host "4. Start using: claude --continue && /fresh"
    Write-Host ""
    Write-Host "📚 Documentation: https://claude-boost.dev"
    Write-Host "💬 Community: https://discord.gg/claude-boost"
}

# Run main function
Main