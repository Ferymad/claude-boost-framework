#!/bin/bash
# Cross-Platform Installation Test Script for Claude Boost
# Tests both NPM and Python installation methods

set -e

echo "🧪 Claude Boost Installation Test Suite"
echo "========================================"

PLATFORM=$(uname -s)
ARCH=$(uname -m)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="test-installation/logs"
TEST_DIR="test-installation/temp_test_${TIMESTAMP}"

mkdir -p "$LOG_DIR"
mkdir -p "$TEST_DIR"

echo "Platform: $PLATFORM $ARCH"
echo "Test Directory: $TEST_DIR"
echo "Log Directory: $LOG_DIR"
echo

# Function to log results
log_result() {
    local test_name="$1"
    local result="$2"
    local message="$3"
    
    if [ "$result" = "PASS" ]; then
        echo "✅ $test_name: PASS - $message" | tee -a "$LOG_DIR/test_results_${TIMESTAMP}.log"
    else
        echo "❌ $test_name: FAIL - $message" | tee -a "$LOG_DIR/test_results_${TIMESTAMP}.log"
    fi
}

# Test 1: Check Prerequisites
echo "🔍 Testing Prerequisites..."
check_prerequisites() {
    local result="PASS"
    local message=""
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        message="Node.js $NODE_VERSION available"
    else
        result="FAIL"
        message="Node.js not found"
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        message="$message, npm $NPM_VERSION available"
    else
        result="FAIL"
        message="$message, npm not found"
    fi
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        message="$message, $PYTHON_VERSION available"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version)
        message="$message, $PYTHON_VERSION available"
    else
        result="WARN"
        message="$message, Python not found (fallback unavailable)"
    fi
    
    log_result "Prerequisites" "$result" "$message"
    return $([ "$result" = "PASS" ] && echo 0 || echo 1)
}

check_prerequisites

# Test 2: NPM Package Creation
echo
echo "📦 Testing NPM Package Creation..."
test_npm_pack() {
    cd claude-boost
    local result="PASS"
    local message=""
    
    if npm pack &> /dev/null; then
        TARBALL=$(ls -t *.tgz | head -1)
        TARBALL_SIZE=$(stat -f%z "$TARBALL" 2>/dev/null || stat -c%s "$TARBALL" 2>/dev/null || echo "unknown")
        message="Package created: $TARBALL (${TARBALL_SIZE} bytes)"
        
        # Move tarball to test directory
        mv "$TARBALL" "../$TEST_DIR/"
        
        # Check package contents
        cd "../$TEST_DIR"
        if tar -tzf "$TARBALL" | head -20 > package_contents.txt; then
            message="$message, contents verified"
        else
            result="FAIL"
            message="$message, failed to verify contents"
        fi
    else
        result="FAIL"
        message="npm pack failed"
    fi
    
    cd ..
    log_result "NPM Pack" "$result" "$message"
    return $([ "$result" = "PASS" ] && echo 0 || echo 1)
}

test_npm_pack

# Test 3: Local Installation Test
echo
echo "⚙️ Testing Local Installation..."
test_local_install() {
    cd "$TEST_DIR"
    local result="PASS"
    local message=""
    
    TARBALL=$(ls *.tgz | head -1)
    
    if npm install "$TARBALL" -g --prefix ./npm_test &> npm_install.log; then
        # Check if binary is accessible
        export PATH="$PWD/npm_test/bin:$PATH"
        
        if command -v claude-boost &> /dev/null; then
            # Test binary execution
            if claude-boost --help &> claude_boost_help.log; then
                message="Global installation successful, binary works"
            else
                result="FAIL"  
                message="Binary installed but doesn't execute properly"
            fi
        else
            result="FAIL"
            message="Binary not found in PATH after installation"
        fi
    else
        result="FAIL"
        message="npm install failed (check npm_install.log)"
    fi
    
    cd ..
    log_result "Local Install" "$result" "$message"
    return $([ "$result" = "PASS" ] && echo 0 || echo 1)
}

test_local_install

# Test 4: Python Installation Test
echo
echo "🐍 Testing Python Installation..."
test_python_install() {
    cd "$TEST_DIR"
    local result="PASS"
    local message=""
    
    # Create virtual environment
    if command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
    elif command -v python &> /dev/null; then
        PYTHON_CMD=python
    else
        result="SKIP"
        message="Python not available"
        log_result "Python Install" "$result" "$message"
        cd ..
        return 0
    fi
    
    if $PYTHON_CMD -m venv python_test_env &> python_venv.log; then
        source python_test_env/bin/activate 2>/dev/null || source python_test_env/Scripts/activate 2>/dev/null
        
        # Install from local directory
        if pip install ../../claude-boost/ &> python_install.log; then
            # Test CLI availability
            if command -v claude-boost &> /dev/null; then
                if claude-boost --help &> python_claude_help.log; then
                    message="Python installation successful, CLI works"
                else
                    result="FAIL"
                    message="CLI installed but doesn't work"
                fi
            else
                result="FAIL"
                message="CLI not available after Python install"
            fi
        else
            result="FAIL"
            message="pip install failed (check python_install.log)"
        fi
        
        deactivate 2>/dev/null || true
    else
        result="FAIL"
        message="Failed to create virtual environment"
    fi
    
    cd ..
    log_result "Python Install" "$result" "$message"
    return $([ "$result" = "PASS" ] && echo 0 || echo 1)
}

test_python_install

# Test 5: Template Files Verification
echo
echo "📄 Testing Template Files..."
test_template_files() {
    cd "$TEST_DIR"
    local result="PASS"
    local message=""
    local template_count=0
    
    # Extract and check template files from NPM package
    TARBALL=$(ls *.tgz | head -1)
    mkdir -p package_extract
    tar -xzf "$TARBALL" -C package_extract
    
    # Count template files
    if [ -d "package_extract/package/claude_boost/templates" ]; then
        template_count=$(find package_extract/package/claude_boost/templates -type f | wc -l)
        
        # Check specific required templates
        required_templates=(
            ".claude/agents/blind-validator.md"
            ".claude/agents/code-reviewer.md"
            ".claude/commands/fresh.md"
            ".claude/hooks/project-indexer.py"
            ".claude/CLAUDE.md"
        )
        
        missing_templates=""
        for template in "${required_templates[@]}"; do
            if [ ! -f "package_extract/package/claude_boost/templates/$template" ]; then
                missing_templates="$missing_templates $template"
            fi
        done
        
        if [ -z "$missing_templates" ]; then
            message="All ${template_count} template files included"
        else
            result="FAIL"
            message="Missing templates:$missing_templates"
        fi
    else
        result="FAIL"
        message="Template directory not found in package"
    fi
    
    cd ..
    log_result "Template Files" "$result" "$message"
    return $([ "$result" = "PASS" ] && echo 0 || echo 1)
}

test_template_files

# Cleanup
echo
echo "🧹 Cleanup..."
if [ -d "$TEST_DIR" ]; then
    rm -rf "$TEST_DIR"
    echo "Test directory cleaned up"
fi

# Summary
echo
echo "📊 Test Summary"
echo "==============="
echo "Results logged to: $LOG_DIR/test_results_${TIMESTAMP}.log"
echo "Platform tested: $PLATFORM $ARCH"

# Count results
TOTAL_TESTS=$(grep -c ":" "$LOG_DIR/test_results_${TIMESTAMP}.log" || echo "0")
PASSED_TESTS=$(grep -c "PASS" "$LOG_DIR/test_results_${TIMESTAMP}.log" || echo "0")
FAILED_TESTS=$(grep -c "FAIL" "$LOG_DIR/test_results_${TIMESTAMP}.log" || echo "0")

echo "Total tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $FAILED_TESTS"

if [ "$FAILED_TESTS" -gt 0 ]; then
    echo
    echo "❌ Some tests failed. Check the log file for details."
    exit 1
else
    echo
    echo "✅ All tests passed! Package is ready for publication."
    exit 0
fi