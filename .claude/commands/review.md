---
description: Comprehensive code review workflow for recent changes
argument-hint: [specific area or files to review]
---

Perform comprehensive code review for: $ARGUMENTS

## Code Review Workflow

1. **Identify scope of review**
   - Analyze recent git changes: `git diff --name-only HEAD~1`
   - Focus on modified files or specified area
   - Check PROJECT_INDEX.json for context

2. **Use code-reviewer subagent for detailed analysis**
   - Automated quality checks and security scanning
   - Architecture pattern consistency validation
   - Performance and maintainability assessment

3. **Security and vulnerability assessment**
   - Check for hardcoded secrets or credentials
   - Validate input sanitization and validation
   - Review authentication and authorization logic
   - Assess potential injection vulnerabilities

4. **Code quality evaluation**
   - Review readability and maintainability
   - Check for proper error handling
   - Validate test coverage adequacy
   - Assess documentation completeness

5. **Architecture and design review**
   - Ensure consistency with existing patterns
   - Evaluate separation of concerns
   - Check dependency management
   - Review API design decisions

6. **Generate review report**
   - Prioritize findings: Critical 🔴, Important 🟡, Suggestions 🔵
   - Provide specific examples and recommended fixes
   - Include actionable next steps
   - Document any architectural decisions

## Review Checklist
- [ ] Security vulnerabilities addressed
- [ ] Code follows project conventions
- [ ] Tests cover new functionality
- [ ] Documentation updated appropriately
- [ ] No breaking changes without proper versioning
- [ ] Performance implications considered
- [ ] Error handling implemented properly

The review should maintain high code quality while enabling efficient development workflow.