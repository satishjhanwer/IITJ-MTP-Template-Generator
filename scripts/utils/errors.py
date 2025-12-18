"""Enhanced error messages with helpful suggestions.

This module provides user-friendly error messages with actionable suggestions
and links to documentation.
"""

from typing import List, Optional


class GeneratorError(Exception):
    """Base exception for generator errors."""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None, 
                 doc_link: Optional[str] = None):
        """Initialize error with message, suggestions, and documentation link.
        
        Args:
            message: Error message
            suggestions: List of helpful suggestions
            doc_link: Link to relevant documentation
        """
        self.message = message
        self.suggestions = suggestions or []
        self.doc_link = doc_link
        super().__init__(self.format_error())
    
    def format_error(self) -> str:
        """Format error message with suggestions and documentation link."""
        lines = [f"\n❌ Error: {self.message}"]
        
        if self.suggestions:
            lines.append("\n💡 Suggestions:")
            for suggestion in self.suggestions:
                lines.append(f"   • {suggestion}")
        
        if self.doc_link:
            lines.append(f"\n📖 Documentation: {self.doc_link}")
        
        return "\n".join(lines)


class ConfigurationError(GeneratorError):
    """Configuration-related errors."""
    pass


class TemplateError(GeneratorError):
    """Template-related errors."""
    pass


class FileError(GeneratorError):
    """File operation errors."""
    pass


class ValidationError(GeneratorError):
    """Validation errors."""
    pass


# Common error scenarios with helpful messages

def config_file_not_found(path: str) -> ConfigurationError:
    """Error when configuration file is not found."""
    return ConfigurationError(
        f"Configuration file not found: {path}",
        suggestions=[
            "Check that the file path is correct",
            "Ensure the file exists in the specified location",
            "Try using an absolute path instead of relative",
            "Run in interactive mode: python scripts/generate.py"
        ],
        doc_link="https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/input-schema"
    )


def invalid_yaml_syntax(path: str, error: str) -> ConfigurationError:
    """Error when YAML file has syntax errors."""
    return ConfigurationError(
        f"Invalid YAML syntax in {path}: {error}",
        suggestions=[
            "Check for proper indentation (use spaces, not tabs)",
            "Ensure all strings with special characters are quoted",
            "Validate your YAML at https://www.yamllint.com/",
            "Compare with example configs in examples/ directory"
        ],
        doc_link="https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/quickstart"
    )


def missing_required_field(field: str, section: str) -> ValidationError:
    """Error when required configuration field is missing."""
    return ValidationError(
        f"Missing required field '{field}' in '{section}' section",
        suggestions=[
            f"Add '{field}' to your configuration file",
            f"Check the example configs in examples/ directory",
            "Refer to the input schema documentation for required fields"
        ],
        doc_link="https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/input-schema"
    )


def invalid_project_type(provided: str) -> ValidationError:
    """Error when project type is invalid."""
    return ValidationError(
        f"Invalid project type: '{provided}'",
        suggestions=[
            "Valid types are: 'proposal', 'major-project', 'presentation'",
            "Check your config file's 'project.type' field",
            "Use interactive mode to select the correct type"
        ],
        doc_link="https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/quickstart"
    )


def template_not_found(template_type: str, path: str) -> TemplateError:
    """Error when template directory is not found."""
    return TemplateError(
        f"Template directory not found for '{template_type}' at {path}",
        suggestions=[
            "Ensure you're running the script from the project root",
            "Check that templates/ directory exists",
            "Verify the repository is complete (not corrupted)",
            "Try re-cloning the repository"
        ],
        doc_link="https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/"
    )


def output_directory_exists(path: str) -> FileError:
    """Error when output directory already exists."""
    return FileError(
        f"Output directory already exists: {path}",
        suggestions=[
            "Remove or rename the existing directory",
            "Specify a different output directory with --output flag",
            "Backup the existing directory if it contains important work"
        ]
    )


def latex_compilation_failed(error: str) -> GeneratorError:
    """Error when LaTeX compilation fails."""
    return GeneratorError(
        f"LaTeX compilation failed: {error}",
        suggestions=[
            "Check the LaTeX log file for detailed errors",
            "Ensure LaTeX is installed (TeX Live, MiKTeX, or MacTeX)",
            "Verify all required LaTeX packages are installed",
            "Try compiling manually to see the full error output"
        ],
        doc_link="https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/faq"
    )


def content_extraction_failed(report_path: str, error: str) -> GeneratorError:
    """Error when content extraction fails."""
    return GeneratorError(
        f"Content extraction failed from {report_path}: {error}",
        suggestions=[
            "Verify the report file is valid LaTeX",
            "Check that the file path is correct",
            "Ensure the report uses standard section names",
            "Try generating without extraction (set extract_from_report: false)"
        ],
        doc_link="https://satishjhanwer.github.io/IITJ-MTP-Template-Generator/content-extraction"
    )
