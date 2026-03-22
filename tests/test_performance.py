"""Tests for performance optimization utilities."""

import pytest
import time
from scripts.utils.performance import (
    get_cached_template_environment,
    clear_template_cache,
    memoize,
    timed,
    PerformanceProfiler,
    get_profiler,
    profile_operation
)


class TestGetCachedTemplateEnvironment:
    """Tests for get_cached_template_environment function."""
    
    def test_environment_creation(self):
        """Test that environment is created."""
        clear_template_cache()
        env = get_cached_template_environment("/tmp/templates")
        assert env is not None
        assert hasattr(env, 'filters')
    
    def test_environment_caching(self):
        """Test that environments are cached."""
        clear_template_cache()
        env1 = get_cached_template_environment("/tmp/templates")
        env2 = get_cached_template_environment("/tmp/templates")
        # Same object should be returned
        assert env1 is env2
    
    def test_different_dirs_different_environments(self):
        """Test that different directories get different environments."""
        clear_template_cache()
        env1 = get_cached_template_environment("/tmp/templates1")
        env2 = get_cached_template_environment("/tmp/templates2")
        # Different environments for different directories
        assert env1 is not env2
    
    def test_clear_template_cache(self):
        """Test clearing template cache."""
        env1 = get_cached_template_environment("/tmp/templates")
        clear_template_cache()
        env2 = get_cached_template_environment("/tmp/templates")
        # After clearing, should create new environment
        assert env1 is not env2


class TestMemoize:
    """Tests for memoize decorator."""
    
    def test_memoize_caches_results(self):
        """Test that memoize caches function results."""
        call_count = 0
        
        @memoize
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1
        
        # Second call with same argument (should use cache)
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Should not increment
    
    def test_memoize_different_arguments(self):
        """Test memoize with different arguments."""
        call_count = 0
        
        @memoize
        def function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        result1 = function(5)
        result2 = function(10)
        
        assert result1 == 10
        assert result2 == 20
        assert call_count == 2  # Both arguments should cause function calls
    
    def test_memoize_with_kwargs(self):
        """Test memoize with keyword arguments."""
        call_count = 0
        
        @memoize
        def function(x, y=2):
            nonlocal call_count
            call_count += 1
            return x * y
        
        result1 = function(5, y=3)
        assert result1 == 15
        assert call_count == 1
        
        # Same arguments should use cache
        result2 = function(5, y=3)
        assert result2 == 15
        assert call_count == 1
    
    def test_memoize_preserves_function_name(self):
        """Test that memoize preserves function name."""
        @memoize
        def my_function(x):
            return x * 2
        
        assert my_function.__name__ == "my_function"
    
    def test_memoize_with_multiple_arguments(self):
        """Test memoize with multiple arguments."""
        call_count = 0
        
        @memoize
        def add(a, b, c):
            nonlocal call_count
            call_count += 1
            return a + b + c
        
        result1 = add(1, 2, 3)
        result2 = add(1, 2, 3)  # Should use cache
        result3 = add(1, 2, 4)  # Different arguments
        
        assert result1 == 6
        assert result2 == 6
        assert result3 == 7
        assert call_count == 2


class TestTimed:
    """Tests for timed decorator."""
    
    def test_timed_decorator_works(self):
        """Test that timed decorator executes function."""
        @timed
        def slow_function():
            time.sleep(0.01)
            return "result"
        
        result = slow_function()
        assert result == "result"
    
    def test_timed_preserves_function_name(self):
        """Test that timed preserves function name."""
        @timed
        def my_function():
            return "result"
        
        assert my_function.__name__ == "my_function"
    
    def test_timed_with_arguments(self):
        """Test timed with function arguments."""
        @timed
        def add(a, b):
            return a + b
        
        result = add(5, 3)
        assert result == 8
    
    def test_timed_returns_correct_value(self):
        """Test that timed returns function result."""
        @timed
        def multiply(x, y):
            return x * y
        
        result = multiply(4, 5)
        assert result == 20


class TestPerformanceProfiler:
    """Tests for PerformanceProfiler class."""
    
    def test_profiler_initialization(self):
        """Test profiler initialization."""
        profiler = PerformanceProfiler()
        assert profiler.timings == {}
        assert profiler.counts == {}
    
    def test_profiler_start_end(self):
        """Test starting and ending operations."""
        profiler = PerformanceProfiler()
        
        profiler.start("operation1")
        time.sleep(0.01)
        profiler.end("operation1")
        
        assert "operation1" in profiler.timings
        assert profiler.counts["operation1"] == 1
        assert profiler.timings["operation1"] > 0.01
    
    def test_profiler_multiple_operations(self):
        """Test profiling multiple operations."""
        profiler = PerformanceProfiler()
        
        profiler.start("op1")
        time.sleep(0.01)
        profiler.end("op1")
        
        profiler.start("op2")
        time.sleep(0.01)
        profiler.end("op2")
        
        assert "op1" in profiler.timings
        assert "op2" in profiler.timings
        assert profiler.counts["op1"] == 1
        assert profiler.counts["op2"] == 1
    
    def test_profiler_accumulation(self):
        """Test that profiler accumulates times."""
        profiler = PerformanceProfiler()
        
        # First call
        profiler.start("operation")
        time.sleep(0.01)
        profiler.end("operation")
        first_time = profiler.timings["operation"]
        
        # Second call
        profiler.start("operation")
        time.sleep(0.01)
        profiler.end("operation")
        second_time = profiler.timings["operation"]
        
        # Should accumulate
        assert second_time > first_time
        assert profiler.counts["operation"] == 2
    
    def test_profiler_reset(self):
        """Test profiler reset."""
        profiler = PerformanceProfiler()
        
        profiler.start("operation")
        time.sleep(0.01)
        profiler.end("operation")
        
        assert "operation" in profiler.timings
        
        profiler.reset()
        
        assert profiler.timings == {}
        assert profiler.counts == {}
    
    def test_profiler_report(self, capsys):
        """Test profiler report output."""
        profiler = PerformanceProfiler()
        
        profiler.start("op1")
        time.sleep(0.001)
        profiler.end("op1")
        
        profiler.report()
        
        captured = capsys.readouterr()
        assert "Performance Report" in captured.out
        assert "op1" in captured.out
    
    def test_profiler_end_without_start(self):
        """Test ending operation that wasn't started."""
        profiler = PerformanceProfiler()
        
        # Should not raise error
        profiler.end("non_existent")
        
        # Operation should not be in timings
        assert "non_existent" not in profiler.timings


class TestGetProfiler:
    """Tests for get_profiler function."""
    
    def test_get_profiler_returns_instance(self):
        """Test that get_profiler returns a profiler instance."""
        profiler = get_profiler()
        assert isinstance(profiler, PerformanceProfiler)
    
    def test_get_profiler_returns_same_instance(self):
        """Test that get_profiler returns same instance."""
        profiler1 = get_profiler()
        profiler2 = get_profiler()
        assert profiler1 is profiler2


class TestProfileOperation:
    """Tests for profile_operation decorator."""
    
    def test_profile_operation_decorator(self):
        """Test profile_operation decorator."""
        @profile_operation("test_op")
        def my_operation():
            time.sleep(0.01)
            return "result"
        
        result = my_operation()
        assert result == "result"
    
    def test_profile_operation_records_time(self):
        """Test that profile_operation records timing."""
        # Reset profiler
        profiler = get_profiler()
        profiler.reset()
        
        @profile_operation("my_test_op")
        def operation():
            time.sleep(0.01)
            return "result"
        
        result = operation()
        
        profiler = get_profiler()
        assert "my_test_op" in profiler.timings
        assert profiler.timings["my_test_op"] > 0
    
    def test_profile_operation_with_exception(self):
        """Test profile_operation with exception."""
        profiler = get_profiler()
        profiler.reset()
        
        @profile_operation("failing_op")
        def failing_operation():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError):
            failing_operation()
        
        # Operation should still be recorded
        assert "failing_op" in profiler.timings
    
    def test_profile_operation_preserves_function_info(self):
        """Test that decorator preserves function name."""
        @profile_operation("test_op")
        def my_function(x, y):
            return x + y
        
        assert my_function.__name__ == "my_function"
        result = my_function(3, 4)
        assert result == 7
    
    def test_profile_operation_multiple_calls(self):
        """Test multiple calls to decorated function."""
        profiler = get_profiler()
        profiler.reset()
        
        @profile_operation("multi_call_op")
        def operation(n):
            return n * 2
        
        operation(5)
        operation(10)
        operation(15)
        
        assert profiler.counts["multi_call_op"] == 3
