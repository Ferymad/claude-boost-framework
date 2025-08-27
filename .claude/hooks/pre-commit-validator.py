#!/usr/bin/env python3
"""
Pre-commit validation hook for Claude Code
Validates code quality and security before commits
"""
import json
import subprocess
import sys
import os
import re
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run command and return result"""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, 
            capture_output=True, text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_sensitive_patterns(content, filepath):
    """Check for potentially sensitive patterns in code"""
    issues = []
    lines = content.split('\n')
    
    # Patterns that might indicate secrets or sensitive data
    sensitive_patterns = [
        (r'password\s*=\s*["\'][^"\']+["\']', 'hardcoded password'),
        (r'api_?key\s*=\s*["\'][^"\']+["\']', 'hardcoded API key'),
        (r'secret\s*=\s*["\'][^"\']+["\']', 'hardcoded secret'),
        (r'token\s*=\s*["\'][^"\']+["\']', 'hardcoded token'),
        (r'credential\s*=\s*["\'][^"\']+["\']', 'hardcoded credential'),
        (r'[A-Za-z0-9+/]{40,}={0,2}', 'potential base64 encoded secret'),
        (r'sk-[A-Za-z0-9]{32,}', 'OpenAI API key pattern'),
        (r'ghp_[A-Za-z0-9]{36}', 'GitHub personal access token'),
        (r'glpat-[A-Za-z0-9_-]{20}', 'GitLab personal access token'),
    ]
    
    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        
        # Skip comments and test files for some patterns
        is_comment = line.strip().startswith(('#', '//', '/*', '*', '<!--'))
        is_test_file = 'test' in filepath.lower()
        
        for pattern, description in sensitive_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Be less strict for test files and comments
                if is_test_file and ('test' in description or 'example' in line_lower):
                    continue
                if is_comment and 'example' in line_lower:
                    continue
                    
                issues.append(f"{filepath}:{i} - {description}: {line.strip()}")
    
    return issues


def check_code_quality(content, filepath):
    """Check for code quality issues"""
    issues = []
    lines = content.split('\n')
    
    # Check for TODO/FIXME in non-development files
    if not any(keyword in filepath.lower() for keyword in ['test', 'demo', 'example', 'draft']):
        for i, line in enumerate(lines, 1):
            if re.search(r'\b(TODO|FIXME|XXX|HACK)\b', line, re.IGNORECASE):
                issues.append(f"{filepath}:{i} - Production code contains TODO/FIXME: {line.strip()}")
    
    # Check for console.log/print statements in certain files
    if filepath.endswith(('.js', '.jsx', '.ts', '.tsx')):
        for i, line in enumerate(lines, 1):
            if re.search(r'console\.(log|debug|info)', line) and not line.strip().startswith('//'):
                issues.append(f"{filepath}:{i} - Debug console statement: {line.strip()}")
    
    elif filepath.endswith('.py'):
        for i, line in enumerate(lines, 1):
            if re.search(r'\bprint\s*\(', line) and not line.strip().startswith('#'):
                issues.append(f"{filepath}:{i} - Debug print statement: {line.strip()}")
    
    return issues


def validate_commit():
    """Validate staged changes before commit"""
    issues = []
    
    # Get staged files
    success, stdout, stderr = run_command("git diff --cached --name-only")
    if not success:
        return ["Could not get staged files: " + stderr]
    
    staged_files = [f.strip() for f in stdout.strip().split('\n') if f.strip()]
    
    if not staged_files:
        return []  # No staged files
    
    # Check each staged file
    for file in staged_files:
        if not os.path.exists(file):
            continue
            
        try:
            # Get staged content (not working directory content)
            success, content, _ = run_command(f"git show :{file}")
            if not success:
                continue
                
            # Only check text files
            if any(file.endswith(ext) for ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.md', '.txt', '.json', '.yaml', '.yml']):
                # Check for sensitive patterns
                sensitive_issues = check_sensitive_patterns(content, file)
                issues.extend(sensitive_issues)
                
                # Check code quality
                quality_issues = check_code_quality(content, file)
                issues.extend(quality_issues)
                
        except Exception as e:
            issues.append(f"{file} - Error analyzing file: {str(e)}")
    
    return issues


def main():
    """Main hook execution"""
    try:
        # Read hook input data
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        command = input_data.get('tool_input', {}).get('command', '')
        
        # Only validate git commits
        if 'git commit' in command:
            issues = validate_commit()
            
            if issues:
                # Create JSON response for critical issues
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "blockExecution": True,
                        "additionalContext": "❌ Pre-commit validation failed:\n" + "\n".join(f"  • {issue}" for issue in issues)
                    }
                }
                print(json.dumps(output))
                sys.exit(1)  # Block the commit
            else:
                # Success response
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse", 
                        "additionalContext": "✅ Pre-commit validation passed - no security or quality issues detected"
                    }
                }
                print(json.dumps(output))
        
    except Exception as e:
        # Don't block commits due to hook errors, but log them
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": f"⚠️ Pre-commit hook warning: {str(e)}"
            }
        }
        print(json.dumps(output))


if __name__ == "__main__":
    main()