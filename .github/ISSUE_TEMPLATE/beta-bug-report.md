---
name: 🐛 Beta Bug Report
about: Report bugs found during CCPES v2.0 beta testing
title: '[BETA BUG] Brief description of the issue'
labels: bug, beta
assignees: ''
---

## 🐛 Beta Bug Report

**Bug Reporter**: [Your name/beta tester handle]  
**Date Discovered**: [Date when bug was found]  
**Severity**: [Critical/High/Medium/Low]  
**Component**: [Installation/Hooks/Subagents/Commands/Other]

---

### 📋 **Bug Summary**
**Brief Description**:
[One-line description of what's broken]

**Expected Behavior**:
[What should happen]

**Actual Behavior**:
[What actually happens]

**Impact on Beta Testing**:
- [ ] Blocking - cannot continue testing
- [ ] Major - significantly impacts workflow
- [ ] Minor - workaround available
- [ ] Cosmetic - doesn't affect functionality

---

### 🔍 **Reproduction Steps**
**Steps to reproduce the bug**:
1. [First step]
2. [Second step]
3. [Third step]
4. [Result/error occurs]

**Frequency**:
- [ ] Always happens
- [ ] Usually happens (75%+ of the time)
- [ ] Sometimes happens (25-75% of the time)  
- [ ] Rarely happens (<25% of the time)
- [ ] Happened once

**First Occurrence**: [When did you first notice this?]

---

### 💻 **Environment Details**
**System Information**:
- **OS**: [Windows 10/11, macOS version, Linux distro]
- **Python Version**: [output of `python --version`]
- **Node.js Version**: [output of `node --version`]
- **Claude Code Version**: [if relevant]
- **CCPES Version**: [0.9.0-beta or git commit]

**Installation Method**:
- [ ] NPM: `npm install -g claude-boost@beta`
- [ ] Git: `git clone` + `python setup.py install`
- [ ] Other: [specify]

**Project Context**:
- **Project Type**: [web app, CLI, API, etc.]
- **Primary Language**: [Python, JavaScript, etc.]
- **Codebase Size**: [Small/Medium/Large]

---

### 📊 **Error Information**
**Error Messages** (if any):
```
[Paste exact error messages here]
```

**Stack Traces** (if available):
```
[Paste full stack traces here]
```

**Log Output**:
```
[Paste relevant log output from .claude/state/ or console]
```

**Screenshots** (if relevant):
[Attach screenshots of the issue]

---

### 🔧 **Additional Context**
**What were you trying to accomplish?**:
[Describe the task you were performing when the bug occurred]

**Recent changes**:
[Any recent changes to your project, system, or CCPES configuration?]

**Workaround** (if found):
[How did you work around this issue, if at all?]

**Related Issues**:
[Links to any related bugs or issues you've found]

---

### 🧪 **Beta Testing Context**
**Testing Phase**: 
- [ ] Initial setup (Week 1)
- [ ] Active development (Week 2)
- [ ] Advanced features (Week 3)
- [ ] Final validation (Week 4)

**Feature Being Tested**:
- [ ] PROJECT_INDEX.json system
- [ ] Subagent functionality
- [ ] Hook automation
- [ ] Command execution
- [ ] Session management
- [ ] Installation/setup

**Impact on Beta Goals**:
[How does this bug affect your ability to validate CCPES performance claims?]

---

### 🚑 **Urgency Assessment**
**Beta Program Impact**:
- [ ] Critical - prevents beta testing entirely
- [ ] High - significantly impacts testing ability
- [ ] Medium - causes inconvenience but testing continues
- [ ] Low - minor issue, testing not affected

**User Experience Impact**:
- [ ] Severely degrades user experience
- [ ] Moderately impacts user experience
- [ ] Minimally affects user experience
- [ ] No real impact on user experience

**Suggested Priority**:
- [ ] Fix immediately (blocks other beta testers)
- [ ] Fix in next patch (affects multiple users)
- [ ] Fix before production (not urgent for beta)
- [ ] Nice to fix eventually (low priority)

---

### ✅ **Reporter Checklist**
Before submitting, I have:
- [ ] Checked if this is already reported in existing issues
- [ ] Provided clear steps to reproduce the problem
- [ ] Included all relevant error messages and logs
- [ ] Specified my system environment details
- [ ] Assessed the impact on beta testing goals
- [ ] Added appropriate severity and component labels

---

### 📝 **Follow-up Commitment**
**I commit to**:
- [ ] Test any proposed fixes and provide feedback
- [ ] Provide additional information if requested
- [ ] Update this issue if I find workarounds
- [ ] Close the issue when confirmed fixed

---

**Bug reported**: [Current date]  
**Expected response time**: 24-48 hours for beta issues  
**Beta program support**: High priority during testing period

Thank you for helping improve CCPES v2.0 through thorough bug reporting! 🔍