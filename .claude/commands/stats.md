---
description: Display comprehensive analytics dashboard with performance metrics and insights
argument-hint: [dashboard-type: overview|detailed|trends|team]
---

Generate comprehensive analytics dashboard for CCPES v2.0 system performance:

## Analytics Dashboard Generator

Display analytics based on dashboard type: $ARGUMENTS

### Available Dashboard Types

1. **Overview Dashboard** (default)
   - Current session context usage and efficiency
   - Real-time system health status
   - Today's productivity metrics summary
   - Critical alerts and recommendations

2. **Detailed Dashboard**
   - Comprehensive context usage breakdown
   - Hook execution success rates and performance
   - Subagent utilization patterns and efficiency
   - Quality metrics and validation success rates

3. **Trends Dashboard**
   - Historical performance trends (last 7/30 days)
   - Context usage patterns over time
   - Productivity improvement tracking
   - Success metrics progression

4. **Team Dashboard**
   - Team productivity and collaboration metrics
   - Shared workflow adoption rates
   - Template usage statistics
   - Team success metrics comparison

## Comprehensive Analytics Generation

### 1. Context Efficiency Analysis
```bash
# Analyze current context usage
echo "=== CONTEXT USAGE ANALYSIS ==="
echo "Current Session Context: [ESTIMATE]%"
echo "70% Threshold Status: [SAFE/WARNING/CRITICAL]"
echo "Context Efficiency Score: [X/10]"
echo "Recommendations: [OPTIMIZATION_SUGGESTIONS]"
```

### 2. System Performance Metrics
```bash
# Check hook execution statistics
echo "=== SYSTEM AUTOMATION HEALTH ==="
python .claude/analytics/analyze-hook-performance.py
echo "Hook Success Rate: [X]%"
echo "PROJECT_INDEX.json Updates: [X] today"
echo "Average Hook Execution Time: [X]ms"
```

### 3. Subagent Utilization Analysis
```bash
# Analyze subagent usage patterns
echo "=== SUBAGENT PERFORMANCE ==="
echo "Most Used Subagents:"
echo "  1. code-reviewer: [X] invocations (avg: [X]s response)"
echo "  2. blind-validator: [X] invocations ([X]% success rate)"
echo "  3. debugger: [X] invocations"
echo "Delegation Efficiency: [X]% automatic vs manual"
```

### 4. Quality Metrics Dashboard
```bash
# Display quality and success metrics
echo "=== QUALITY & SUCCESS METRICS ==="
echo "Task Completion Accuracy: [X]% (Target: >95%)"
echo "Code Duplication Rate: [X]% (Target: <5%)"
echo "Validation Success Rate: [X]% (Target: >95%)"
echo "Session Continuity Rate: [X]% (Target: >80%)"
```

### 5. Productivity Insights
```bash
# Generate productivity analysis
echo "=== PRODUCTIVITY INSIGHTS ==="
echo "Feature Development Time: [X]% improvement vs baseline"
echo "Context Usage Efficiency: [X]% average per session"
echo "Hook Automation Savings: [X] manual steps automated"
echo "Quality Gate Success: [X]% first-time pass rate"
```

### 6. Performance Trends
```bash
# Show historical trends
python .claude/analytics/generate-trend-analysis.py --days 7
echo "=== 7-DAY PERFORMANCE TRENDS ==="
echo "Context Usage Trend: [IMPROVING/STABLE/DEGRADING]"
echo "Quality Metrics Trend: [IMPROVING/STABLE/DEGRADING]"
echo "Automation Reliability: [IMPROVING/STABLE/DEGRADING]"
```

### 7. Team Collaboration Metrics
```bash
# Team-specific analytics
echo "=== TEAM COLLABORATION METRICS ==="
echo "Workflow Template Usage: [X]% adoption rate"
echo "Shared Subagent Usage: [X] team invocations"
echo "Knowledge Sharing Score: [X/10]"
echo "Team Productivity Index: [X/10]"
```

### 8. Optimization Recommendations
```bash
# Intelligent recommendations engine
echo "=== OPTIMIZATION RECOMMENDATIONS ==="
echo "🔥 HIGH PRIORITY:"
echo "  • [SPECIFIC_RECOMMENDATION_1]"
echo "⚡ MEDIUM PRIORITY:"
echo "  • [SPECIFIC_RECOMMENDATION_2]"
echo "💡 OPPORTUNITIES:"
echo "  • [SPECIFIC_RECOMMENDATION_3]"
```

### 9. Success Metrics Validation
```bash
# Validate against PRD success criteria
echo "=== PRD SUCCESS METRICS VALIDATION ==="
echo "✅ Code Duplication <5%: [STATUS]"
echo "✅ Task Accuracy >95%: [STATUS]"
echo "✅ Context Usage <70%: [STATUS]"
echo "✅ Hook Success >99%: [STATUS]"
echo "✅ Team Adoption >80%: [STATUS]"
```

### 10. Interactive Analytics
```bash
# Generate interactive dashboard
python .claude/analytics/dashboard-generator.py --type $ARGUMENTS
echo "📊 Interactive dashboard generated at: .claude/analytics/dashboard.html"
echo "🔗 View in browser: file://$(pwd)/.claude/analytics/dashboard.html"
```

## Advanced Analytics Features

### Real-time Monitoring
- Live context usage tracking
- Hook execution monitoring
- Subagent performance alerts
- Quality threshold monitoring

### Historical Analysis
- 7/30/90 day trend analysis
- Performance regression detection
- Success metric progression tracking
- Team productivity evolution

### Predictive Insights
- Context usage prediction
- Performance bottleneck forecasting
- Optimization opportunity identification
- Resource planning recommendations

### Custom Metrics
- Project-specific KPI tracking
- Custom validation success rates
- Team-defined productivity metrics
- Business impact measurements

## Usage Patterns

### Daily Monitoring
```bash
> /stats overview  # Quick daily health check
```

### Weekly Reviews
```bash
> /stats trends   # Weekly performance review
```

### Monthly Analysis
```bash
> /stats detailed  # Comprehensive monthly analysis
```

### Team Reviews
```bash
> /stats team     # Team productivity dashboard
```

## Alert Thresholds

### Critical Alerts (Immediate Action)
- Context usage >70%
- Hook failure rate >5%
- Quality metric below target by >10%
- System performance degradation >20%

### Warning Alerts (Monitor Closely)
- Context usage >60%
- Subagent response time >5s
- Validation failure rate >3%
- Team adoption rate declining

### Information Alerts (Optimize When Possible)
- Optimization opportunities identified
- New best practices available
- Performance improvement suggestions
- Team collaboration enhancement tips

---

**Remember**: Analytics drive optimization. Use these insights to continuously improve your development workflow and maintain the high performance standards of CCPES v2.0. Data-driven decisions lead to predictable success.