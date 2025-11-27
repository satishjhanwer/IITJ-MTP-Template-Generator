"""Template rendering utilities for IITJ MTP Template Generator."""

import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict, Any


def setup_jinja_env(template_dir: str) -> Environment:
    """Set up Jinja2 environment for LaTeX templating.
    
    Args:
        template_dir: Directory containing templates
        
    Returns:
        Configured Jinja2 Environment
    """
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']),
        block_start_string='\\BLOCK{',
        block_end_string='}',
        variable_start_string='\\VAR{',
        variable_end_string='}',
        comment_start_string='\\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        lstrip_blocks=True,
    )
    
    # Add custom filters
    env.filters['latex_escape'] = latex_escape
    
    return env


def latex_escape(text: str) -> str:
    """Escape special LaTeX characters.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text safe for LaTeX
    """
    if not isinstance(text, str):
        return text
    
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


def render_template(template_path: str, context: Dict[str, Any], output_path: str) -> None:
    """Render a Jinja2 template to a file.
    
    Args:
        template_path: Path to template file
        context: Template context variables
        output_path: Path to write rendered output
    """
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)
    
    env = setup_jinja_env(template_dir)
    template = env.get_template(template_name)
    
    rendered = template.render(**context)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)


def prepare_context(config: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare template context from configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Context dictionary for template rendering
    """
    context = {
        # Project info
        'TITLE': config.get('project', {}).get('title', ''),
        'PROJECT_TYPE': config.get('project', {}).get('type', ''),
        
        # Author info
        'AUTHOR_NAME': config.get('author', {}).get('name', ''),
        'ROLL_NUMBER': config.get('author', {}).get('roll_number', ''),
        'EMAIL': config.get('author', {}).get('email', ''),
        
        # Academic info
        'SUPERVISOR': config.get('academic', {}).get('supervisor', ''),
        'CO_SUPERVISOR': config.get('academic', {}).get('co_supervisor', ''),
        'SUPERVISOR_DESIGNATION': config.get('academic', {}).get('supervisor_designation', 'Professor'),
        'SUPERVISOR_DEPARTMENT': config.get('academic', {}).get('supervisor_department', 
                                                                config.get('academic', {}).get('department', '')),
        'DEPARTMENT': config.get('academic', {}).get('department', ''),
        'UNIVERSITY': config.get('academic', {}).get('university', ''),
        'DEGREE': config.get('academic', {}).get('degree', ''),
        'SESSION': config.get('academic', {}).get('session', ''),
        
        # Dates
        'SUBMISSION_DATE': config.get('dates', {}).get('submission_date', ''),
        
        # Formatting
        'COLOR_SCHEME': config.get('formatting', {}).get('color_scheme', 'blue'),
        'FONT_SIZE': config.get('formatting', {}).get('font_size', 12),
        'LINE_SPACING': config.get('formatting', {}).get('line_spacing', 1.5),
        'BIBLIOGRAPHY_STYLE': config.get('formatting', {}).get('bibliography_style', 'IEEE'),
        
        # Content options
        'INCLUDE_DECLARATION': config.get('content', {}).get('include_declaration', True),
        'INCLUDE_CERTIFICATE': config.get('content', {}).get('include_certificate', True),
        'INCLUDE_ACKNOWLEDGMENTS': config.get('content', {}).get('include_acknowledgments', True),
        'INCLUDE_ABSTRACT': config.get('content', {}).get('include_abstract', True),
        
        # Assets
        'LOGO_PATH': config.get('assets', {}).get('logo_path', 'logo.png'),
    }
    
    return context
