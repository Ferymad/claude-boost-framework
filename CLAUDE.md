# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context Imports
@README.md
@PROJECT_INDEX.json
@PRD.md
@roadmap.md
@alignment-report.md

## Project Overview

This is the **Claude Code Performance Enhancement System (CCPES) v2.0** - a comprehensive system that combines official Claude Code features with innovative custom solutions to solve critical AI development problems:

- **Context Degradation**: Maintaining quality under 70% context usage
- **Code Duplication**: Reducing from 40% to <5% through PROJECT_INDEX.json awareness
- **False Completion Claims**: Improving accuracy from 60% to >95% via blind validation
- **Session Discontinuity**: Achieving >80% continuity rate with enhanced state management

## Architecture Overview

The system follows a hybrid approach:

### Official Claude Code Features Enhanced:
- **Subagent Architecture**: Task-specific agents via `/agents` command
- **Hook System**: Automated workflows via `/hooks` command 
- **Memory Management**: CLAUDE.md with @file imports and hierarchical loading
- **Plan Mode**: Safe exploration with `--permission-mode plan`
- **Session Continuity**: Enhanced `--continue`/`--resume` with deep state preservation

### Custom Innovations:
- **PROJECT_INDEX.json System**: Minified codebase abstractions preventing code duplication
- **Blind Validation Pattern**: Independent verification using subagents without development context
- **70% Context Rule**: Proactive quality maintenance threshold
- **Advanced Session State**: Deep context preservation beyond official capabilities

## Key Commands

### Project Management
- `python3 .claude/hooks/project-indexer.py` - Generate/update PROJECT_INDEX.json
- `git status` - Check project state
- `git log --oneline -10` - View recent changes

### Development Workflow Commands
- Use Plan Mode for complex changes: `claude --permission-mode plan`
- Monitor context usage: Reference `/cost` command output
- Session continuity: `claude --continue` to resume sessions
- Reference project structure: Always check @PROJECT_INDEX.json before creating new functionality

## Architecture Patterns

### Context Management Strategy
- **70% Context Rule**: Rotate sessions before quality degrades (not at 90%)
- **Progressive Disclosure**: Start broad, narrow down to specific implementation
- **Strategic Thinking**: Use `think` (4K), `think harder` (16K), `ultra think` (32K) based on complexity

### Quality Assurance Workflow
1. **Plan First**: Use Plan Mode for exploration before implementation
2. **Build with Awareness**: Check PROJECT_INDEX.json to prevent duplication
3. **Validate Independently**: Use blind validation pattern for completion verification
4. **Monitor Continuously**: Track context usage and hook performance

### File Organization
```
.claude/
├── hooks/          # Automation scripts (project-indexer.py, etc.)
├── agents/         # Specialized subagents (code-reviewer, validator, etc.)
├── commands/       # Custom slash commands (/cleanup, /fresh, etc.)
└── settings.json   # Project-specific configurations
```

## Development Principles

### Project Awareness First
- Always reference PROJECT_INDEX.json before creating new functionality
- Check for existing similar implementations
- Prioritize refactoring existing code over creating duplicates
- Maintain architectural consistency

### Validation-Driven Development  
- Use blind validation pattern: Independent verification without development context
- Block task completion until validation passes with evidence
- Test against original requirements, not implementation details
- Generate pass/fail determinations with supporting evidence

### Session Management Excellence
- Use cleanup → clear → fresh sequence for session transitions
- Preserve state in files before clearing context
- Load comprehensive project context on session start
- Maintain memory hierarchy: Enterprise → Project → User → Local

## Hook Integration

The project uses automated hooks for:
- **PostToolUse**: Automatic PROJECT_INDEX.json updates on file changes
- **SessionEnd**: State preservation for continuity 
- **SessionStart**: Context restoration with project awareness
- **PreToolUse**: Validation and security checks

Configure hooks via `/hooks` command interface, not manual JSON editing.

## Success Metrics

Track these KPIs to measure system effectiveness:
- Code duplication rate: Target <5% (from baseline 40%)
- Task completion accuracy: Target >95% (from baseline 60%) 
- Context usage efficiency: Target <70% average per session
- Feature development time: Target 37% reduction
- Session continuity rate: Target >80% success rate
- Hook execution success: Target >99% reliability