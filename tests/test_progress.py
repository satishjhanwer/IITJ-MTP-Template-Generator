"""Tests for progress tracking utilities."""

import pytest
import time
from io import StringIO
import sys
from scripts.utils.progress import (
    ProgressBar,
    Spinner,
    progress_context,
    spinner_context,
    with_progress
)


class TestProgressBar:
    """Tests for ProgressBar class."""
    
    def test_initialization(self):
        """Test ProgressBar initialization."""
        progress = ProgressBar(100, "Testing")
        assert progress.total == 100
        assert progress.current == 0
        assert progress.description == "Testing"
    
    def test_update(self):
        """Test updating progress."""
        progress = ProgressBar(10)
        progress.update(5)
        assert progress.current == 5
        progress.update(3)
        assert progress.current == 8
    
    def test_update_beyond_total(self):
        """Test that update doesn't exceed total."""
        progress = ProgressBar(10)
        progress.update(15)
        assert progress.current == 10
    
    def test_finish(self):
        """Test finishing progress."""
        progress = ProgressBar(10)
        progress.update(5)
        progress.finish()
        assert progress.current == 10


class TestSpinner:
    """Tests for Spinner class."""
    
    def test_initialization(self):
        """Test Spinner initialization."""
        spinner = Spinner("Loading")
        assert spinner.description == "Loading"
        assert spinner.running == False
    
    def test_start_stop(self):
        """Test starting and stopping spinner."""
        spinner = Spinner("Processing")
        spinner.start()
        assert spinner.running == True
        spinner.stop()
        assert spinner.running == False


class TestProgressContext:
    """Tests for progress_context context manager."""
    
    def test_context_manager(self):
        """Test progress_context as context manager."""
        with progress_context(10, "Testing") as progress:
            assert isinstance(progress, ProgressBar)
            assert progress.total == 10
            progress.update(5)
            assert progress.current == 5
        # Progress should be finished after context
        assert progress.current == 10
    
    def test_context_with_exception(self):
        """Test that progress finishes even with exception."""
        try:
            with progress_context(10, "Testing") as progress:
                progress.update(5)
                raise ValueError("Test error")
        except ValueError:
            pass
        # Progress should still be finished
        assert progress.current == 10


class TestSpinnerContext:
    """Tests for spinner_context context manager."""
    
    def test_context_manager(self):
        """Test spinner_context as context manager."""
        with spinner_context("Loading") as spinner:
            assert isinstance(spinner, Spinner)
            assert spinner.running == True
        # Spinner should be stopped after context
        assert spinner.running == False
    
    def test_context_with_exception(self):
        """Test that spinner stops even with exception."""
        try:
            with spinner_context("Processing") as spinner:
                assert spinner.running == True
                raise ValueError("Test error")
        except ValueError:
            pass
        # Spinner should still be stopped
        assert spinner.running == False


class TestWithProgressDecorator:
    """Tests for with_progress decorator."""
    
    def test_decorator(self):
        """Test with_progress decorator."""
        @with_progress("Processing")
        def test_function():
            return "result"
        
        result = test_function()
        assert result == "result"
    
    def test_decorator_with_args(self):
        """Test decorator with function arguments."""
        @with_progress("Calculating")
        def add(a, b):
            return a + b
        
        result = add(2, 3)
        assert result == 5
