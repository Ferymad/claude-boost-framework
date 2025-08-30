#!/usr/bin/env python3
"""
Session-specific workspace management
Creates isolated workspace for each development session
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

def create_session_workspace():
    """Create isolated workspace for this session"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    workspace_root = Path(".workspace")
    session_dir = workspace_root / "sessions" / f"session-{timestamp}"
    
    # Create session directories
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / "work").mkdir(exist_ok=True)
    (session_dir / "experiments").mkdir(exist_ok=True)
    (session_dir / "temp").mkdir(exist_ok=True)
    (session_dir / "planning").mkdir(exist_ok=True)
    
    # Create session info file
    session_info = {
        "session_id": f"session-{timestamp}",
        "started_at": datetime.now().isoformat(),
        "workspace_dir": str(session_dir),
        "purpose": "Isolated development session workspace",
        "rules": [
            "All experimental work goes here",
            "Real project files accessed via symlinks", 
            "Session automatically archived after 7 days",
            "No clutter files created in project root"
        ]
    }
    
    with open(session_dir / "session-info.json", 'w') as f:
        json.dump(session_info, f, indent=2)
    
    # Create quick access symlinks in session
    project_files = ["CLAUDE.md", "PROJECT_INDEX.json", "README.md"]
    for file_name in project_files:
        source = Path("../../../") / file_name  # Relative to session dir
        target = session_dir / file_name
        if not target.exists():
            try:
                os.symlink(source, target)
            except OSError:
                # Fallback for Windows - create reference file
                with open(target, 'w') as f:
                    f.write(f"# Reference to: {source}\n")
                    f.write(f"# Use: cat {source}\n")
    
    return session_dir, f"session-{timestamp}"

def main():
    try:
        input_data = json.load(sys.stdin)
        hook_event = input_data.get('hook_event_name', '')
        
        if hook_event == "SessionStart":
            session_dir, session_id = create_session_workspace()
            
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": f"""
🏗️ SESSION WORKSPACE CREATED: {session_dir}

📁 Workspace Structure:
  • .workspace/sessions/{session_id}/
    ├── work/         # Current session work
    ├── experiments/  # Test files and prototypes
    ├── temp/         # Temporary files
    ├── planning/     # Session planning docs
    └── session-info.json

🔗 Project access via symlinks in .workspace/
⚠️  All development artifacts automatically isolated
✅ Repository root protected from clutter

Use workspace commands: /dev-start, /experiment, /test
                    """,
                    "sessionWorkspace": str(session_dir),
                    "sessionId": session_id
                }
            }))
        else:
            # For other events, just confirm workspace is active
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": hook_event,
                    "additionalContext": "🛡️ Workspace isolation system active"
                }
            }))
            
    except Exception as e:
        # Never break the workflow
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"⚠️ Session workspace warning: {str(e)}"
            }
        }))

if __name__ == "__main__":
    main()