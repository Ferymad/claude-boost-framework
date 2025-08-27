# Feature Development Workflow Template
*CCPES v2.0 Team Standard - Use this template for all new feature development*

## 📋 Prerequisites
- [ ] Feature requirements documented and approved
- [ ] Project context loaded with `/fresh` command
- [ ] Current context usage < 40% (check with `/stats`)
- [ ] Recent `git status` shows clean working tree

## 🎯 Phase 1: Planning & Architecture (Plan Mode)
*Use Plan Mode for safe exploration before implementation*

### 1.1 Requirements Analysis
```bash
claude --permission-mode plan
> analyze the requirements for [FEATURE_NAME]
> check @PROJECT_INDEX.json for similar existing functionality
> identify potential code reuse opportunities
```

### 1.2 Architecture Design
```bash
> use the system-architect subagent to design [FEATURE_NAME]
> review existing patterns in @PROJECT_INDEX.json
> ensure consistency with current architecture
```

**Deliverables:**
- [ ] Architecture plan with component breakdown
- [ ] Integration points identified
- [ ] Database schema changes (if needed)
- [ ] API contract specifications
- [ ] Security and performance considerations

## 🔨 Phase 2: Implementation
*Exit Plan Mode and begin development with full automation*

### 2.1 Setup Development Session
```bash
# Exit Plan Mode (Shift+Tab twice)
> /fresh  # Reload complete project context
> create implementation plan based on architecture design
```

### 2.2 Core Development Loop
For each major component:

1. **Implement Component**
   ```bash
   > implement [COMPONENT_NAME] following the architecture plan
   > check @PROJECT_INDEX.json to avoid duplicate code
   ```

2. **Automated Quality Check**
   ```bash
   # Automatic code review (proactive subagent usage)
   > review the implemented [COMPONENT_NAME] code for quality and security
   ```

3. **Update Documentation**
   ```bash
   > /document [COMPONENT_NAME]  # Auto-generate documentation
   ```

### 2.3 Integration Points
```bash
> implement API endpoints for [FEATURE_NAME]
> add database integration following existing patterns
> ensure error handling consistency
```

**Deliverables:**
- [ ] Core functionality implemented
- [ ] API endpoints created and documented
- [ ] Database changes applied
- [ ] Error handling implemented
- [ ] Automated code review passed

## 🧪 Phase 3: Testing & Validation
*Comprehensive quality assurance using specialized subagents*

### 3.1 Automated Testing
```bash
> use the test-runner subagent to create comprehensive tests for [FEATURE_NAME]
> ensure test coverage meets project minimum (80%+)
> run all existing tests to check for regressions
```

### 3.2 Quality Validation
```bash
> use the code-reviewer subagent to perform final code review
> focus on security, performance, and maintainability
```

### 3.3 Independent Verification
```bash
> use the blind-validator subagent to verify [FEATURE_NAME] works according to original requirements
> ensure all acceptance criteria are met
```

### 3.4 Performance Testing (if applicable)
```bash
> use the performance-optimizer subagent to analyze [FEATURE_NAME] performance
> benchmark critical paths and optimize if needed
```

**Deliverables:**
- [ ] Unit tests covering all functionality (>80% coverage)
- [ ] Integration tests for API endpoints
- [ ] Performance benchmarks established
- [ ] Security review completed
- [ ] Blind validation PASSED with evidence

## 🚀 Phase 4: Documentation & Deployment Preparation
*Final preparation for team integration*

### 4.1 Comprehensive Documentation
```bash
> /document [FEATURE_NAME] --comprehensive
> update API documentation
> create usage examples and tutorials
```

### 4.2 Team Integration Preparation
```bash
> update @CLAUDE.md with new patterns and conventions
> document any new subagent usage patterns
> create troubleshooting guide for common issues
```

### 4.3 Pre-deployment Validation
```bash
> /validate [FEATURE_NAME] --full-suite
> run complete regression test suite
> verify all hooks execute successfully
```

**Deliverables:**
- [ ] Complete API documentation
- [ ] Usage examples and tutorials
- [ ] Updated team conventions
- [ ] Troubleshooting guide
- [ ] All validations PASSED

## 📈 Phase 5: Deployment & Monitoring
*Deploy with confidence using automated quality gates*

### 5.1 Pre-commit Validation
```bash
> run final validation before commit
> ensure PROJECT_INDEX.json is updated automatically
> verify no security vulnerabilities introduced
```

### 5.2 Deployment
```bash
> commit with descriptive message following team conventions
> create pull request with validation evidence
> address any review feedback promptly
```

### 5.3 Post-deployment Monitoring
```bash
> /stats --post-deployment
> monitor system performance metrics
> track feature adoption and usage patterns
```

**Deliverables:**
- [ ] Code committed with validation evidence
- [ ] Pull request created with comprehensive description
- [ ] Performance metrics baseline established
- [ ] Feature successfully deployed and monitored

## 🎯 Quality Gates & Success Criteria

### Mandatory Gates (Must Pass)
- [ ] **Architecture Review**: System-architect subagent approval
- [ ] **Code Quality**: Code-reviewer subagent approval with no critical issues
- [ ] **Test Coverage**: Minimum 80% coverage with test-runner validation
- [ ] **Security**: No security vulnerabilities identified
- [ ] **Performance**: No regressions, meets performance requirements
- [ ] **Blind Validation**: Independent verification PASSED with evidence
- [ ] **Documentation**: Complete and accurate documentation generated

### Team Standards
- [ ] **Consistency**: Follows existing patterns in PROJECT_INDEX.json
- [ ] **Reusability**: No duplicate code created, maximum reuse achieved
- [ ] **Maintainability**: Clear, readable code with proper error handling
- [ ] **Scalability**: Performance characteristics documented and acceptable

## 🚨 Troubleshooting Common Issues

### PROJECT_INDEX.json Not Updated
**Symptoms**: Claude suggests creating duplicate functionality
**Solution**: 
```bash
python .claude/hooks/project-indexer.py  # Manual update
# Check hook configuration: /hooks
```

### Subagent Delegation Failing  
**Symptoms**: Manual intervention required instead of automatic delegation
**Solution**:
```bash
# Use explicit invocation:
> use the [subagent-name] subagent to [specific task]
# Check subagent definitions: /agents
```

### Context Usage Too High
**Symptoms**: Quality degrading, approaching 70% threshold
**Solution**:
```bash
> /cleanup "continue [FEATURE_NAME] implementation"
> /clear  # If necessary
> /fresh  # Restore context for next session
```

### Validation Failures
**Symptoms**: Blind validator reports FAILED status
**Solution**:
1. Review validation evidence carefully
2. Fix identified issues
3. Re-run validation until PASSED
4. Never proceed without validation success

## 📊 Success Metrics to Track

### Feature Development Metrics
- [ ] **Implementation Time**: Target 37% reduction vs baseline
- [ ] **Code Duplication**: <5% similar code created
- [ ] **Context Efficiency**: Average <70% usage per session
- [ ] **Quality Score**: >95% validation success rate

### Team Collaboration Metrics
- [ ] **Consistency**: All team members follow workflow
- [ ] **Knowledge Sharing**: Templates updated with new patterns
- [ ] **Review Efficiency**: 30% reduction in review cycles
- [ ] **Deployment Success**: >95% first-time success rate

## 🎓 Learning & Improvement

### After Each Feature
- [ ] **Retrospective**: What worked well? What can improve?
- [ ] **Pattern Updates**: Add new patterns to PROJECT_INDEX.json
- [ ] **Template Updates**: Improve this workflow based on experience
- [ ] **Team Sharing**: Share learnings with other team members

### Continuous Improvement
- [ ] **Metrics Review**: Weekly analysis of development efficiency
- [ ] **Automation Enhancement**: Identify manual steps that can be automated
- [ ] **Quality Evolution**: Raise quality bars based on team maturity
- [ ] **Tool Evolution**: Adopt new Claude Code features as available

---

**Remember**: This workflow leverages the complete CCPES v2.0 system to ensure reliable, high-quality feature development. Trust the automated quality gates, but always verify with blind validation. Focus on architecture and planning - the system handles the execution details.

**🔄 Template Version**: v2.0.1 - Update this template based on team experience and system evolution.