---
description: Create tests in isolated workspace  
argument-hint: [test description]
---

🧪 **Create Tests in Proper Isolated Location**

**Creating test for: $ARGUMENTS**

1. **TEST LOCATION**: `.workspace/experiments/test_$ARGUMENTS.py`
2. **ISOLATION FIRST**: All test files automatically go to workspace
3. **PROJECT ACCESS**: Import real code via `.workspace/` symlinks
4. **PROMOTION PATH**: Move to real `/tests/` directory when ready
5. **ZERO POLLUTION**: Never create test files in project root

**🛡️ AUTOMATIC PROTECTION**: Test files cannot clutter main repository
**🔄 WORKSPACE REDIRECTION**: Hook system ensures proper placement
**⬆️ PROMOTION READY**: Easy to move to official test suite when complete

**Test safely - repository stays clean automatically!**