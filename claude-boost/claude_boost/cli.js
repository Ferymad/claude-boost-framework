#!/usr/bin/env node

// Node.js wrapper for the Python CLI
// This allows npx claude-boost to work seamlessly

const { spawn } = require('child_process');
const path = require('path');

function runPythonCLI() {
    // Cross-platform Python detection
    const isWindows = process.platform === 'win32';
    const pythonCommands = isWindows ? ['py', 'python', 'python3'] : ['python3', 'python'];
    
    // Get the path to the Python CLI script
    const pythonScript = path.join(__dirname, 'cli.py');
    
    // Pass through all arguments
    const args = [pythonScript, ...process.argv.slice(2)];
    
    // Try Python commands in order
    tryPythonCommand(pythonCommands, args, 0);
}

function tryPythonCommand(commands, args, index) {
    if (index >= commands.length) {
        console.error('❌ Error: Python not found. Please install Python 3.8 or higher.');
        console.error('   Windows: https://python.org/downloads or Microsoft Store');
        console.error('   macOS: brew install python3');
        console.error('   Linux: sudo apt install python3 (or your package manager)');
        process.exit(1);
    }
    
    const pythonCmd = commands[index];
    console.log(`🔍 Trying ${pythonCmd}...`);
    
    // Spawn the Python process
    const pythonProcess = spawn(pythonCmd, args, {
        stdio: 'inherit',
        shell: false  // Don't use shell for better cross-platform compatibility
    });
    
    pythonProcess.on('error', (err) => {
        if (err.code === 'ENOENT') {
            // Try next command
            tryPythonCommand(commands, args, index + 1);
        } else {
            console.error('❌ Error running Claude Code Boost:', err.message);
            process.exit(1);
        }
    });
    
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            process.exit(0);
        } else if (code === 127 || code === 9009) {
            // Command not found - try next
            tryPythonCommand(commands, args, index + 1);
        } else {
            process.exit(code);
        }
    });
}

// Show help if no Python available
function showNodejsHelp() {
    console.log('🧪 Claude Code Boost v0.9.0-beta');
    console.log('');
    console.log('This tool requires Python 3.8 or higher to run.');
    console.log('');
    console.log('Installation options:');
    console.log('  1. Install Python: https://python.org/downloads');
    console.log('  2. Use pip instead: pip install claude-boost');
    console.log('');
    console.log('Once Python is installed, run:');
    console.log('  npx claude-boost init');
}

// Check if this is a help request
if (process.argv.includes('--help') || process.argv.includes('-h')) {
    console.log('Claude Code Boost - Supercharge your AI development workflow');
    console.log('');
    console.log('Usage:');
    console.log('  npx claude-boost init    Initialize Claude Code Boost in current project');
    console.log('  npx claude-boost --help  Show this help message');
    console.log('');
    console.log('Alternative installation:');
    console.log('  pip install claude-boost && claude-boost init');
    process.exit(0);
}

// Run the Python CLI
runPythonCLI();