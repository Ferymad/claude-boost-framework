# 🪟 Windows Setup Guide for Claude Code Boost

This guide helps Windows users set up Claude Code Boost successfully on PowerShell, Command Prompt, and WSL.

## 🚀 Quick Setup (Most Users)

```powershell
# Step 1: Install Python (if not already installed)
# Option A: Microsoft Store (Recommended)
# Search "Python" in Microsoft Store and install Python 3.11+

# Option B: Official Download
# Visit https://python.org/downloads and download latest Python

# Step 2: Install Claude Code Boost
npx claude-boost init
```

## ⚠️ Troubleshooting Common Issues

### Issue 1: "python3 is not recognized"

**Solution**: Windows uses `python` or `py` instead of `python3`

```powershell
# Check if Python is installed
python --version
# or
py --version

# If neither work, install Python first
```

### Issue 2: Python Not Found

**Error**: `❌ Error: Python not found`

**Solutions**:

1. **Microsoft Store** (Easiest):
   - Open Microsoft Store
   - Search "Python"
   - Install Python 3.11 or newer

2. **Official Download**:
   - Visit https://python.org/downloads
   - Download latest Python for Windows
   - **Important**: Check "Add Python to PATH" during installation

3. **Package Managers**:
   ```powershell
   # Chocolatey
   choco install python

   # Scoop
   scoop install python

   # Winget
   winget install Python.Python.3.11
   ```

### Issue 3: PATH Issues

**Error**: Commands work in some terminals but not others

**Solution**: Add Python to system PATH manually

1. Find Python installation:
   ```powershell
   where python
   # or
   where py
   ```

2. Add to PATH:
   - Open "Environment Variables" in Windows Settings
   - Add Python installation directory to PATH
   - Restart terminal

### Issue 4: PowerShell Execution Policy

**Error**: `execution of scripts is disabled on this system`

**Solution**:
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy to allow scripts (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🖥️ Environment-Specific Instructions

### PowerShell (Recommended)

```powershell
# Works with both Windows PowerShell and PowerShell Core
npx claude-boost init

# Verify installation
ls .claude
cat CLAUDE.md
```

### Command Prompt (CMD)

```cmd
REM Same command works
npx claude-boost init

REM Alternative: Use batch wrapper directly
claude-boost\claude_boost\cli.cmd init
```

### WSL (Windows Subsystem for Linux)

```bash
# WSL uses Linux commands
sudo apt update
sudo apt install python3 python3-pip

# Then install normally
npx claude-boost init
```

## ✅ Verification Steps

After installation, verify everything works:

```powershell
# 1. Check Claude Code Boost files were created
ls .claude/

# 2. Verify Python CLI works directly
python .claude/hooks/project-indexer.py

# 3. Test Claude Code integration
claude
> /fresh
```

Expected output:
```
✅ Generated PROJECT_INDEX.json (X files analyzed)
✅ Claude Code Boost v1.0.1 setup complete
```

## 🔧 Advanced Configuration

### Custom Python Installation

If you have multiple Python versions:

```powershell
# Specify Python version for the project
# Edit .claude/settings.json
{
  "pythonPath": "C:\\Python311\\python.exe"
}
```

### WSL Integration

For mixed Windows/WSL development:

```powershell
# In Windows PowerShell
npx claude-boost init

# In WSL, symlink to Windows installation
ln -s /mnt/c/path/to/your/project/.claude ~/.claude-windows
```

## 🆘 Still Having Issues?

### Common Error Messages

| Error | Solution |
|-------|----------|
| `'python3' is not recognized` | Use `python` or `py` command |
| `Module not found: setuptools` | `pip install setuptools` |
| `Permission denied` | Run PowerShell as Administrator |
| `Execution policy` | `Set-ExecutionPolicy RemoteSigned` |

### Getting Help

1. **Check Python Installation**:
   ```powershell
   python --version
   pip --version
   ```

2. **Enable Verbose Logging**:
   ```powershell
   $env:DEBUG="claude-boost"
   npx claude-boost init
   ```

3. **Report Issues**:
   - GitHub: https://github.com/Ferymad/claude-boost-framework/issues
   - Include: Windows version, PowerShell version, Python version, error message

## 🎯 Windows-Specific Features

### Performance Optimizations

```powershell
# Exclude project directories from Windows Defender scanning
# for better performance (optional)
Add-MpPreference -ExclusionPath "C:\YourProjects"
```

### Integration with Windows Terminal

Add to Windows Terminal settings for better experience:

```json
{
  "profiles": {
    "defaults": {
      "startingDirectory": "C:\\YourProjects"
    }
  }
}
```

---

**Note**: This guide is specific to Windows environments. For macOS/Linux, see the main README.md installation instructions.