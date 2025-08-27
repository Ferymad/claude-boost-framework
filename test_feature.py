#!/usr/bin/env python3
"""
Test feature for demonstrating Phase 3 automation workflow
This file contains intentional issues to test validation systems
"""

def insecure_login(username, password):
    """Login function with security issues for testing"""
    # This should be caught by pre-commit validation
    api_key = "sk-test123456789abcdef"  # Hardcoded API key - should trigger warning
    
    if password == "admin123":  # Hardcoded password - should trigger warning
        return True
    
    # TODO: Fix this security issue  # Should trigger warning for production code
    return False

def format_user_data(name, email):
    """Format user data with debug prints"""
    print(f"Debug: formatting data for {name}")  # Debug print - should trigger warning
    
    if not email:
        return None
        
    return {
        "name": name,
        "email": email.lower(),
        "formatted": True
    }

# Test function to verify system works
def test_workflow():
    """Test function to verify automation workflow"""
    result = format_user_data("Test User", "test@example.com")
    return result is not None