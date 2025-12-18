"""Progress tracking and display utilities.

This module provides progress indicators for long-running operations.
"""

import sys
import time
from typing import Optional, Callable
from contextlib import contextmanager


class ProgressBar:
    """Simple progress bar for terminal output."""
    
    def __init__(self, total: int, description: str = "", width: int = 40):
        """Initialize progress bar.
        
        Args:
            total: Total number of steps
            description: Description of the operation
            width: Width of the progress bar in characters
        """
        self.total = total
        self.current = 0
        self.description = description
        self.width = width
        self.start_time = time.time()
    
    def update(self, step: int = 1):
        """Update progress by specified steps."""
        self.current = min(self.current + step, self.total)
        self._display()
    
    def _display(self):
        """Display the progress bar."""
        if self.total == 0:
            return
        
        percent = self.current / self.total
        filled = int(self.width * percent)
        bar = '█' * filled + '░' * (self.width - filled)
        
        # Calculate elapsed time and ETA
        elapsed = time.time() - self.start_time
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = f"ETA: {int(eta)}s"
        else:
            eta_str = "ETA: --"
        
        # Format output
        output = f"\r{self.description} [{bar}] {int(percent * 100)}% ({self.current}/{self.total}) {eta_str}"
        sys.stdout.write(output)
        sys.stdout.flush()
        
        if self.current >= self.total:
            sys.stdout.write("\n")
            sys.stdout.flush()
    
    def finish(self):
        """Mark progress as complete."""
        self.current = self.total
        self._display()


class Spinner:
    """Simple spinner for indeterminate operations."""
    
    FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    def __init__(self, description: str = ""):
        """Initialize spinner.
        
        Args:
            description: Description of the operation
        """
        self.description = description
        self.frame_index = 0
        self.running = False
    
    def start(self):
        """Start the spinner."""
        self.running = True
        self._display()
    
    def stop(self, final_message: Optional[str] = None):
        """Stop the spinner.
        
        Args:
            final_message: Optional message to display when stopping
        """
        self.running = False
        sys.stdout.write('\r' + ' ' * 80 + '\r')  # Clear line
        if final_message:
            print(final_message)
        sys.stdout.flush()
    
    def _display(self):
        """Display the spinner frame."""
        if not self.running:
            return
        
        frame = self.FRAMES[self.frame_index % len(self.FRAMES)]
        output = f"\r{frame} {self.description}"
        sys.stdout.write(output)
        sys.stdout.flush()
        self.frame_index += 1


@contextmanager
def progress_context(total: int, description: str = "Processing"):
    """Context manager for progress tracking.
    
    Args:
        total: Total number of steps
        description: Description of the operation
    
    Yields:
        ProgressBar instance
    
    Example:
        with progress_context(100, "Copying files") as progress:
            for i in range(100):
                # Do work
                progress.update()
    """
    progress = ProgressBar(total, description)
    try:
        yield progress
    finally:
        progress.finish()


@contextmanager
def spinner_context(description: str = "Processing"):
    """Context manager for spinner.
    
    Args:
        description: Description of the operation
    
    Yields:
        Spinner instance
    
    Example:
        with spinner_context("Loading configuration") as spinner:
            # Do work
            pass
    """
    spinner = Spinner(description)
    spinner.start()
    try:
        yield spinner
    finally:
        spinner.stop()


def with_progress(description: str = "Processing"):
    """Decorator for functions that should show progress.
    
    Args:
        description: Description of the operation
    
    Example:
        @with_progress("Generating report")
        def generate_report(config):
            # Function implementation
            pass
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            with spinner_context(description):
                result = func(*args, **kwargs)
            print(f"✅ {description} complete")
            return result
        return wrapper
    return decorator
