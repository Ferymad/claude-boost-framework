#!/usr/bin/env python3
"""
Session state management for Claude Code
Saves and restores session context for continuity
"""
import json
import sys
import os
from datetime import datetime

def save_session_state(session_data):
    """Save current session state"""
    state = {
        'timestamp': datetime.now().isoformat(),
        'session_id': session_data.get('session_id'),
        'current_task': 'Task completion and session cleanup',
        'context_summary': 'Session ending - state preserved for continuity',
        'next_steps': [
            'Use /fresh command to restore context',
            'Continue with planned development tasks',
            'Reference PROJECT_INDEX.json for current state'
        ],
        'project_status': {
            'last_modified_files': [],
            'active_features': [],
            'pending_tests': [],
            'known_issues': []
        }
    }
    
    # Save to .claude directory
    os.makedirs('.claude/state', exist_ok=True)
    with open('.claude/state/last_session.json', 'w') as f:
        json.dump(state, f, indent=2)
    
    print("💾 Session state saved for continuity", file=sys.stderr)

def load_session_state():
    """Load previous session state"""
    try:
        with open('.claude/state/last_session.json', 'r') as f:
            state = json.load(f)
        return state
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    try:
        input_data = json.load(sys.stdin)
        hook_event = input_data.get('hook_event_name', '')
        
        if hook_event == 'SessionEnd':
            save_session_state(input_data)
        elif hook_event == 'SessionStart':
            state = load_session_state()
            if state:
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": f"""
Previous session context restored:
- Last session: {state['timestamp']}
- Task: {state['current_task']}
- Next steps: {', '.join(state['next_steps'])}

Use /fresh to fully restore project context.
                        """
                    }
                }))
    except Exception as e:
        print(f"Session state error: {e}", file=sys.stderr)