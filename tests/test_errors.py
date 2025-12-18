"""Tests for error handling utilities."""

import pytest
from scripts.utils.errors import (
    GeneratorError,
    ConfigurationError,
    TemplateError,
    FileError,
    ValidationError,
    config_file_not_found,
    invalid_yaml_syntax,
    missing_required_field,
    invalid_project_type,
    template_not_found,
    output_directory_exists,
    latex_compilation_failed,
    content_extraction_failed
)


class TestGeneratorError:
    """Tests for GeneratorError base class."""
    
    def test_error_with_message_only(self):
        """Test error with just a message."""
        error = GeneratorError("Test error")
        assert "Test error" in str(error)
        assert "❌ Error:" in str(error)
    
    def test_error_with_suggestions(self):
        """Test error with suggestions."""
        error = GeneratorError(
            "Test error",
            suggestions=["Suggestion 1", "Suggestion 2"]
        )
        error_str = str(error)
        assert "💡 Suggestions:" in error_str
        assert "Suggestion 1" in error_str
        assert "Suggestion 2" in error_str
    
    def test_error_with_doc_link(self):
        """Test error with documentation link."""
        error = GeneratorError(
            "Test error",
            doc_link="https://example.com/docs"
        )
        error_str = str(error)
        assert "📖 Documentation:" in error_str
        assert "https://example.com/docs" in error_str
    
    def test_error_with_all_fields(self):
        """Test error with all fields."""
        error = GeneratorError(
            "Test error",
            suggestions=["Fix this"],
            doc_link="https://example.com"
        )
        error_str = str(error)
        assert "Test error" in error_str
        assert "Fix this" in error_str
        assert "https://example.com" in error_str


class TestSpecificErrors:
    """Tests for specific error types."""
    
    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Config error")
        assert isinstance(error, GeneratorError)
        assert "Config error" in str(error)
    
    def test_template_error(self):
        """Test TemplateError."""
        error = TemplateError("Template error")
        assert isinstance(error, GeneratorError)
    
    def test_file_error(self):
        """Test FileError."""
        error = FileError("File error")
        assert isinstance(error, GeneratorError)
    
    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Validation error")
        assert isinstance(error, GeneratorError)


class TestErrorHelpers:
    """Tests for error helper functions."""
    
    def test_config_file_not_found(self):
        """Test config_file_not_found helper."""
        error = config_file_not_found("config.yaml")
        assert isinstance(error, ConfigurationError)
        assert "config.yaml" in str(error)
        assert "Suggestions:" in str(error)
        assert "Documentation:" in str(error)
    
    def test_invalid_yaml_syntax(self):
        """Test invalid_yaml_syntax helper."""
        error = invalid_yaml_syntax("config.yaml", "unexpected character")
        assert isinstance(error, ConfigurationError)
        assert "config.yaml" in str(error)
        assert "unexpected character" in str(error)
        assert "yamllint" in str(error)
    
    def test_missing_required_field(self):
        """Test missing_required_field helper."""
        error = missing_required_field("title", "project")
        assert isinstance(error, ValidationError)
        assert "title" in str(error)
        assert "project" in str(error)
    
    def test_invalid_project_type(self):
        """Test invalid_project_type helper."""
        error = invalid_project_type("invalid-type")
        assert isinstance(error, ValidationError)
        assert "invalid-type" in str(error)
        assert "proposal" in str(error)
        assert "major-project" in str(error)
        assert "presentation" in str(error)
    
    def test_template_not_found(self):
        """Test template_not_found helper."""
        error = template_not_found("proposal", "/path/to/templates")
        assert isinstance(error, TemplateError)
        assert "proposal" in str(error)
        assert "/path/to/templates" in str(error)
    
    def test_output_directory_exists(self):
        """Test output_directory_exists helper."""
        error = output_directory_exists("/path/to/output")
        assert isinstance(error, FileError)
        assert "/path/to/output" in str(error)
        assert "Remove or rename" in str(error)
    
    def test_latex_compilation_failed(self):
        """Test latex_compilation_failed helper."""
        error = latex_compilation_failed("undefined control sequence")
        assert isinstance(error, GeneratorError)
        assert "undefined control sequence" in str(error)
        assert "LaTeX" in str(error)
    
    def test_content_extraction_failed(self):
        """Test content_extraction_failed helper."""
        error = content_extraction_failed("report.tex", "parse error")
        assert isinstance(error, GeneratorError)
        assert "report.tex" in str(error)
        assert "parse error" in str(error)
