#!/usr/bin/env python3
"""
Token usage tracking and analytics for Claude Code
Monitors usage patterns for optimization opportunities
"""
import json
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict


def log_tool_usage(input_data):
    """Log tool usage for analytics"""
    try:
        # Extract relevant information
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'tool_name': input_data.get('tool_name', 'unknown'),
            'hook_event': input_data.get('hook_event_name', ''),
            'session_id': input_data.get('session_id', ''),
            'tool_input_size': len(str(input_data.get('tool_input', {}))),
            'command': input_data.get('tool_input', {}).get('command', '')[:100] if input_data.get('tool_input', {}).get('command') else ''
        }
        
        # Create analytics directory
        os.makedirs('.claude/analytics', exist_ok=True)
        
        # Append to usage log (JSONL format for easy processing)
        with open('.claude/analytics/usage.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
            
        return True
        
    except Exception as e:
        # Silent failure for analytics - don't break normal operations
        with open('.claude/analytics/errors.log', 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} - Token tracker error: {e}\n")
        return False


def generate_usage_report():
    """Generate usage analytics report"""
    try:
        if not os.path.exists('.claude/analytics/usage.jsonl'):
            return "No usage data available yet."
        
        # Read usage data
        entries = []
        with open('.claude/analytics/usage.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        
        if not entries:
            return "No valid usage data found."
        
        # Analyze usage patterns
        tool_usage = defaultdict(int)
        hook_usage = defaultdict(int)
        daily_usage = defaultdict(int)
        session_tools = defaultdict(set)
        
        for entry in entries:
            tool_usage[entry.get('tool_name', 'unknown')] += 1
            hook_event = entry.get('hook_event', '')
            if hook_event:
                hook_usage[hook_event] += 1
            
            # Daily usage
            date = entry.get('timestamp', '')[:10]
            daily_usage[date] += 1
            
            # Session analysis
            session_id = entry.get('session_id', '')
            if session_id:
                session_tools[session_id].add(entry.get('tool_name', 'unknown'))
        
        # Generate report
        report = f"""# Usage Analytics Report
Generated: {datetime.now().isoformat()}
Total Events: {len(entries)}

## Tool Usage Summary
{chr(10).join(f"  {tool}: {count} times" for tool, count in sorted(tool_usage.items(), key=lambda x: x[1], reverse=True))}

## Hook Events Summary  
{chr(10).join(f"  {hook}: {count} times" for hook, count in sorted(hook_usage.items(), key=lambda x: x[1], reverse=True)) if hook_usage else "  No hook events recorded"}

## Daily Usage (Last 7 Days)
{chr(10).join(f"  {date}: {count} events" for date, count in sorted(daily_usage.items())[-7:])}

## Session Analysis
- Average tools per session: {sum(len(tools) for tools in session_tools.values()) / len(session_tools) if session_tools else 0:.1f}
- Total sessions tracked: {len(session_tools)}
- Most common tool combinations: {list(tool_usage.keys())[:3]}

## Optimization Opportunities
- Consider optimizing workflows for top tools: {list(tool_usage.keys())[:2]}
- Hook performance: {'Good' if len(hook_usage) > 0 else 'No hooks active'}
"""
        
        return report
        
    except Exception as e:
        return f"Error generating usage report: {e}"


def cleanup_old_logs(days_to_keep=30):
    """Clean up old analytics logs"""
    try:
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Read current logs
        if not os.path.exists('.claude/analytics/usage.jsonl'):
            return
            
        recent_entries = []
        with open('.claude/analytics/usage.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entry_date = datetime.fromisoformat(entry.get('timestamp', '').replace('Z', '+00:00'))
                    if entry_date > cutoff_date:
                        recent_entries.append(line)
                except (json.JSONDecodeError, ValueError):
                    continue
        
        # Write back only recent entries
        with open('.claude/analytics/usage.jsonl', 'w', encoding='utf-8') as f:
            f.writelines(recent_entries)
            
    except Exception as e:
        # Silent failure - don't break operations
        pass


def main():
    """Main hook execution"""
    try:
        # Handle different hook events
        if len(sys.argv) > 1 and sys.argv[1] == '--report':
            print(generate_usage_report())
            return
            
        if len(sys.argv) > 1 and sys.argv[1] == '--cleanup':
            cleanup_old_logs()
            print("Analytics logs cleaned up")
            return
        
        # Normal hook processing
        input_data = json.load(sys.stdin)
        success = log_tool_usage(input_data)
        
        # Optional output for debugging (normally silent)
        if os.environ.get('CLAUDE_DEBUG_ANALYTICS') == '1':
            output = {
                "hookSpecificOutput": {
                    "hookEventName": input_data.get('hook_event_name', 'TokenTracker'),
                    "additionalContext": f"📊 Usage logged: {input_data.get('tool_name', 'unknown')}" if success else "⚠️ Analytics logging failed"
                }
            }
            print(json.dumps(output))
        
    except Exception as e:
        # Silent failure for analytics
        if os.environ.get('CLAUDE_DEBUG_ANALYTICS') == '1':
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "TokenTracker",
                    "additionalContext": f"Analytics error: {e}"
                }
            }
            print(json.dumps(output))


if __name__ == "__main__":
    main()