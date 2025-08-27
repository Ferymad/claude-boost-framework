#!/usr/bin/env python3
"""
Session state management for Claude Code
Saves and restores session context for continuity
"""
import json
import sys
import os
import subprocess
from datetime import datetime


def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return ""
    except:
        return ""


def get_recent_activity():
    """Get recent git activity and project status"""
    activity = {
        'recent_commits': [],
        'modified_files': [],
        'current_branch': '',
        'staged_files': [],
        'git_status': ''
    }
    
    # Get recent commits
    commits = run_command("git log --oneline -5 2>/dev/null")
    if commits:
        activity['recent_commits'] = commits.split('\n')
    
    # Get current branch
    activity['current_branch'] = run_command("git branch --show-current 2>/dev/null")
    
    # Get git status
    activity['git_status'] = run_command("git status --porcelain 2>/dev/null")
    
    # Get modified files
    modified = run_command("git diff --name-only 2>/dev/null")
    if modified:
        activity['modified_files'] = modified.split('\n')
    
    # Get staged files
    staged = run_command("git diff --cached --name-only 2>/dev/null")  
    if staged:
        activity['staged_files'] = staged.split('\n')
    
    return activity


def save_session_state(session_data):
    """Save enhanced session state with project context"""
    activity = get_recent_activity()
    
    state = {
        'timestamp': datetime.now().isoformat(),
        'session_id': session_data.get('session_id'),
        'current_task': 'Session ended - context preserved',
        'context_summary': 'Enhanced session state with git context and project status',
        'git_activity': activity,
        'next_steps': [
            'Use /fresh command to restore full project context',
            'Review PROJECT_INDEX.json for current codebase state', 
            'Check git status for any pending changes',
            'Continue with development tasks'
        ],
        'project_status': {
            'last_modified_files': activity['modified_files'],
            'staged_files': activity['staged_files'],
            'current_branch': activity['current_branch'],
            'recent_work': activity['recent_commits'][:3] if activity['recent_commits'] else []
        }
    }
    
    # Save to .claude directory
    os.makedirs('.claude/state', exist_ok=True)
    with open('.claude/state/last_session.json', 'w') as f:
        json.dump(state, f, indent=2)
    
    # Also save a backup with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'.claude/state/session_backup_{timestamp}.json', 'w') as f:
        json.dump(state, f, indent=2)

def load_session_state():
    """Load previous session state with enhanced context"""
    try:
        with open('.claude/state/last_session.json', 'r') as f:
            state = json.load(f)
        return state
    except FileNotFoundError:
        return None


def format_session_context(state):
    """Format session context for display"""
    if not state:
        return "No previous session state found."
    
    context = f"""🔄 **Session Continuity Restored**

**Previous Session**: {state['timestamp']}
**Branch**: {state.get('project_status', {}).get('current_branch', 'unknown')}

**Recent Activity**:
{chr(10).join(f"  • {commit}" for commit in state.get('project_status', {}).get('recent_work', []))}

**Modified Files**: {len(state.get('project_status', {}).get('last_modified_files', []))} files
**Staged Files**: {len(state.get('project_status', {}).get('staged_files', []))} files

**Next Steps**:
{chr(10).join(f"  • {step}" for step in state.get('next_steps', []))}

Use `/fresh` to load complete project context."""
    
    return context


if __name__ == "__main__":
    try:
        input_data = json.load(sys.stdin)
        hook_event = input_data.get('hook_event_name', '')
        
        if hook_event == 'SessionEnd':
            save_session_state(input_data)
            # Output success message
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "SessionEnd",
                    "additionalContext": "💾 Enhanced session state saved with git context and project status"
                }
            }
            print(json.dumps(output))
            
        elif hook_event == 'SessionStart':
            state = load_session_state()
            context = format_session_context(state)
            
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context
                }
            }
            print(json.dumps(output))
            
    except Exception as e:
        # Graceful degradation - don't break session start/end
        output = {
            "hookSpecificOutput": {
                "hookEventName": input_data.get('hook_event_name', 'Unknown'),
                "additionalContext": f"⚠️ Session state hook warning: {str(e)}"
            }
        }
        print(json.dumps(output))