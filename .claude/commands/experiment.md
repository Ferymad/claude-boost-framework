---
description: Create experiments safely in isolated workspace
argument-hint: [experiment name]
---

🧪 **Create Development Experiment in Isolated Workspace**

**Creating experiment: $ARGUMENTS**

1. **EXPERIMENT LOCATION**: `.workspace/experiments/experiment_$ARGUMENTS.py`
2. **ISOLATED ENVIRONMENT**: Zero impact on main project repository
3. **PROJECT ACCESS**: Reference real code via symlinks in `.workspace/`
4. **DISPOSABLE WORK**: Can delete entire experiment without consequences
5. **AUTOMATIC REDIRECTION**: Workspace manager ensures proper isolation

**🛡️ REPOSITORY PROTECTION**: Experiment files cannot pollute project root
**🔗 FULL ACCESS**: Use project code via `.workspace/` symlinks  
**♻️ CLEANUP**: Archive or delete when experiment complete

**Safe to experiment - main repository stays pristine!**