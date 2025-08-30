#!/usr/bin/env python3
"""
Session State Manager for Claude Code Boost
Saves and restores session context for continuity
"""
import json
import sys
import os
from datetime import datetime

def save_session_state():
    """Save current session state"""
    state = {
        'timestamp': datetime.now().isoformat(),
        'context_summary': 'Session ending - state preserved for continuity',
        'next_steps': [
            'Use /fresh command to restore context',
            'Continue with planned development tasks',
            'Reference PROJECT_INDEX.json for current state'
        ]
    }
    
    # Ensure .claude/state directory exists
    os.makedirs('.claude/state', exist_ok=True)
    
    # Save state file
    with open('.claude/state/last_session.json', 'w') as f:
        json.dump(state, f, indent=2)
    
    print("💾 Session state saved for continuity")
    return state

def load_session_state():
    """Load previous session state"""
    try:
        with open('.claude/state/last_session.json', 'r') as f:
            state = json.load(f)
        return state
    except FileNotFoundError:
        return None

def main():
    try:
        input_data = json.load(sys.stdin)
        hook_event = input_data.get('hook_event_name', '')
        
        if hook_event == 'SessionEnd':
            save_session_state()
        elif hook_event == 'SessionStart':
            state = load_session_state()
            if state:
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart", 
                        "additionalContext": f"""
🔄 **Session Continuity Restored**

**Previous Session**: {state['timestamp']}

**Next Steps**:
  • Use /fresh command to restore context
  • Continue with planned development tasks
  • Reference PROJECT_INDEX.json for current state

Use `/fresh` to load complete project context."""
                    }
                }))
    except Exception as e:
        print(f"Session manager error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()