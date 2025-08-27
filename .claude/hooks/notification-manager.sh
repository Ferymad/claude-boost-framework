#!/bin/bash
# Notification and alert system for Claude Code
# Manages alerts for important events and system status

# Configuration
LOG_DIR=".claude/analytics"
NOTIFICATION_LOG="$LOG_DIR/notifications.log"
MAX_LOG_SIZE=1048576  # 1MB

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Function to log notifications
log_notification() {
    local level="$1"
    local message="$2"
    local timestamp=$(date -Iseconds 2>/dev/null || date)
    
    echo "[$timestamp] [$level] $message" >> "$NOTIFICATION_LOG"
    
    # Rotate log if too large
    if [ -f "$NOTIFICATION_LOG" ]; then
        local size=$(stat -c%s "$NOTIFICATION_LOG" 2>/dev/null || echo 0)
        if [ "$size" -gt $MAX_LOG_SIZE ]; then
            mv "$NOTIFICATION_LOG" "$NOTIFICATION_LOG.old"
            echo "[$timestamp] [INFO] Log rotated" >> "$NOTIFICATION_LOG"
        fi
    fi
}

# Function to check for critical issues
check_critical_issues() {
    local issues=""
    
    # Check if hooks are failing frequently
    if [ -f "$LOG_DIR/errors.log" ]; then
        local recent_errors=$(tail -n 10 "$LOG_DIR/errors.log" 2>/dev/null | wc -l)
        if [ "$recent_errors" -gt 5 ]; then
            issues="$issues\n- Multiple hook failures detected ($recent_errors recent errors)"
        fi
    fi
    
    # Check disk space
    local available_space=$(df . 2>/dev/null | awk 'NR==2 {print $4}' || echo 999999999)
    if [ "$available_space" -lt 1000000 ]; then  # Less than ~1GB
        issues="$issues\n- Low disk space detected"
    fi
    
    # Check if PROJECT_INDEX.json is outdated
    if [ -f "PROJECT_INDEX.json" ]; then
        local index_age=$(( $(date +%s) - $(stat -c%Y "PROJECT_INDEX.json" 2>/dev/null || echo $(date +%s)) ))
        if [ "$index_age" -gt 86400 ]; then  # Older than 24 hours
            issues="$issues\n- PROJECT_INDEX.json may be outdated"
        fi
    fi
    
    if [ -n "$issues" ]; then
        echo -e "$issues"
        return 1
    fi
    return 0
}

# Function to process hook events
process_hook_event() {
    local event_name="$1"
    local tool_name="$2"
    
    case "$event_name" in
        "PostToolUse")
            if [ "$tool_name" = "Edit" ] || [ "$tool_name" = "MultiEdit" ] || [ "$tool_name" = "Write" ]; then
                log_notification "INFO" "Project files modified - PROJECT_INDEX.json update triggered"
            fi
            ;;
        "SessionEnd")
            log_notification "INFO" "Session ended - state preserved"
            ;;
        "SessionStart")
            log_notification "INFO" "New session started - context restored"
            if ! check_critical_issues >/dev/null 2>&1; then
                local issues=$(check_critical_issues 2>/dev/null)
                log_notification "WARN" "System issues detected: $issues"
            fi
            ;;
    esac
}

# Main execution
main() {
    if [ ! -t 0 ]; then  # stdin is not a terminal
        local input_json=$(cat)
        
        # Extract event information
        local event_name=$(echo "$input_json" | grep -o '"hook_event_name":"[^"]*"' | cut -d'"' -f4)
        local tool_name=$(echo "$input_json" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
        
        if [ -n "$event_name" ]; then
            process_hook_event "$event_name" "$tool_name"
            
            cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "$event_name",
    "additionalContext": "📢 Notification manager processed $event_name event"
  }
}
EOF
        fi
    else
        # Command line usage
        case "$1" in
            "--status")
                echo "Notification Manager Status:"
                echo "Log file: $NOTIFICATION_LOG"
                if [ -f "$NOTIFICATION_LOG" ]; then
                    echo "Recent notifications:"
                    tail -n 5 "$NOTIFICATION_LOG" 2>/dev/null | while read line; do
                        echo "  $line"
                    done
                else
                    echo "No notifications logged yet"
                fi
                ;;
            "--check")
                echo "Checking for system issues..."
                if check_critical_issues; then
                    echo "✅ No critical issues detected"
                else
                    echo "⚠️ Issues found:"
                    check_critical_issues
                fi
                ;;
            *)
                echo "Usage: $0 [--status|--check]"
                ;;
        esac
    fi
}

main "$@"