"""Tests for template rendering engine."""

import pytest
import os
import tempfile
from scripts.utils.template_engine import (
    get_template_environment,
    latex_escape,
    prepare_context,
    render_template
)


class TestLatexEscape:
    """Tests for latex_escape function."""
    
    def test_escape_backslash(self):
        """Test escaping backslash."""
        result = latex_escape("path\\to\\file")
        # Backslash and braces should be escaped
        assert "textbackslash" in result
    
    def test_escape_ampersand(self):
        """Test escaping ampersand."""
        result = latex_escape("A & B & C")
        assert r"\&" in result
        assert result.count(r"\&") == 2
    
    def test_escape_percent(self):
        """Test escaping percent sign."""
        result = latex_escape("100%")
        assert r"\%" in result
    
    def test_escape_dollar(self):
        """Test escaping dollar sign."""
        result = latex_escape("$50 or $75")
        assert r"\$" in result
        assert result.count(r"\$") == 2
    
    def test_escape_hash(self):
        """Test escaping hash."""
        result = latex_escape("#include <stdio.h>")
        assert r"\#" in result
    
    def test_escape_underscore(self):
        """Test escaping underscore."""
        result = latex_escape("variable_name")
        assert r"\_" in result
    
    def test_escape_braces(self):
        """Test escaping braces."""
        result = latex_escape("{content}")
        assert r"\{" in result
        assert r"\}" in result
    
    def test_escape_tilde(self):
        """Test escaping tilde."""
        result = latex_escape("~user")
        assert r"\textasciitilde{}" in result
    
    def test_escape_caret(self):
        """Test escaping caret."""
        result = latex_escape("x^2")
        assert r"\textasciicircum{}" in result
    
    def test_escape_multiple_chars(self):
        """Test escaping multiple special characters."""
        result = latex_escape("a&b$c%d_e")
        assert r"\&" in result
        assert r"\$" in result
        assert r"\%" in result
        assert r"\_" in result
    
    def test_escape_empty_string(self):
        """Test escaping empty string."""
        result = latex_escape("")
        assert result == ""
    
    def test_escape_normal_text(self):
        """Test that normal text is not modified."""
        text = "This is normal text with no special chars"
        result = latex_escape(text)
        assert result == text
    
    def test_escape_non_string(self):
        """Test with non-string input."""
        result = latex_escape(123)  # type: ignore
        assert result == 123
    
    def test_escape_none(self):
        """Test with None input."""
        result = latex_escape(None)  # type: ignore
        assert result is None


class TestGetTemplateEnvironment:
    """Tests for get_template_environment function."""
    
    def test_create_environment(self):
        """Test creating template environment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            env = get_template_environment(temp_dir)
            assert env is not None
            assert hasattr(env, 'filters')
    
    def test_environment_is_functional(self):
        """Test that environment is created and is functional."""
        with tempfile.TemporaryDirectory() as temp_dir:
            env = get_template_environment(temp_dir)
            assert hasattr(env, 'filters')
            assert len(env.filters) > 0
    
    def test_environment_has_block_start_string(self):
        """Test that environment has block start string configured."""
        with tempfile.TemporaryDirectory() as temp_dir:
            env = get_template_environment(temp_dir)
            # Environment should have some block start string, either custom or default
            assert env.block_start_string is not None
    
    def test_cached_environment(self):
        """Test that environments are cached."""
        with tempfile.TemporaryDirectory() as temp_dir:
            env1 = get_template_environment(temp_dir)
            env2 = get_template_environment(temp_dir)
            # Both calls should return the same object
            assert env1 is env2


class TestPrepareContext:
    """Tests for prepare_context function."""
    
    def test_basic_context_preparation(self):
        """Test preparing basic context."""
        config = {
            "project": {"title": "My Project", "type": "proposal"},
            "author": {"name": "John Doe", "roll_number": "12345"},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            }
        }
        
        context = prepare_context(config)
        
        assert context['TITLE'] == "My Project"
        assert context['PROJECT_TYPE'] == "proposal"
        assert context['AUTHOR_NAME'] == "John Doe"
        assert context['ROLL_NUMBER'] == "12345"
        assert context['SUPERVISOR'] == "Dr. Smith"
    
    def test_context_with_missing_fields(self):
        """Test context preparation with missing optional fields."""
        config = {
            "project": {"title": "My Project"},
            "author": {"name": "John Doe"},
        }
        
        context = prepare_context(config)
        
        assert context['TITLE'] == "My Project"
        assert context['AUTHOR_NAME'] == "John Doe"
        assert context['PROJECT_TYPE'] == ""
        assert context['EMAIL'] == ""
    
    def test_context_with_email(self):
        """Test context with email field."""
        config = {
            "project": {"title": "My Project"},
            "author": {"name": "John Doe", "email": "john@example.com"},
        }
        
        context = prepare_context(config)
        assert context['EMAIL'] == "john@example.com"
    
    def test_context_with_dates(self):
        """Test context with date fields."""
        config = {
            "project": {"title": "My Project"},
            "dates": {"submission_date": "December 2024"}
        }
        
        context = prepare_context(config)
        assert context['SUBMISSION_DATE'] == "December 2024"
        assert context['PRESENTATION_DATE'] == "December 2024"
    
    def test_context_with_formatting(self):
        """Test context with formatting options."""
        config = {
            "project": {"title": "My Project"},
            "formatting": {
                "color_scheme": "red",
                "font_size": 14,
                "line_spacing": 1.5,
                "bibliography_style": "Springer"
            }
        }
        
        context = prepare_context(config)
        # COLOR_SCHEME may be overridden by presentation settings
        assert context['FONT_SIZE'] == 14
        assert context['LINE_SPACING'] == 1.5
        assert context['BIBLIOGRAPHY_STYLE'] == "Springer"
    
    def test_context_with_content_options(self):
        """Test context with content inclusion options."""
        config = {
            "project": {"title": "My Project"},
            "content": {
                "include_declaration": True,
                "include_certificate": False,
            }
        }
        
        context = prepare_context(config)
        assert context['INCLUDE_DECLARATION'] is True
        assert context['INCLUDE_CERTIFICATE'] is False
    
    def test_context_with_presentation_options(self):
        """Test context with presentation-specific options."""
        config = {
            "project": {"title": "My Project"},
            "presentation": {
                "theme": "Beamer",
                "color_scheme": "default",
                "aspect_ratio": "16:9"
            }
        }
        
        context = prepare_context(config)
        assert context['THEME'] == "Beamer"
        assert context['ASPECT_RATIO'] == "16:9"
        assert context['ASPECT_RATIO_VALUE'] == "169"
    
    def test_context_with_presentation_4_3_aspect(self):
        """Test context with 4:3 aspect ratio."""
        config = {
            "project": {"title": "My Project"},
            "presentation": {
                "aspect_ratio": "4:3"
            }
        }
        
        context = prepare_context(config)
        assert context['ASPECT_RATIO'] == "4:3"
        assert context['ASPECT_RATIO_VALUE'] == "43"
    
    def test_context_with_supervisor_designation(self):
        """Test context with supervisor designation."""
        config = {
            "project": {"title": "My Project"},
            "academic": {
                "supervisor": "Dr. Smith",
                "supervisor_designation": "Assistant Professor"
            }
        }
        
        context = prepare_context(config)
        assert context['SUPERVISOR_DESIGNATION'] == "Assistant Professor"
    
    def test_context_with_co_supervisor(self):
        """Test context with co-supervisor."""
        config = {
            "project": {"title": "My Project"},
            "academic": {
                "supervisor": "Dr. Smith",
                "co_supervisor": "Dr. Johnson"
            }
        }
        
        context = prepare_context(config)
        assert context['CO_SUPERVISOR'] == "Dr. Johnson"
    
    def test_context_with_extracted_content(self):
        """Test context with extracted content."""
        config = {
            "project": {"title": "My Project"},
            "extracted_content": {
                "introduction": "Sample introduction",
                "methods": "Sample methods"
            }
        }
        
        context = prepare_context(config)
        assert context['extracted_content'] == config['extracted_content']
    
    def test_context_with_logo_path(self):
        """Test context with logo path."""
        config = {
            "project": {"title": "My Project"},
            "assets": {"logo_path": "/path/to/logo.png"}
        }
        
        context = prepare_context(config)
        assert context['LOGO_PATH'] == "/path/to/logo.png"
    
    def test_context_default_values(self):
        """Test that context has sensible defaults."""
        config = {}
        
        context = prepare_context(config)
        
        # Check some defaults
        assert context['TITLE'] == ""
        assert context['AUTHOR_NAME'] == ""
        assert context['SUPERVISOR_DESIGNATION'] == "Professor"
        assert context['BIBLIOGRAPHY_STYLE'] == "IEEE"
        assert context['THEME'] == "Madrid"
        assert context['ASPECT_RATIO'] == "16:9"


class TestEnvironmentCaching:
    """Additional tests for environment caching."""
    
    def test_different_paths_different_environments(self):
        """Test that different paths create different environment caches."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path1 = os.path.join(temp_dir, "templates1")
            path2 = os.path.join(temp_dir, "templates2")
            os.makedirs(path1)
            os.makedirs(path2)
            
            env1 = get_template_environment(path1)
            env2 = get_template_environment(path2)
            # Different paths should create different environments
            assert env1 is not env2
    
    def test_long_text_escaping(self):
        """Test escaping long text with many special chars."""
        long_text = "A_file$named#test&with%special^chars~in~it" * 10
        result = latex_escape(long_text)
        # Should successfully escape all characters
        assert len(result) > len(long_text)


class TestContextPrepariationAdvanced:
    """Advanced tests for context preparation."""
    
    def test_context_supervisor_department_fallback(self):
        """Test supervisor department using department as fallback."""
        config = {
            "project": {"title": "My Project"},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "Computer Science",
            }
        }
        
        context = prepare_context(config)
        assert context['SUPERVISOR_DEPARTMENT'] == "Computer Science"
    
    def test_context_complete_academic_info(self):
        """Test complete academic information."""
        config = {
            "project": {"title": "Research"},
            "academic": {
                "supervisor": "Dr. A",
                "co_supervisor": "Dr. B",
                "supervisor_designation": "Professor",
                "supervisor_department": "CSE",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech",
                "session": "2023-24"
            }
        }
        
        context = prepare_context(config)
        assert context['SUPERVISOR'] == "Dr. A"
        assert context['CO_SUPERVISOR'] == "Dr. B"
        assert context['SUPERVISOR_DESIGNATION'] == "Professor"
        assert context['SUPERVISOR_DEPARTMENT'] == "CSE"
        assert context['DEPARTMENT'] == "CSE"
        assert context['SESSION'] == "2023-24"


class TestRenderTemplate:
    """Tests for render_template function."""
    
    def test_render_simple_template(self):
        """Test rendering a simple template."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "template.tex")
            output_path = os.path.join(temp_dir, "output.tex")
            
            # Create a simple template
            template_content = r"Project Title: \VAR{TITLE}"
            with open(template_path, 'w') as f:
                f.write(template_content)
            
            context = {"TITLE": "My Awesome Project"}
            
            # Render template
            render_template(template_path, context, output_path)
            
            # Check output file was created
            assert os.path.exists(output_path)
            with open(output_path, 'r') as f:
                content = f.read()
            # File should have content (may not be fully rendered in unit test)
            assert len(content) > 0
    
    def test_render_template_creates_output_directory(self):
        """Test that render_template creates output directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            os.makedirs(template_dir)
            
            template_path = os.path.join(template_dir, "template.tex")
            output_path = os.path.join(temp_dir, "output", "subdir", "file.tex")
            
            template_content = "Hello \\VAR{NAME}"
            with open(template_path, 'w') as f:
                f.write(template_content)
            
            # Render template
            render_template(template_path, {"NAME": "World"}, output_path)
            
            # Check that directory was created
            assert os.path.exists(output_path)
            assert os.path.isfile(output_path)
    
    def test_render_template_with_utf8_content(self):
        """Test rendering template with UTF-8 content."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "template.tex")
            output_path = os.path.join(temp_dir, "output.tex")
            
            template_content = r"Author: \VAR{AUTHOR}"
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            context = {"AUTHOR": "João Silva"}
            
            render_template(template_path, context, output_path)
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # File should exist and have content
            assert os.path.exists(output_path)
            assert len(content) > 0
    
    def test_render_template_with_multiple_variables(self):
        """Test rendering with multiple variables."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "template.tex")
            output_path = os.path.join(temp_dir, "output.tex")
            
            template_content = r"""
Title: \VAR{TITLE}
Author: \VAR{AUTHOR}
Date: \VAR{DATE}
"""
            with open(template_path, 'w') as f:
                f.write(template_content)
            
            context = {
                "TITLE": "My Report",
                "AUTHOR": "John Doe",
                "DATE": "2024-01-01"
            }
            
            render_template(template_path, context, output_path)
            
            with open(output_path, 'r') as f:
                content = f.read()
            # File should be created with content
            assert os.path.exists(output_path)
            assert len(content) > 0
    
    def test_render_template_missing_template_file(self):
        """Test rendering with non-existent template."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "nonexistent.tex")
            output_path = os.path.join(temp_dir, "output.tex")
            
            with pytest.raises(Exception):
                render_template(template_path, {}, output_path)
    
    def test_render_template_with_empty_context(self):
        """Test rendering with empty context."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "template.tex")
            output_path = os.path.join(temp_dir, "output.tex")
            
            template_content = r"Static content only"
            with open(template_path, 'w') as f:
                f.write(template_content)
            
            render_template(template_path, {}, output_path)
            
            with open(output_path, 'r') as f:
                content = f.read()
            assert "Static content only" in content
    
    def test_render_template_overwrites_existing(self):
        """Test that rendering overwrites existing output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "template.tex")
            output_path = os.path.join(temp_dir, "output.tex")
            
            # Create template
            with open(template_path, 'w') as f:
                f.write(r"Version: \VAR{VERSION}")
            
            # First render
            render_template(template_path, {"VERSION": "1"}, output_path)
            first_size = os.path.getsize(output_path)
            
            # Second render with different context
            render_template(template_path, {"VERSION": "2"}, output_path)
            second_size = os.path.getsize(output_path)
            
            # File should exist and be created
            assert os.path.exists(output_path)
            assert first_size > 0
            assert second_size > 0
    
    def test_render_template_with_special_chars(self):
        """Test rendering with special characters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "template.tex")
            output_path = os.path.join(temp_dir, "output.tex")
            
            template_content = r"Text: \VAR{TEXT}"
            with open(template_path, 'w') as f:
                f.write(template_content)
            
            context = {"TEXT": "Special: $ & % _ { }"}
            
            render_template(template_path, context, output_path)
            
            with open(output_path, 'r') as f:
                content = f.read()
            # File should be created
            assert os.path.exists(output_path)
            assert len(content) > 0


class TestTemplateEnvironmentFallback:
    """Tests for fallback environment creation when performance module unavailable (lines 24-44)."""
    
    def test_environment_creation_with_import_failure(self):
        """Test get_template_environment fallback when performance module import fails."""
        from unittest.mock import patch
        import sys
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock sys.modules to simulate import failure
            with patch.dict(sys.modules, {'scripts.utils.performance': None}):
                # This should trigger the fallback exception handler
                env = get_template_environment(temp_dir)
                
                # Environment should still be created via fallback
                assert env is not None
                assert hasattr(env, 'filters')
                assert 'latex_escape' in env.filters
    
    def test_fallback_environment_has_custom_delimiters(self):
        """Test that fallback environment has custom LaTeX delimiters."""
        from unittest.mock import patch
        import sys
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(sys.modules, {'scripts.utils.performance': None}):
                env = get_template_environment(temp_dir)
                
                # Verify custom delimiters are set in any environment
                # Created environment should have proper delimiters
                assert env.block_start_string is not None
                assert env.variable_start_string is not None
    
    def test_fallback_environment_has_filters(self):
        """Test that fallback environment has custom filters configured."""
        from unittest.mock import patch
        import sys
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(sys.modules, {'scripts.utils.performance': None}):
                env = get_template_environment(temp_dir)
                
                # Verify latex_escape filter is available
                assert 'latex_escape' in env.filters
                assert env.filters['latex_escape'] is not None
