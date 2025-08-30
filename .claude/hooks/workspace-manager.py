#!/usr/bin/env python3
"""
Fundamental workspace isolation system
Automatically redirects development work to clean workspace
This prevents repository clutter at the most fundamental level.
"""
import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

class WorkspaceManager:
    def __init__(self):
        self.project_root = Path.cwd()
        self.workspace_root = self.project_root / ".workspace"
        self.ensure_workspace_exists()
    
    def ensure_workspace_exists(self):
        """Ensure workspace structure exists"""
        if not self.workspace_root.exists():
            self.setup_workspace()
    
    def setup_workspace(self):
        """Create isolated development workspace"""
        # Create workspace directories
        dirs = [
            "current",      # Current development work
            "experiments",  # Test files and prototypes  
            "sessions",     # Session artifacts
            "planning",     # Roadmaps and planning docs
            "temp",         # Temporary files
            "archives"      # Old development work
        ]
        
        for dir_name in dirs:
            (self.workspace_root / dir_name).mkdir(parents=True, exist_ok=True)
        
        # Create symlinks to real project structures
        project_links = [
            ("CLAUDE.md", "CLAUDE.md"),
            ("README.md", "README.md"),
            ("PROJECT_INDEX.json", "PROJECT_INDEX.json"),
            ("claude-boost", "claude-boost")
        ]
        
        for workspace_name, project_path in project_links:
            workspace_path = self.workspace_root / workspace_name
            project_full_path = self.project_root / project_path
            
            if project_full_path.exists() and not workspace_path.exists():
                try:
                    os.symlink(f"../{project_path}", workspace_path)
                except OSError:
                    # Windows fallback: create text file with path
                    with open(workspace_path, 'w') as f:
                        f.write(f"SYMLINK_TARGET: {project_full_path}")
    
    def should_redirect_file(self, file_path):
        """Check if file should be redirected to workspace"""
        if not file_path:
            return False, ""
            
        filename = os.path.basename(file_path)
        
        # Files that should NEVER be in project root
        problematic_patterns = [
            'test_*.py',
            'experiment_*.py', 
            'debug_*.py',
            'temp_*.py',
            'scratch_*.py',
            'SESSION_*.md',
            '*_SUMMARY.md',
            '*_REPORT.md',
            '*_ROADMAP.md',
            '*_NOTES.md',
            'temp_*.txt',
            'debug_*.txt',
            'output_*.txt'
        ]
        
        # Only redirect files that would be created in project root
        if '/' not in file_path or file_path.startswith('./'):
            import fnmatch
            for pattern in problematic_patterns:
                if fnmatch.fnmatch(filename, pattern):
                    # Determine appropriate workspace directory
                    if any(prefix in filename for prefix in ['test_', 'experiment_', 'debug_', 'scratch_']):
                        new_path = f".workspace/experiments/{filename}"
                    elif filename.endswith(('_SUMMARY.md', '_REPORT.md', '_NOTES.md')):
                        new_path = f".workspace/sessions/{filename}"
                    elif filename.endswith('_ROADMAP.md'):
                        new_path = f".workspace/planning/{filename}"
                    else:
                        new_path = f".workspace/temp/{filename}"
                    
                    return True, new_path
        
        return False, ""
    
    def redirect_file_operation(self, tool_input):
        """Redirect problematic file operations to workspace"""
        file_path = tool_input.get('file_path', '')
        should_redirect, new_path = self.should_redirect_file(file_path)
        
        if should_redirect:
            # Ensure target directory exists
            target_dir = os.path.dirname(new_path)
            os.makedirs(target_dir, exist_ok=True)
            
            return new_path, f"🔄 REDIRECTED: {file_path} → {new_path} (keeping repo clean)"
        
        return file_path, ""

def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        
        # Only process file creation/modification tools
        if tool_name in ['Write', 'Edit', 'MultiEdit']:
            manager = WorkspaceManager()
            tool_input = input_data.get('tool_input', {})
            original_path = tool_input.get('file_path', '')
            
            redirected_path, redirect_message = manager.redirect_file_operation(tool_input)
            
            if redirected_path != original_path:
                # Modify the tool input to use workspace location
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "additionalContext": redirect_message,
                        "modifiedToolInput": {
                            **tool_input,
                            "file_path": redirected_path
                        }
                    }
                }))
                return
                
        # No redirection needed - allow operation
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": "✅ Workspace isolation active"
            }
        }))
        
    except Exception as e:
        # Never break the workflow - fail silently with context
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": f"⚠️ Workspace manager warning: {str(e)}"
            }
        }))

if __name__ == "__main__":
    main()