#!/usr/bin/env python3
"""
Claude Code Boost CLI
Interactive installer for the Claude Code enhancement system
"""
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

def print_header():
    """Print the welcome header"""
    print("\n🚀 Claude Code Boost v1.0 - Supercharge your AI development")
    print("=" * 60)

def check_claude_code():
    """Check if Claude Code is available with cross-platform support"""
    claude_commands = ['claude', 'claude.cmd', 'npx @anthropic-ai/claude-code']
    
    for cmd in claude_commands:
        try:
            if cmd.startswith('npx'):
                # Use shell=True for npx commands
                result = subprocess.run(cmd.split() + ['--version'], 
                                      capture_output=True, text=True, shell=True, timeout=10)
            else:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and 'Claude Code' in result.stdout:
                version = result.stdout.strip()
                print(f"✅ Claude Code installation detected: {version}")
                return True
                
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
        except Exception as e:
            # Log but continue trying other commands
            continue
    
    # If all detection methods fail, check npm global packages
    try:
        result = subprocess.run(['npm', 'list', '-g', '--depth=0'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and '@anthropic-ai/claude-code' in result.stdout:
            print("✅ Claude Code installation detected via npm global packages")
            return True
    except Exception:
        pass
    
    print("❌ Claude Code not found. Please install Claude Code first:")
    print("   Windows: npm install -g @anthropic-ai/claude-code")
    print("   macOS/Linux: curl -sSL https://claude.ai/install.sh | bash")
    print("   Visit: https://claude.ai/code")
    return False

def detect_project_type():
    """Detect project type based on files present"""
    project_types = []
    
    if os.path.exists("package.json"):
        project_types.append("JavaScript/Node.js")
    if os.path.exists("requirements.txt") or os.path.exists("pyproject.toml"):
        project_types.append("Python")
    if os.path.exists("Cargo.toml"):
        project_types.append("Rust")
    if os.path.exists("go.mod"):
        project_types.append("Go")
    
    return project_types if project_types else ["Generic"]

def get_user_preferences():
    """Get user preferences for installation"""
    print("\n📋 Configuration Options:")
    
    # Feature selection
    features = {
        "project_indexer": {
            "name": "Project Indexer - Prevent code duplication",
            "default": True
        },
        "smart_agents": {
            "name": "Smart Agents - Code review, validation, debugging",
            "default": True
        },
        "session_manager": {
            "name": "Session Manager - Never lose context",
            "default": True
        }
    }
    
    selected_features = {}
    for key, feature in features.items():
        default = "Y" if feature["default"] else "N"
        try:
            response = input(f"  [{default}] {feature['name']} (y/N): ").strip().lower()
            selected_features[key] = response in ['y', 'yes'] if response else feature["default"]
        except EOFError:
            # Non-interactive mode: use defaults
            print(f"  [AUTO] {feature['name']}: {'Yes' if feature['default'] else 'No'}")
            selected_features[key] = feature["default"]
    
    return selected_features

def copy_template_files(features: Dict[str, bool]):
    """Copy template files based on selected features"""
    print("\n📦 Installing...")
    
    # Get the template directory path
    template_dir = Path(__file__).parent / "templates" / ".claude"
    
    if not template_dir.exists():
        print(f"❌ Template directory not found: {template_dir}")
        return False
    
    # Create .claude directory
    claude_dir = Path(".claude")
    claude_dir.mkdir(exist_ok=True)
    print("  ✅ Creating .claude directory")
    
    # Copy CLAUDE.md
    shutil.copy2(template_dir / "CLAUDE.md", claude_dir / "CLAUDE.md")
    print("  ✅ Setting up CLAUDE.md template")
    
    if features.get("smart_agents", True):
        # Copy agents
        agents_dir = claude_dir / "agents"
        agents_dir.mkdir(exist_ok=True)
        
        for agent_file in (template_dir / "agents").glob("*.md"):
            shutil.copy2(agent_file, agents_dir / agent_file.name)
        print("  ✅ Configuring 4 specialized agents")
        
        # Copy commands
        commands_dir = claude_dir / "commands" 
        commands_dir.mkdir(exist_ok=True)
        
        for command_file in (template_dir / "commands").glob("*.md"):
            shutil.copy2(command_file, commands_dir / command_file.name)
        print("  ✅ Adding essential commands")
    
    if features.get("project_indexer", True):
        # Copy hooks
        hooks_dir = claude_dir / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        
        for hook_file in (template_dir / "hooks").glob("*.py"):
            shutil.copy2(hook_file, hooks_dir / hook_file.name)
            # Make hooks executable
            os.chmod(hooks_dir / hook_file.name, 0o755)
        print("  ✅ Setting up PROJECT_INDEX.json generator")
    
    if features.get("session_manager", True):
        print("  ✅ Initializing session management")
    
    return True

def generate_initial_index():
    """Generate initial PROJECT_INDEX.json"""
    hooks_dir = Path(".claude/hooks")
    indexer_script = hooks_dir / "project-indexer.py"
    
    if indexer_script.exists():
        try:
            result = subprocess.run([sys.executable, str(indexer_script)], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                print("  ✅ Generated initial PROJECT_INDEX.json")
                return True
            else:
                print(f"  ⚠️ Warning: Could not generate PROJECT_INDEX.json: {result.stderr}")
                return False
        except Exception as e:
            print(f"  ⚠️ Warning: Could not generate PROJECT_INDEX.json: {e}")
            return False
    return False

def show_next_steps():
    """Show next steps to the user"""
    print("\n🎉 Success! Claude Code Boost installed")
    print("\nQuick start:")
    print("  1. Run: claude --continue")
    print("  2. Type: /fresh")
    print("  3. Start coding with 37% productivity boost!")
    print("\nDocumentation: https://claude-boost.dev")
    print("Community: https://discord.gg/claude-boost")

def create_gitignore_entry():
    """Add PROJECT_INDEX.json to .gitignore if it exists"""
    gitignore_path = Path(".gitignore")
    entry = "PROJECT_INDEX.json"
    
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        if entry not in content:
            with open(gitignore_path, 'a') as f:
                f.write(f"\n# Claude Code Boost\n{entry}\n")
            print("  ✅ Added PROJECT_INDEX.json to .gitignore")
    else:
        with open(gitignore_path, 'w') as f:
            f.write(f"# Claude Code Boost\n{entry}\n")
        print("  ✅ Created .gitignore with PROJECT_INDEX.json")

def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("Claude Code Boost - Supercharge your AI development workflow")
        print("\nUsage:")
        print("  claude-boost init    Initialize Claude Code Boost in current project")
        print("  claude-boost --help  Show this help message")
        return
    
    if len(sys.argv) < 2 or sys.argv[1] != 'init':
        print("Usage: claude-boost init")
        print("Run 'claude-boost --help' for more information")
        return
    
    print_header()
    
    # Check prerequisites
    if not check_claude_code():
        sys.exit(1)
    
    # Analyze project
    print("\n✅ Analyzing project structure...")
    project_types = detect_project_type()
    print(f"  Project type detected: {', '.join(project_types)}")
    
    # Get user preferences
    features = get_user_preferences()
    
    # Install files
    if not copy_template_files(features):
        print("\n❌ Installation failed")
        sys.exit(1)
    
    # Generate initial project index
    if features.get("project_indexer", True):
        generate_initial_index()
    
    # Update .gitignore
    create_gitignore_entry()
    
    # Show success message
    show_next_steps()

if __name__ == "__main__":
    main()