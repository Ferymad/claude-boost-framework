#!/usr/bin/env python3
"""
Comprehensive test suite for test_module.py
Tests the UserManager class, calculate_tax, validate_email, and format_phone functions
"""

import unittest
import tempfile
import os
import sqlite3
from test_module import UserManager, calculate_tax, validate_email, format_phone


class TestUserManager(unittest.TestCase):
    """Test cases for UserManager class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.database_url = f'sqlite:///{self.temp_db.name}'
        self.user_manager = UserManager(self.database_url)
    
    def tearDown(self):
        """Clean up after each test method"""
        if hasattr(self, 'user_manager') and self.user_manager.connection:
            self.user_manager.connection.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_init_valid_database_url(self):
        """Test UserManager initialization with valid database URL"""
        self.assertEqual(self.user_manager.database_url, self.database_url)
        self.assertIsNotNone(self.user_manager.connection)
        self.assertIsInstance(self.user_manager.connection, sqlite3.Connection)
    
    def test_init_invalid_database_url(self):
        """Test UserManager initialization with invalid database URL"""
        user_manager = UserManager("invalid://url")
        self.assertIsNone(user_manager.connection)
    
    def test_establish_connection_sqlite(self):
        """Test database connection establishment for SQLite"""
        connection = self.user_manager._establish_connection()
        self.assertIsNotNone(connection)
        self.assertIsInstance(connection, sqlite3.Connection)
        connection.close()
    
    def test_establish_connection_invalid_url(self):
        """Test database connection with invalid URL"""
        user_manager = UserManager("invalid://url")
        connection = user_manager._establish_connection()
        self.assertIsNone(connection)
    
    def test_authenticate_user_valid_credentials(self):
        """Test user authentication with valid credentials"""
        result = self.user_manager.authenticate_user("testuser", "password123")
        self.assertTrue(result)
    
    def test_authenticate_user_empty_username(self):
        """Test user authentication with empty username"""
        result = self.user_manager.authenticate_user("", "password123")
        self.assertIsNone(result)
    
    def test_authenticate_user_empty_password(self):
        """Test user authentication with empty password"""
        result = self.user_manager.authenticate_user("testuser", "")
        self.assertIsNone(result)
    
    def test_authenticate_user_none_credentials(self):
        """Test user authentication with None credentials"""
        result = self.user_manager.authenticate_user(None, "password")
        self.assertIsNone(result)
        result = self.user_manager.authenticate_user("user", None)
        self.assertIsNone(result)
    
    def test_authenticate_user_no_connection(self):
        """Test user authentication when database connection is None"""
        user_manager = UserManager("invalid://url")
        result = user_manager.authenticate_user("testuser", "password123")
        self.assertIsNone(result)
    
    def test_create_user_valid_data(self):
        """Test user creation with valid data"""
        user_data = {"username": "newuser", "email": "user@example.com"}
        result = self.user_manager.create_user(user_data)
        self.assertEqual(result, "user_123")
    
    def test_create_user_none_data(self):
        """Test user creation with None data"""
        result = self.user_manager.create_user(None)
        self.assertIsNone(result)
    
    def test_create_user_invalid_data_type(self):
        """Test user creation with invalid data type"""
        result = self.user_manager.create_user("not_a_dict")
        self.assertIsNone(result)
    
    def test_create_user_empty_dict(self):
        """Test user creation with empty dictionary"""
        result = self.user_manager.create_user({})
        self.assertIsNone(result)
    
    def test_create_user_no_connection(self):
        """Test user creation when database connection is None"""
        user_manager = UserManager("invalid://url")
        user_data = {"username": "newuser", "email": "user@example.com"}
        result = user_manager.create_user(user_data)
        self.assertIsNone(result)


class TestCalculateTax(unittest.TestCase):
    """Test cases for calculate_tax function"""
    
    def test_calculate_tax_valid_inputs(self):
        """Test tax calculation with valid inputs"""
        result = calculate_tax(100.0, 0.10)
        self.assertEqual(result, 10.0)
        
        result = calculate_tax(250, 0.15)
        self.assertEqual(result, 37.5)
        
        result = calculate_tax(0, 0.10)
        self.assertEqual(result, 0.0)
    
    def test_calculate_tax_zero_rate(self):
        """Test tax calculation with zero rate"""
        result = calculate_tax(100.0, 0.0)
        self.assertEqual(result, 0.0)
    
    def test_calculate_tax_none_amount(self):
        """Test tax calculation with None amount"""
        result = calculate_tax(None, 0.10)
        self.assertIsNone(result)
    
    def test_calculate_tax_none_rate(self):
        """Test tax calculation with None rate"""
        result = calculate_tax(100.0, None)
        self.assertIsNone(result)
    
    def test_calculate_tax_both_none(self):
        """Test tax calculation with both parameters None"""
        result = calculate_tax(None, None)
        self.assertIsNone(result)
    
    def test_calculate_tax_invalid_amount_type(self):
        """Test tax calculation with invalid amount type"""
        result = calculate_tax("100", 0.10)
        self.assertIsNone(result)
        
        result = calculate_tax([100], 0.10)
        self.assertIsNone(result)
    
    def test_calculate_tax_invalid_rate_type(self):
        """Test tax calculation with invalid rate type"""
        result = calculate_tax(100.0, "0.10")
        self.assertIsNone(result)
        
        result = calculate_tax(100.0, [0.10])
        self.assertIsNone(result)
    
    def test_calculate_tax_negative_amount(self):
        """Test tax calculation with negative amount"""
        result = calculate_tax(-100.0, 0.10)
        self.assertIsNone(result)
    
    def test_calculate_tax_negative_rate(self):
        """Test tax calculation with negative rate"""
        result = calculate_tax(100.0, -0.10)
        self.assertIsNone(result)


class TestValidateEmail(unittest.TestCase):
    """Test cases for validate_email function"""
    
    def test_validate_email_valid_addresses(self):
        """Test email validation with valid email addresses"""
        self.assertTrue(validate_email("user@example.com"))
        self.assertTrue(validate_email("test.email@domain.org"))
        self.assertTrue(validate_email("User@Example.COM"))  # Should handle case
        self.assertTrue(validate_email("  user@example.com  "))  # Should handle whitespace
    
    def test_validate_email_invalid_addresses(self):
        """Test email validation with invalid email addresses"""
        self.assertFalse(validate_email("user.example.com"))  # No @
        self.assertFalse(validate_email("user@"))  # No domain
        self.assertFalse(validate_email("@example.com"))  # No user
        self.assertFalse(validate_email("user@@example.com"))  # Multiple @
        self.assertFalse(validate_email("user@example"))  # No dot in domain
    
    def test_validate_email_empty_string(self):
        """Test email validation with empty string"""
        self.assertFalse(validate_email(""))
        self.assertFalse(validate_email("   "))  # Whitespace only
    
    def test_validate_email_none_input(self):
        """Test email validation with None input"""
        result = validate_email(None)
        self.assertIsNone(result)
    
    def test_validate_email_invalid_type(self):
        """Test email validation with invalid input type"""
        result = validate_email(123)
        self.assertIsNone(result)
        
        result = validate_email(["user@example.com"])
        self.assertIsNone(result)


class TestFormatPhone(unittest.TestCase):
    """Test cases for format_phone function"""
    
    def test_format_phone_valid_inputs(self):
        """Test phone formatting with valid inputs"""
        self.assertEqual(format_phone("123-456-7890"), "1234567890")
        self.assertEqual(format_phone("(123) 456-7890"), "1234567890")
        self.assertEqual(format_phone("123 456 7890"), "1234567890")
        self.assertEqual(format_phone("1234567890"), "1234567890")
    
    def test_format_phone_mixed_formatting(self):
        """Test phone formatting with mixed formatting"""
        self.assertEqual(format_phone("(123)-456 7890"), "1234567890")
        self.assertEqual(format_phone("123-(456) 7890"), "1234567890")
    
    def test_format_phone_none_input(self):
        """Test phone formatting with None input"""
        result = format_phone(None)
        self.assertIsNone(result)
    
    def test_format_phone_invalid_type(self):
        """Test phone formatting with invalid input type"""
        result = format_phone(1234567890)
        self.assertIsNone(result)
        
        result = format_phone(["123-456-7890"])
        self.assertIsNone(result)
    
    def test_format_phone_non_digit_characters(self):
        """Test phone formatting with non-digit characters"""
        result = format_phone("123-456-abcd")
        self.assertIsNone(result)
        
        result = format_phone("123-456-789x")
        self.assertIsNone(result)
    
    def test_format_phone_empty_string(self):
        """Test phone formatting with empty string"""
        result = format_phone("")
        self.assertIsNone(result)
    
    def test_format_phone_only_separators(self):
        """Test phone formatting with only separators"""
        result = format_phone("()-")
        self.assertIsNone(result)
        
        result = format_phone("   ")
        self.assertIsNone(result)


if __name__ == '__main__':
    # Run the tests with verbose output
    unittest.main(verbosity=2)