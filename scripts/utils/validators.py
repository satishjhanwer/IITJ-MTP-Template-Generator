"""Input validation utilities for IITJ MTP Template Generator."""

import re
import os
from typing import Dict, List, Optional


def validate_email(email: str) -> bool:
    """Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_required_fields(data: Dict, required_fields: List[str]) -> List[str]:
    """Check for missing required fields.
    
    Args:
        data: Dictionary of user inputs
        required_fields: List of required field names
        
    Returns:
        List of missing field names
    """
    missing = []
    for field in required_fields:
        if '.' in field:
            # Nested field (e.g., 'author.name')
            parts = field.split('.')
            current = data
            for part in parts:
                if not isinstance(current, dict) or part not in current or not current[part]:
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
    # Simple validation for "Month Year" format
    pattern = r'^[A-Z][a-z]+\s+\d{4}$'
    return bool(re.match(pattern, date_str))


def sanitize_latex(text: str) -> str:
    """Escape special LaTeX characters.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text safe for LaTeX
    """
    # LaTeX special characters that need escaping
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    
    result = text
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
    
    return result


def validate_config(config: Dict) -> tuple[bool, List[str]]:
    """Validate complete configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required fields
    required = [
        'project.title',
        'project.type',
        'author.name',
        'author.roll_number',
        'academic.supervisor',
        'academic.department',
        'academic.university',
        'academic.degree',
    ]
    
    missing = validate_required_fields(config, required)
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")
    
    # Validate email if provided
    if 'author' in config and 'email' in config['author'] and config['author']['email']:
        if not validate_email(config['author']['email']):
            errors.append(f"Invalid email format: {config['author']['email']}")
    
    # Validate project type
    if 'project' in config and 'type' in config['project']:
        valid_types = ['proposal', 'major-project', 'presentation']
        if config['project']['type'] not in valid_types:
            errors.append(f"Invalid project type: {config['project']['type']}. Must be one of {valid_types}")
    
    # Validate logo path if provided
    if 'assets' in config and 'logo_path' in config['assets'] and config['assets']['logo_path']:
        if not validate_file_path(config['assets']['logo_path']):
            errors.append(f"Logo file not found: {config['assets']['logo_path']}")
    
    return len(errors) == 0, errors
