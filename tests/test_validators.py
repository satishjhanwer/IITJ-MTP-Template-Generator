"""Tests for input validation utilities."""

import os
import tempfile
from scripts.utils.validators import (
    validate_email,
    validate_required_fields,
    validate_file_path,
    validate_date_format,
    sanitize_latex,
    validate_config
)


class TestValidateEmail:
    """Tests for validate_email function."""
    
    def test_valid_email_basic(self):
        """Test valid basic email."""
        assert validate_email("user@example.com") is True
    
    def test_valid_email_with_dots(self):
        """Test valid email with dots."""
        assert validate_email("user.name@example.co.uk") is True
    
    def test_valid_email_with_numbers(self):
        """Test valid email with numbers."""
        assert validate_email("user123@example456.com") is True
    
    def test_valid_email_with_hyphen(self):
        """Test valid email with hyphen."""
        assert validate_email("user-name@example-domain.com") is True
    
    def test_valid_email_with_plus(self):
        """Test valid email with plus sign."""
        assert validate_email("user+tag@example.com") is True
    
    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        assert validate_email("userexample.com") is False
    
    def test_invalid_email_no_domain(self):
        """Test invalid email without domain extension."""
        assert validate_email("user@example") is False
    
    def test_invalid_email_multiple_at(self):
        """Test invalid email with multiple @ symbols."""
        assert validate_email("user@name@example.com") is False
    
    def test_invalid_email_empty(self):
        """Test invalid empty email."""
        assert validate_email("") is False
    
    def test_invalid_email_space(self):
        """Test invalid email with space."""
        assert validate_email("user @example.com") is False
    
    def test_invalid_email_no_local_part(self):
        """Test invalid email without local part."""
        assert validate_email("@example.com") is False


class TestValidateRequiredFields:
    """Tests for validate_required_fields function."""
    
    def test_all_fields_present(self):
        """Test when all required fields are present."""
        data = {"name": "John", "email": "john@example.com"}
        missing = validate_required_fields(data, ["name", "email"])
        assert missing == []
    
    def test_missing_single_field(self):
        """Test when one field is missing."""
        data = {"name": "John"}
        missing = validate_required_fields(data, ["name", "email"])
        assert "email" in missing
    
    def test_missing_multiple_fields(self):
        """Test when multiple fields are missing."""
        data = {"name": "John"}
        missing = validate_required_fields(data, ["name", "email", "phone"])
        assert "email" in missing
        assert "phone" in missing
    
    def test_empty_field_value(self):
        """Test when field is empty string."""
        data = {"name": "John", "email": ""}
        missing = validate_required_fields(data, ["name", "email"])
        assert "email" in missing
    
    def test_nested_field_present(self):
        """Test nested fields when present."""
        data = {"author": {"name": "John", "email": "john@example.com"}}
        missing = validate_required_fields(data, ["author.name", "author.email"])
        assert missing == []
    
    def test_nested_field_missing(self):
        """Test nested fields when missing."""
        data = {"author": {"name": "John"}}
        missing = validate_required_fields(data, ["author.name", "author.email"])
        assert "author.email" in missing
    
    def test_nested_field_parent_missing(self):
        """Test nested field when parent doesn't exist."""
        data = {}
        missing = validate_required_fields(data, ["author.name"])
        assert "author.name" in missing
    
    def test_nested_field_parent_empty(self):
        """Test nested field when parent is empty."""
        data = {"author": ""}
        missing = validate_required_fields(data, ["author.name"])
        assert "author.name" in missing
    
    def test_empty_data(self):
        """Test with empty data."""
        missing = validate_required_fields({}, ["name", "email"])
        assert len(missing) == 2
    
    def test_empty_required_fields(self):
        """Test with no required fields."""
        data = {"name": "John"}
        missing = validate_required_fields(data, [])
        assert missing == []


class TestValidateFilePath:
    """Tests for validate_file_path function."""
    
    def test_existing_file(self):
        """Test with existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            assert validate_file_path(temp_path) is True
        finally:
            os.unlink(temp_path)
    
    def test_non_existing_file(self):
        """Test with non-existing file."""
        assert validate_file_path("/non/existing/file.txt") is False
    
    def test_directory_path(self):
        """Test with directory path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            assert validate_file_path(temp_dir) is False
    
    def test_empty_path(self):
        """Test with empty path."""
        assert validate_file_path("") is False


class TestValidateDateFormat:
    """Tests for validate_date_format function."""
    
    def test_valid_date_format(self):
        """Test valid date format."""
        assert validate_date_format("November 2024") is True
    
    def test_valid_date_single_letter_month(self):
        """Test valid date with other months."""
        assert validate_date_format("April 2023") is True
        assert validate_date_format("January 2022") is True
    
    def test_invalid_date_lower_case(self):
        """Test invalid date with lowercase month."""
        assert validate_date_format("november 2024") is False
    
    def test_invalid_date_all_caps(self):
        """Test invalid date with all caps month."""
        assert validate_date_format("NOVEMBER 2024") is False
    
    def test_invalid_date_missing_year(self):
        """Test invalid date without year."""
        assert validate_date_format("November") is False
    
    def test_invalid_date_only_numbers(self):
        """Test invalid date with only numbers."""
        assert validate_date_format("11 2024") is False
    
    def test_invalid_date_no_space(self):
        """Test invalid date without space."""
        assert validate_date_format("November2024") is False
    
    def test_invalid_date_swap_order(self):
        """Test invalid date with swapped order."""
        assert validate_date_format("2024 November") is False
    
    def test_invalid_date_empty(self):
        """Test invalid empty date."""
        assert validate_date_format("") is False
    
    def test_invalid_date_lowercase_month(self):
        """Test invalid date with lowercase month."""
        assert validate_date_format("november 2024") is False


class TestSanitizeLatex:
    """Tests for sanitize_latex function."""
    
    def test_backslash_escape(self):
        """Test backslash escaping."""
        result = sanitize_latex("path\\to\\file")
        # Check that backslashes are escaped
        assert "textbackslash" in result
    
    def test_ampersand_escape(self):
        """Test ampersand escaping."""
        result = sanitize_latex("A & B")
        assert r"\&" in result
    
    def test_percent_escape(self):
        """Test percent escaping."""
        result = sanitize_latex("100% complete")
        assert r"\%" in result
    
    def test_dollar_escape(self):
        """Test dollar sign escaping."""
        result = sanitize_latex("$100")
        assert r"\$" in result
    
    def test_hash_escape(self):
        """Test hash escaping."""
        result = sanitize_latex("#include")
        assert r"\#" in result
    
    def test_underscore_escape(self):
        """Test underscore escaping."""
        result = sanitize_latex("variable_name")
        assert r"\_" in result
    
    def test_braces_escape(self):
        """Test braces escaping."""
        result = sanitize_latex("{content}")
        assert r"\{" in result
        assert r"\}" in result
    
    def test_tilde_escape(self):
        """Test tilde escaping."""
        result = sanitize_latex("~user")
        assert r"\textasciitilde{}" in result
    
    def test_caret_escape(self):
        """Test caret escaping."""
        result = sanitize_latex("x^2")
        assert r"\textasciicircum{}" in result
    
    def test_multiple_special_chars(self):
        """Test multiple special characters."""
        result = sanitize_latex("File_1 & File_2 (50%)")
        assert r"\_" in result
        assert r"\&" in result
        assert r"\%" in result
    
    def test_empty_string(self):
        """Test empty string."""
        result = sanitize_latex("")
        assert result == ""
    
    def test_normal_text(self):
        """Test normal text without special characters."""
        text = "This is normal text"
        result = sanitize_latex(text)
        assert result == text


class TestValidateConfig:
    """Tests for validate_config function."""
    
    def test_valid_config(self):
        """Test valid configuration."""
        config = {
            "project": {"title": "My Project", "type": "proposal"},
            "author": {"name": "John Doe", "roll_number": "12345", "email": "john@example.com"},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            }
        }
        is_valid, errors = validate_config(config)
        assert is_valid is True
        assert errors == []
    
    def test_missing_required_field(self):
        """Test config with missing required field."""
        config = {
            "project": {"title": "My Project", "type": "proposal"},
            "author": {"name": "John Doe", "roll_number": "12345"},
            "academic": {
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            }
        }
        is_valid, errors = validate_config(config)
        assert is_valid is False
        assert len(errors) > 0
    
    def test_invalid_email(self):
        """Test config with invalid email."""
        config = {
            "project": {"title": "My Project", "type": "proposal"},
            "author": {"name": "John Doe", "roll_number": "12345", "email": "invalid-email"},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            }
        }
        is_valid, errors = validate_config(config)
        assert is_valid is False
        assert any("email" in error.lower() for error in errors)
    
    def test_invalid_project_type(self):
        """Test config with invalid project type."""
        config = {
            "project": {"title": "My Project", "type": "invalid-type"},
            "author": {"name": "John Doe", "roll_number": "12345", "email": "john@example.com"},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            }
        }
        is_valid, errors = validate_config(config)
        assert is_valid is False
        assert any("project type" in error.lower() for error in errors)
    
    def test_valid_project_types(self):
        """Test all valid project types."""
        base_config = {
            "project": {"title": "My Project", "type": "proposal"},
            "author": {"name": "John Doe", "roll_number": "12345", "email": "john@example.com"},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            }
        }
        
        for ptype in ["proposal", "major-project", "presentation"]:
            config = base_config.copy()
            config["project"] = {"title": "My Project", "type": ptype}
            is_valid, errors = validate_config(config)
            assert is_valid is True, f"Project type {ptype} should be valid"
    
    def test_missing_logo_path(self):
        """Test config with missing logo file."""
        config = {
            "project": {"title": "My Project", "type": "proposal"},
            "author": {"name": "John Doe", "roll_number": "12345", "email": "john@example.com"},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            },
            "assets": {"logo_path": "/non/existing/logo.png"}
        }
        is_valid, errors = validate_config(config)
        assert is_valid is False
        assert any("logo" in error.lower() for error in errors)
    
    def test_valid_logo_path(self):
        """Test config with valid logo file."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            temp_logo = f.name
        
        try:
            config = {
                "project": {"title": "My Project", "type": "proposal"},
                "author": {"name": "John Doe", "roll_number": "12345", "email": "john@example.com"},
                "academic": {
                    "supervisor": "Dr. Smith",
                    "department": "CSE",
                    "university": "IITJ",
                    "degree": "B.Tech"
                },
                "assets": {"logo_path": temp_logo}
            }
            is_valid, errors = validate_config(config)
            assert is_valid is True
        finally:
            os.unlink(temp_logo)
    
    def test_empty_email_field(self):
        """Test config with empty email field."""
        config = {
            "project": {"title": "My Project", "type": "proposal"},
            "author": {"name": "John Doe", "roll_number": "12345", "email": ""},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            }
        }
        is_valid, errors = validate_config(config)
        assert is_valid is True
    
    def test_empty_logo_field(self):
        """Test config with empty logo path field."""
        config = {
            "project": {"title": "My Project", "type": "proposal"},
            "author": {"name": "John Doe", "roll_number": "12345", "email": "john@example.com"},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            },
            "assets": {"logo_path": ""}
        }
        is_valid, errors = validate_config(config)
        assert is_valid is True
