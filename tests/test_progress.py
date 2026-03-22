"""Tests for progress tracking utilities."""

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
        assert progress.current == 10 # type: ignore


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
        assert spinner.running == False # type: ignore


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


class TestProgressBarEdgeCases:
    """Tests for edge cases in ProgressBar."""
    
    def test_progress_with_zero_total(self):
        """Test progress bar with zero total (line 37)."""
        progress = ProgressBar(0, "Empty")
        progress.update(1)
        # Should handle gracefully without error
        assert progress.current == 0
        progress.finish()
        assert progress.current == 0
    
    def test_progress_eta_calculation_at_start(self):
        """Test ETA calculation when current is 0 (line 49)."""
        progress = ProgressBar(100, "Processing")
        # No updates yet - current should be 0
        assert progress.current == 0
        progress.finish()
        # After finish, verify final display runs
        assert progress.current == 100
    
    def test_progress_eta_calculation_with_update(self):
        """Test ETA calculation when current > 0 (line 49)."""
        import time
        progress = ProgressBar(10, "Processing")
        # Update to non-zero
        progress.update(5)
        assert progress.current == 5
        # Small delay to ensure time has passed
        time.sleep(0.01)
        # Display will calculate ETA since current > 0
        progress._display()
        assert progress.current == 5
    
    def test_progress_display_called(self):
        """Test that display is called during update."""
        progress = ProgressBar(10, "Test")
        progress.update(5)
        assert progress.current == 5


class TestSpinnerEdgeCases:
    """Tests for edge cases in Spinner."""
    
    def test_spinner_display_when_not_running(self):
        """Test spinner display when not running (line 95)."""
        spinner = Spinner("Test")
        # Don't start the spinner
        assert spinner.running == False
        spinner._display()
        # Should not raise error
        assert spinner.running == False
    
    def test_spinner_stop_with_message(self):
        """Test spinner stop with final message (line 101)."""
        spinner = Spinner("Processing")
        spinner.start()
        assert spinner.running == True
        spinner.stop(final_message="Completed!")
        assert spinner.running == False
    
    def test_spinner_stop_without_message(self):
        """Test spinner stop without message."""
        spinner = Spinner("Processing")
        spinner.start()
        assert spinner.running == True
        spinner.stop()
        assert spinner.running == False
    
    def test_spinner_frame_cycling(self):
        """Test that spinner cycles through frames."""
        spinner = Spinner("Test")
        initial_frame = spinner.frame_index
        spinner.start()
        spinner._display()
        # Frame index should increment
        assert spinner.frame_index > initial_frame
