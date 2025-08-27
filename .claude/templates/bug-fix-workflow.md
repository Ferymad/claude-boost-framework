# Bug Fix Workflow Template
*CCPES v2.0 Emergency Response - Fast, reliable issue resolution with quality assurance*

## 🚨 Emergency Response Protocol
*For critical production issues requiring immediate attention*

### Priority Classification
- **P0 - Critical**: Production down, data loss, security breach
- **P1 - High**: Major functionality broken, significant user impact  
- **P2 - Medium**: Minor functionality issues, limited user impact
- **P3 - Low**: Cosmetic issues, enhancement requests

## 📋 Prerequisites
- [ ] Issue clearly documented with reproduction steps
- [ ] Priority level assigned (P0-P3)
- [ ] Impact assessment completed
- [ ] Clean working tree (`git status`)

## 🔍 Phase 1: Investigation & Diagnosis
*Use debugger subagent for systematic root cause analysis*

### 1.1 Initial Triage (All Priority Levels)
```bash
> /fresh  # Load complete project context
> /stats  # Check current system status
```

### 1.2 Issue Reproduction
```bash
> use the debugger subagent to reproduce [BUG_DESCRIPTION]
> analyze error logs and stack traces
> identify affected components using @PROJECT_INDEX.json
```

### 1.3 Root Cause Analysis
```bash
> use the debugger subagent to identify root cause of [BUG_DESCRIPTION]
> check recent commits for potential regression: git log --oneline -20
> analyze dependencies and integration points
```

**Deliverables:**
- [ ] Issue successfully reproduced
- [ ] Root cause identified and documented
- [ ] Impact scope clearly defined
- [ ] Fix approach determined

## ⚡ Phase 2: Solution Development
*Priority-based approach with appropriate quality gates*

### P0 - Critical Issues (Hotfix Process)
```bash
# Skip Plan Mode for critical issues - implement directly
> create minimal hotfix for [CRITICAL_ISSUE]
> focus on immediate resolution, not perfect code
> use debugger subagent to verify fix resolves root cause
```

### P1-P3 Issues (Standard Process)
```bash
claude --permission-mode plan
> analyze proper fix approach for [BUG_DESCRIPTION]
> check @PROJECT_INDEX.json for similar patterns
> design solution that prevents regression
```

### 2.1 Implementation
```bash
> implement fix for [BUG_DESCRIPTION] following debugger recommendations
> ensure fix addresses root cause, not just symptoms
> minimize scope of changes to reduce risk
```

### 2.2 Immediate Validation
```bash
> use the debugger subagent to verify fix resolves the original issue
> test edge cases and potential regression scenarios
```

**Deliverables:**
- [ ] Minimal, targeted fix implemented
- [ ] Root cause addressed (not just symptoms)
- [ ] Immediate verification successful
- [ ] Change scope minimized for safety

## 🧪 Phase 3: Quality Assurance
*Comprehensive testing appropriate to priority level*

### P0 - Critical (Fast Track)
```bash
> use the test-runner subagent to run affected test suite
> manually test critical path functionality
> use blind-validator for basic functionality verification
```

### P1-P3 - Standard Testing
```bash
> use the test-runner subagent to create specific regression tests
> run full test suite to check for side effects
> use the code-reviewer subagent to review fix quality
> use blind-validator to verify complete resolution
```

### 3.1 Regression Prevention
```bash
> create or update tests to prevent this bug recurring
> document the issue and solution in code comments
> update monitoring if applicable
```

**Deliverables:**
- [ ] Regression tests created/updated
- [ ] Full test suite passes
- [ ] No new issues introduced
- [ ] Monitoring updated (if needed)

## 📚 Phase 4: Documentation & Communication
*Ensure team learns from the issue*

### 4.1 Issue Documentation
```bash
> /document [BUG_FIX] --include-root-cause-analysis
> update TROUBLESHOOTING.md if this is a common issue
> document prevention strategies
```

### 4.2 Team Communication
```bash
> prepare summary of root cause and resolution
> identify process improvements to prevent similar issues
> update team knowledge base
```

**Deliverables:**
- [ ] Root cause analysis documented
- [ ] Resolution steps recorded
- [ ] Prevention strategies identified
- [ ] Team knowledge updated

## 🚀 Phase 5: Deployment & Monitoring
*Safe deployment with verification*

### P0 - Critical (Immediate Deployment)
```bash
> commit hotfix with clear description
> deploy immediately to affected environments
> monitor system health closely post-deployment
```

### P1-P3 - Standard Deployment
```bash
> /validate [BUG_FIX] --comprehensive
> create pull request with detailed testing evidence
> follow standard review and deployment process
```

### 5.1 Post-Deployment Verification
```bash
> verify issue is resolved in production
> monitor error rates and system metrics
> confirm no regression introduced
```

**Deliverables:**
- [ ] Fix successfully deployed
- [ ] Original issue verified resolved
- [ ] System stability confirmed
- [ ] Monitoring shows expected improvement

## 🎯 Quality Gates by Priority

### P0 - Critical Issues
**Minimum Gates** (Speed is priority):
- [ ] Root cause identified by debugger subagent
- [ ] Fix verified by debugger subagent
- [ ] Critical path tests pass
- [ ] Basic functionality verified by blind-validator

### P1 - High Priority
**Standard Gates**:
- [ ] Root cause analysis complete
- [ ] Code review by code-reviewer subagent
- [ ] Regression tests created
- [ ] Full affected test suite passes
- [ ] Blind validation PASSED

### P2-P3 - Medium/Low Priority
**Full Gates**:
- [ ] Complete root cause analysis
- [ ] Architecture review for complex fixes
- [ ] Comprehensive test coverage
- [ ] Full validation suite PASSED
- [ ] Documentation complete

## 🔧 Emergency Procedures

### System Down (P0)
1. **Immediate Response** (0-5 minutes):
   ```bash
   > /fresh
   > use debugger subagent for immediate system assessment
   > identify if rollback is fastest resolution
   ```

2. **Hotfix Development** (5-30 minutes):
   ```bash
   > create minimal fix addressing immediate issue
   > verify fix with debugger subagent
   > deploy to staging for quick validation
   ```

3. **Production Deployment** (30-45 minutes):
   ```bash
   > deploy hotfix to production
   > monitor system recovery
   > prepare proper fix for later deployment
   ```

### Data Loss Risk (P0)
1. **Immediate Containment**:
   ```bash
   > identify scope of potential data loss
   > implement immediate safeguards
   > backup current state before any fixes
   ```

2. **Recovery Strategy**:
   ```bash
   > use debugger subagent to analyze data integrity
   > implement data recovery procedures
   > verify recovery completeness
   ```

### Security Breach (P0)
1. **Immediate Response**:
   ```bash
   > identify compromised components
   > implement immediate access restrictions
   > notify security team and stakeholders
   ```

2. **Containment**:
   ```bash
   > use security patterns from @PROJECT_INDEX.json
   > implement security fixes immediately
   > verify breach is contained
   ```

## 🚨 Escalation Procedures

### When to Escalate
- **Technical**: Root cause unclear after 2 hours investigation
- **Impact**: Issue affects more systems than initially assessed  
- **Resources**: Expertise needed beyond current team capabilities
- **Time**: P0 issues not resolved within SLA (4 hours)

### Escalation Process
```bash
> /document [ISSUE] --escalation-summary
> prepare technical brief with current findings
> identify specific expertise needed
> transfer context using enhanced session state
```

## 📊 Success Metrics

### Resolution Time Targets
- **P0 Critical**: 4 hours maximum, 2 hours target
- **P1 High**: 24 hours maximum, 8 hours target  
- **P2 Medium**: 1 week maximum, 3 days target
- **P3 Low**: 1 month maximum, 2 weeks target

### Quality Metrics
- [ ] **Root Cause Accuracy**: >95% correct identification
- [ ] **Fix Effectiveness**: <5% regression rate
- [ ] **Test Coverage**: 100% of fix paths covered
- [ ] **Documentation Quality**: Complete troubleshooting info

### Process Metrics
- [ ] **First Time Fix Rate**: >90% issues resolved permanently
- [ ] **Escalation Rate**: <10% of issues require escalation
- [ ] **Learning Rate**: Preventable recurrence <2%
- [ ] **Team Knowledge**: All team members can use workflow

## 🎓 Learning & Improvement

### Post-Incident Review (P0-P1 Issues)
```bash
> /document [INCIDENT] --post-mortem
> analyze what worked well in response
> identify process improvements
> update emergency procedures if needed
```

### Knowledge Capture
- [ ] **Root Cause Patterns**: Update detection algorithms
- [ ] **Solution Patterns**: Add to reusable fix library
- [ ] **Prevention Strategies**: Update development guidelines
- [ ] **Tool Improvements**: Enhance debugger subagent capabilities

### Team Development
- [ ] **Skill Building**: Identify knowledge gaps exposed
- [ ] **Process Training**: Update training materials
- [ ] **Tool Mastery**: Improve subagent usage patterns
- [ ] **Response Coordination**: Enhance team communication

---

**Remember**: In bug fixing, speed and quality must be balanced based on priority. Use the full power of CCPES subagents to ensure thorough analysis and reliable fixes. Never skip validation, but adjust the depth based on urgency.

**🔄 Template Version**: v2.0.1 - Continuously improve based on incident learnings and system evolution.