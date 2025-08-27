# Claude Code Boost Project

This file provides guidance to Claude Code when working with code in this repository.

## Context Imports
@README.md
@package.json
@PROJECT_INDEX.json

## Quick Reference Commands
- Build: `npm run build` or `python -m build`
- Test: `npm test` or `pytest`
- Lint: `npm run lint` or `flake8`
- Start: `npm start` or `python main.py`

## Development Workflow
- Always use Plan Mode for complex changes: `claude --permission-mode plan`
- Use `/cost` to monitor context usage (stay under 70%)
- Use `--continue` to resume sessions
- Reference @PROJECT_INDEX.json before creating new functionality

## Claude Code Boost Features
- **Project Awareness**: Always check @PROJECT_INDEX.json to understand existing code
- **Smart Validation**: Use /validate to verify work completion
- **Session Continuity**: Use /fresh to restore context, /cleanup to prepare transitions
- **Quality Focus**: Automatic code review and testing via specialized agents

## Extended Thinking Usage
- `think` for routine analysis (4K tokens)
- `think harder` for complex problems (16K tokens)
- `ultra think` for initial research (32K tokens)

## Architecture Patterns
- Follow existing patterns found in @PROJECT_INDEX.json
- Prioritize refactoring over duplication
- Use dependency injection for services
- Prefer composition over inheritance

## Code Style Conventions
- Use descriptive variable names
- Maximum function length: 50 lines
- Follow language-specific best practices
- Include proper error handling