"""Performance optimization utilities.

This module provides caching and optimization utilities for improved performance.
"""

import functools
import os
import time
from typing import Any, Callable, Dict, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape


# Global template environment cache
_template_env_cache: Dict[str, Environment] = {}


def get_cached_template_environment(template_dir: str) -> Environment:
    """Get or create a cached Jinja2 environment.
    
    Args:
        template_dir: Path to template directory
    
    Returns:
        Cached Jinja2 Environment instance
    """
    if template_dir not in _template_env_cache:
        _template_env_cache[template_dir] = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
    return _template_env_cache[template_dir]


def clear_template_cache():
    """Clear the template environment cache."""
    _template_env_cache.clear()


def memoize(func: Callable) -> Callable:
    """Memoization decorator for caching function results.
    
    Args:
        func: Function to memoize
    
    Returns:
        Wrapped function with caching
    
    Example:
        @memoize
        def expensive_function(arg):
            # Expensive computation
            return result
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key from arguments
        key = str(args) + str(sorted(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    return wrapper


def timed(func: Callable) -> Callable:
    """Decorator to measure function execution time.
    
    Args:
        func: Function to time
    
    Returns:
        Wrapped function that prints execution time
    
    Example:
        @timed
        def slow_function():
            # Implementation
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        elapsed = end_time - start_time
        print(f"⏱️  {func.__name__} took {elapsed:.3f}s")
        
        return result
    
    return wrapper


class PerformanceProfiler:
    """Simple performance profiler for tracking operation times."""
    
    def __init__(self):
        """Initialize profiler."""
        self.timings: Dict[str, float] = {}
        self.counts: Dict[str, int] = {}
    
    def start(self, operation: str):
        """Start timing an operation.
        
        Args:
            operation: Name of the operation
        """
        self.timings[f"{operation}_start"] = time.time()
    
    def end(self, operation: str):
        """End timing an operation.
        
        Args:
            operation: Name of the operation
        """
        start_key = f"{operation}_start"
        if start_key in self.timings:
            elapsed = time.time() - self.timings[start_key]
            
            # Accumulate time
            if operation not in self.timings:
                self.timings[operation] = 0
                self.counts[operation] = 0
            
            self.timings[operation] += elapsed
            self.counts[operation] += 1
            
            # Clean up start time
            del self.timings[start_key]
    
    def report(self):
        """Print performance report."""
        print("\n📊 Performance Report")
        print("=" * 60)
        
        # Sort by total time
        sorted_ops = sorted(
            [(op, time_val) for op, time_val in self.timings.items() 
             if not op.endswith('_start')],
            key=lambda x: x[1],
            reverse=True
        )
        
        for operation, total_time in sorted_ops:
            count = self.counts.get(operation, 1)
            avg_time = total_time / count
            print(f"{operation:30s} | Total: {total_time:6.3f}s | "
                  f"Count: {count:4d} | Avg: {avg_time:6.3f}s")
        
        print("=" * 60)
    
    def reset(self):
        """Reset profiler statistics."""
        self.timings.clear()
        self.counts.clear()


# Global profiler instance
_profiler = PerformanceProfiler()


def get_profiler() -> PerformanceProfiler:
    """Get the global profiler instance.
    
    Returns:
        Global PerformanceProfiler instance
    """
    return _profiler


def profile_operation(operation: str):
    """Decorator to profile an operation.
    
    Args:
        operation: Name of the operation to profile
    
    Example:
        @profile_operation("template_rendering")
        def render_template(template, context):
            # Implementation
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            profiler = get_profiler()
            profiler.start(operation)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                profiler.end(operation)
        return wrapper
    return decorator
