#!/usr/bin/env node

// Node.js wrapper for the Python CLI
// This allows npx claude-boost to work seamlessly

const { spawn } = require('child_process');
const path = require('path');

function runPythonCLI() {
    // Try to find Python
    const pythonCommands = ['python3', 'python'];
    let pythonCmd = 'python3';
    
    // Get the path to the Python CLI script
    const pythonScript = path.join(__dirname, 'cli.py');
    
    // Pass through all arguments
    const args = [pythonScript, ...process.argv.slice(2)];
    
    // Spawn the Python process
    const pythonProcess = spawn(pythonCmd, args, {
        stdio: 'inherit',
        shell: true
    });
    
    pythonProcess.on('error', (err) => {
        if (err.code === 'ENOENT') {
            // Try with 'python' instead
            const fallbackProcess = spawn('python', args, {
                stdio: 'inherit',
                shell: true
            });
            
            fallbackProcess.on('error', (fallbackErr) => {
                console.error('❌ Error: Python not found. Please install Python 3.8 or higher.');
                console.error('   Visit: https://python.org/downloads');
                process.exit(1);
            });
            
            fallbackProcess.on('close', (code) => {
                process.exit(code);
            });
        } else {
            console.error('❌ Error running Claude Code Boost:', err.message);
            process.exit(1);
        }
    });
    
    pythonProcess.on('close', (code) => {
        process.exit(code);
    });
}

// Show help if no Python available
function showNodejsHelp() {
    console.log('🚀 Claude Code Boost v1.0');
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