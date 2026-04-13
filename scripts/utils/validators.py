"""Input validation utilities for IITJ MTP Template Generator."""

import os
import re
from typing import Dict, List


def validate_email(email: str) -> bool:
    """Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if email is valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_required_fields(data: Dict, required_fields: List[str]) -> List[str]:
    """Check for missing required fields.

    Args:
        data: Dictionary of user inputs
        required_fields: List of required field names (dot-notation for nested keys)

    Returns:
        List of missing field names
    """
    missing = []
    for field in required_fields:
        if "." in field:
            parts = field.split(".")
            current = data
            for part in parts:
                if (
                    not isinstance(current, dict)
                    or part not in current
                    or not current[part]
                ):
                    missing.append(field)
                    break
                current = current[part]
        else:
            if field not in data or not data[field]:
                missing.append(field)
    return missing


def validate_file_path(path: str) -> bool:
    """Validate that a file path exists.

    Args:
        path: File path to validate

    Returns:
        True if file exists, False otherwise
    """
    return os.path.isfile(path)


def validate_date_format(date_str: str) -> bool:
    """Validate date format (Month Year, e.g., 'November 2024').

    Args:
        date_str: Date string to validate

    Returns:
        True if format is valid, False otherwise
    """
    pattern = r"^[A-Z][a-z]+\s+\d{4}$"
    return bool(re.match(pattern, date_str))


def sanitize_latex(text: str) -> str:
    """Escape special LaTeX characters in a single pass to avoid corruption.

    Uses a regex substitution so that no replacement string is re-scanned,
    which prevents sequences like \\textbackslash{} from having their braces
    re-escaped on a second pass.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text safe for LaTeX
    """
    _latex_escape_map = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return re.sub(r"[\\{}&%$#_~^]", lambda m: _latex_escape_map[m.group()], text)


def validate_config(config: Dict) -> tuple[bool, List[str]]:
    """Validate complete configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    required = [
        "project.title",
        "project.type",
        "author.name",
        "author.roll_number",
        "academic.supervisor",
        "academic.department",
        "academic.university",
        "academic.degree",
    ]

    missing = validate_required_fields(config, required)
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")

    if "author" in config and "email" in config["author"] and config["author"]["email"]:
        if not validate_email(config["author"]["email"]):
            errors.append(f"Invalid email format: {config['author']['email']}")

    if "project" in config and "type" in config["project"]:
        valid_types = ["proposal", "major-project", "presentation"]
        if config["project"]["type"] not in valid_types:
            ptype = config["project"]["type"]
            errors.append(
                f"Invalid project type: {ptype}. Must be one of {valid_types}"
            )

    if (
        "assets" in config
        and "logo_path" in config["assets"]
        and config["assets"]["logo_path"]
    ):
        if not validate_file_path(config["assets"]["logo_path"]):
            errors.append(f"Logo file not found: {config['assets']['logo_path']}")

    return len(errors) == 0, errors
