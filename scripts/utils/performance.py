"""Performance optimization utilities.

This module provides caching and optimization utilities for improved performance.
"""

import functools
import time
from typing import Any, Callable, Dict

from jinja2 import Environment, FileSystemLoader

_template_env_cache: Dict[str, Environment] = {}


def get_cached_template_environment(template_dir: str) -> Environment:
    """Get or create a cached Jinja2 environment.

    Args:
        template_dir: Path to template directory

    Returns:
        Cached Jinja2 Environment instance
    """
    if template_dir not in _template_env_cache:
        _template_env_cache[template_dir] = Environment(  # nosec B701
            loader=FileSystemLoader(template_dir),
            block_start_string="\\BLOCK{",
            block_end_string="}",
            variable_start_string="\\VAR{",
            variable_end_string="}",
            comment_start_string="\\#{",
            comment_end_string="}",
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
    return _template_env_cache[template_dir]


def clear_template_cache() -> None:
    """Clear the template environment cache."""
    _template_env_cache.clear()


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
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
    cache: Dict[str, Any] = {}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


def timed(func: Callable[..., Any]) -> Callable[..., Any]:
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
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[TIMER] {func.__name__} took {end_time - start_time:.3f}s")
        return result

    return wrapper


class PerformanceProfiler:
    """Simple performance profiler for tracking operation times."""

    def __init__(self) -> None:
        """Initialize profiler."""
        self.timings: Dict[str, float] = {}
        self.counts: Dict[str, int] = {}

    def start(self, operation: str) -> None:
        """Start timing an operation.

        Args:
            operation: Name of the operation
        """
        self.timings[f"{operation}_start"] = time.time()

    def end(self, operation: str) -> None:
        """End timing an operation.

        Args:
            operation: Name of the operation
        """
        start_key = f"{operation}_start"
        if start_key in self.timings:
            elapsed = time.time() - self.timings[start_key]

            if operation not in self.timings:
                self.timings[operation] = 0
                self.counts[operation] = 0

            self.timings[operation] += elapsed
            self.counts[operation] += 1
            del self.timings[start_key]

    def report(self) -> None:
        """Print performance report."""
        print("\nPerformance Report")
        print("=" * 60)

        sorted_ops = sorted(
            [
                (op, time_val)
                for op, time_val in self.timings.items()
                if not op.endswith("_start")
            ],
            key=lambda x: x[1],
            reverse=True,
        )

        for operation, total_time in sorted_ops:
            count = self.counts.get(operation, 1)
            avg_time = total_time / count
            print(
                f"{operation:30s} | Total: {total_time:6.3f}s | "
                f"Count: {count:4d} | Avg: {avg_time:6.3f}s"
            )

        print("=" * 60)

    def reset(self) -> None:
        """Reset profiler statistics."""
        self.timings.clear()
        self.counts.clear()


_profiler = PerformanceProfiler()


def get_profiler() -> PerformanceProfiler:
    """Get the global profiler instance.

    Returns:
        Global PerformanceProfiler instance
    """
    return _profiler


def profile_operation(
    operation: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to profile an operation.

    Args:
        operation: Name of the operation to profile

    Example:
        @profile_operation("template_rendering")
        def render_template(template, context):
            # Implementation
            pass
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            profiler = get_profiler()
            profiler.start(operation)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                profiler.end(operation)

        return wrapper

    return decorator
