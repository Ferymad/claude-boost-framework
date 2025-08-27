# Claude Code Enhancement System - Troubleshooting Guide

This guide helps resolve common issues with the Claude Code Performance Enhancement System (CCPES) v2.0.

## Quick Diagnostics

Run these commands to check system health:

```bash
# Check hook configuration
/.claude/hooks/notification-manager.sh --status

# Generate usage analytics
python3 .claude/hooks/token-tracker.py --report  

# Test PROJECT_INDEX.json generation
python3 .claude/hooks/project-indexer.py

# Verify all hooks are executable
ls -la .claude/hooks/
```

---

## Common Issues

### 1. Hook Failures - "python: command not found"

**Symptoms**: 
- Dashboard shows 0% hook success rate
- Error messages: "status code 127: /bin/sh: 1: python: not found"
- PROJECT_INDEX.json not updating automatically
- Analytics not being collected

**Root Cause**: 
System has `python3` installed but hooks are configured to use `python` command.

**Solutions**:

1. **Fix hook configuration in settings.json** (RECOMMENDED):
   ```bash
   # Edit .claude/settings.json and change all instances of:
   "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/..."
   # to:
   "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/..."
   ```

2. **Alternative: Reconfigure via /hooks command**:
   ```bash
   # Use Claude Code's hook interface
   claude > /hooks
   # Remove existing hooks and re-add with python3 command
   ```

3. **Verify fix worked**:
   ```bash
   # Check recent hook executions
   tail -n 10 .claude/analytics/notifications.log
   # Should show recent successful executions
   ```

### 2. PROJECT_INDEX.json Not Updating

**Symptoms**: 
- Claude creates duplicate code despite existing functionality
- PROJECT_INDEX.json missing or outdated
- "No such file or directory" errors

**Solutions**:

1. **Check hook configuration** (after fixing python3 issue above):
   ```bash
   # Verify hooks are properly configured
   cat .claude/settings.json | grep python3
   ```

2. **Manually regenerate index**:
   ```bash
   python3 .claude/hooks/project-indexer.py
   ```

3. **Verify file permissions**:
   ```bash
   chmod +x .claude/hooks/project-indexer.py
   ```

4. **Check Python availability**:
   ```bash
   which python3
   # If not found, install Python 3 or update PATH
   ```

**Prevention**: The PostToolUse hook should automatically update PROJECT_INDEX.json after file modifications.

### 2. Hooks Not Executing

**Symptoms**:
- Automation not working
- Manual processes still required
- No hook output in logs

**Solutions**:

1. **Verify hook permissions**:
   ```bash
   chmod +x .claude/hooks/*.py .claude/hooks/*.sh
   ```

2. **Test hooks manually**:
   ```bash
   # Test with sample JSON input
   echo '{"tool_name":"Edit","hook_event_name":"PostToolUse"}' | python3 .claude/hooks/project-indexer.py
   ```

3. **Check hook configuration syntax**:
   ```bash
   # Validate JSON syntax
   cat .claude/settings.json | python3 -m json.tool
   ```

4. **Review hook logs**:
   ```bash
   tail -f .claude/analytics/errors.log
   ```

### 3. Subagents Not Spawning Correctly

**Symptoms**:
- Tasks not delegated to appropriate subagents
- "Agent not found" errors
- Manual subagent invocation required

**Solutions**:

1. **Check subagent definitions**:
   ```bash
   ls .claude/agents/
   cat .claude/agents/code-reviewer.md
   ```

2. **Verify tool permissions in frontmatter**:
   ```yaml
   ---
   name: code-reviewer
   tools: Read, Grep, Glob, Bash
   ---
   ```

3. **Use explicit invocation**:
   ```
   > use the code-reviewer subagent to check recent changes
   > have the validator subagent verify the login feature works
   ```

4. **Check Claude Code version**:
   ```bash
   claude --version
   # Ensure subagent features are supported
   ```

### 4. Context Degradation Despite Guidelines

**Symptoms**:
- Quality drops even under 70% context usage
- Repetitive or inconsistent responses
- Loss of project awareness

**Solutions**:

1. **Use cleanup → clear → fresh sequence**:
   ```
   > /cleanup "implement user dashboard"
   > /clear
   > /fresh
   ```

2. **Check for context pollution**:
   - Review CLAUDE.md for overly verbose content
   - Minimize @import file sizes
   - Use progressive disclosure (broad → specific)

3. **Optimize memory files**:
   ```bash
   # Keep CLAUDE.md concise
   wc -w CLAUDE.md  # Target: <500 words
   
   # Check PROJECT_INDEX.json size
   du -h PROJECT_INDEX.json
   ```

4. **Use extended thinking strategically**:
   - `think` for routine tasks (4K tokens)
   - `think harder` for complex analysis (16K tokens)  
   - `ultra think` for initial research only (32K tokens)

### 5. Session Continuity Issues

**Symptoms**:
- Lost context between sessions
- Repeated explanations required
- Previous work not remembered

**Solutions**:

1. **Use official session continuation**:
   ```bash
   claude --continue    # Continue most recent conversation
   claude --resume     # Show conversation picker
   ```

2. **Check session state files**:
   ```bash
   ls .claude/state/
   cat .claude/state/last_session.json
   ```

3. **Manually load project context**:
   ```
   > /fresh
   > Review @PROJECT_INDEX.json and @CLAUDE.md for project context
   ```

4. **Verify SessionStart/SessionEnd hooks**:
   ```bash
   grep -A 10 "SessionStart" .claude/settings.json
   ```

### 6. Pre-commit Validation Blocking Commits

**Symptoms**:
- Git commits fail with validation errors
- "Sensitive patterns detected" messages
- Unable to commit legitimate code

**Solutions**:

1. **Review validation errors**:
   ```bash
   # Check what patterns were detected
   git commit -v  # Shows detailed error messages
   ```

2. **Temporarily disable validation** (if needed):
   ```bash
   # Remove PreToolUse hook temporarily
   cp .claude/settings.json .claude/settings.json.backup
   # Edit settings.json to comment out PreToolUse
   ```

3. **Whitelist test files or comments**:
   - Add `# test example` comments for test data
   - Use meaningful variable names in examples
   - Place sensitive patterns in configuration files, not code

4. **Fix legitimate issues**:
   ```bash
   # Replace hardcoded values with environment variables
   export API_KEY="your-key-here"
   # Reference via os.environ or process.env
   ```

### 7. Performance Issues

**Symptoms**:
- Hook execution takes too long
- System becomes unresponsive
- High CPU or memory usage

**Solutions**:

1. **Profile hook performance**:
   ```bash
   time python3 .claude/hooks/project-indexer.py
   time bash .claude/hooks/notification-manager.sh --check
   ```

2. **Clean up analytics data**:
   ```bash
   python3 .claude/hooks/token-tracker.py --cleanup
   rm .claude/analytics/*.log.old
   ```

3. **Optimize PROJECT_INDEX.json generation**:
   ```bash
   # Check for large files being analyzed
   find . -name "*.py" -size +100k
   find . -name "*.js" -size +100k
   ```

4. **Limit concurrent hooks**:
   - Reduce number of hooks per matcher
   - Use conditional execution in hook scripts

---

## Advanced Diagnostics

### Debug Mode

Enable detailed logging:

```bash
export CLAUDE_DEBUG_ANALYTICS=1
# Run operations to see detailed hook output
```

### Hook Execution Tracing

```bash
# Enable bash debugging
export PS4='+ ${BASH_SOURCE}:${LINENO}: '
bash -x .claude/hooks/notification-manager.sh --status
```

### Manual Hook Testing

```bash
# Create test input for hooks
echo '{
  "tool_name": "Edit",
  "hook_event_name": "PostToolUse",
  "tool_input": {"file_path": "test.py", "content": "print(\"hello\")"}
}' | python3 .claude/hooks/project-indexer.py
```

### Performance Monitoring

```bash
# Monitor system resources during operations
top -p $(pgrep -f "python3.*claude")
iostat 1 5  # Monitor I/O during index generation
```

---

## Best Practices

### Prevention

1. **Regular maintenance**:
   ```bash
   # Weekly cleanup
   python3 .claude/hooks/token-tracker.py --cleanup
   bash .claude/hooks/notification-manager.sh --check
   ```

2. **Monitor system health**:
   ```bash
   # Check for issues daily
   bash .claude/hooks/notification-manager.sh --status
   ```

3. **Keep hooks updated**:
   ```bash
   git log --oneline .claude/hooks/
   ```

### Recovery

1. **Reset to working state**:
   ```bash
   cp .claude/settings.json.backup .claude/settings.json
   python3 .claude/hooks/project-indexer.py
   ```

2. **Clean slate restart**:
   ```bash
   rm -rf .claude/analytics/
   rm -rf .claude/state/
   # Regenerate PROJECT_INDEX.json
   python3 .claude/hooks/project-indexer.py
   ```

---

## Getting Help

### Log Analysis

Check these locations for error information:

- `.claude/analytics/errors.log` - Hook execution errors
- `.claude/analytics/notifications.log` - System events
- `.claude/analytics/usage.jsonl` - Usage analytics

### Report Issues

When reporting issues, include:

1. **System information**:
   ```bash
   uname -a
   python3 --version
   claude --version
   ```

2. **Configuration**:
   ```bash
   cat .claude/settings.json
   ls -la .claude/
   ```

3. **Recent logs**:
   ```bash
   tail -20 .claude/analytics/*.log
   ```

4. **Steps to reproduce**:
   - Exact commands run
   - Expected vs actual behavior
   - Error messages

### Community Resources

- GitHub Issues: [claude-code-enhancement-issues](https://github.com/user/project/issues)
- Documentation: Check `README.md`, `PRD.md`, and `roadmap.md`
- Best Practices: Review `CLAUDE.md` for project-specific guidelines

---

**Remember**: The enhancement system is designed to be resilient. Most issues can be resolved by regenerating the PROJECT_INDEX.json and restarting with `/fresh`. When in doubt, return to the official Claude Code documentation for baseline functionality.