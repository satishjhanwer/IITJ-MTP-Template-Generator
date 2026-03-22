"""Tests for parallel file operations."""

import os
import tempfile
from pathlib import Path
from scripts.utils.parallel_io import (
    copy_file_with_progress,
    copy_files_parallel,
    get_files_to_copy,
    copy_directory_parallel
)


class TestCopyFileWithProgress:
    """Tests for copy_file_with_progress function."""
    
    def test_successful_copy(self):
        """Test successful file copy."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_file = os.path.join(temp_dir, "source.txt")
            dst_file = os.path.join(temp_dir, "dest.txt")
            
            # Create source file
            with open(src_file, 'w') as f:
                f.write("test content")
            
            # Copy file
            filename, success = copy_file_with_progress(src_file, dst_file)
            
            assert success is True
            assert filename == "source.txt"
            assert os.path.exists(dst_file)
            assert Path(dst_file).read_text() == "test content"
    
    def test_copy_creates_directory(self):
        """Test that copy creates destination directory if missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_file = os.path.join(temp_dir, "source.txt")
            dst_dir = os.path.join(temp_dir, "subdir", "nested")
            dst_file = os.path.join(dst_dir, "dest.txt")
            
            # Create source file
            with open(src_file, 'w') as f:
                f.write("test content")
            
            # Copy file to nested directory
            filename, success = copy_file_with_progress(src_file, dst_file)
            
            assert success is True
            assert os.path.exists(dst_file)
    
    def test_copy_preserves_metadata(self):
        """Test that copy preserves file metadata."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_file = os.path.join(temp_dir, "source.txt")
            dst_file = os.path.join(temp_dir, "dest.txt")
            
            # Create source file
            with open(src_file, 'w') as f:
                f.write("test content")
            
            # Get source file stats
            src_stats = os.stat(src_file)
            
            # Copy file
            copy_file_with_progress(src_file, dst_file)
            
            # Get destination file stats
            dst_stats = os.stat(dst_file)
            
            # Check that modification times are preserved (within reasonable margin)
            assert abs(src_stats.st_mtime - dst_stats.st_mtime) < 1
    
    def test_copy_nonexistent_source(self):
        """Test copying from nonexistent source."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_file = os.path.join(temp_dir, "nonexistent.txt")
            dst_file = os.path.join(temp_dir, "dest.txt")
            
            filename, success = copy_file_with_progress(src_file, dst_file)
            
            assert success is False
            assert filename == "nonexistent.txt"
    
    def test_copy_binary_file(self):
        """Test copying binary file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_file = os.path.join(temp_dir, "image.bin")
            dst_file = os.path.join(temp_dir, "image_copy.bin")
            
            # Create binary file
            with open(src_file, 'wb') as f:
                f.write(b'\x00\x01\x02\x03\x04')
            
            # Copy file
            filename, success = copy_file_with_progress(src_file, dst_file)
            
            assert success is True
            with open(dst_file, 'rb') as f:
                assert f.read() == b'\x00\x01\x02\x03\x04'


class TestGetFilesToCopy:
    """Tests for get_files_to_copy function."""
    
    def test_simple_directory_structure(self):
        """Test getting files from simple directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            # Create directory structure
            os.makedirs(src_dir)
            Path(os.path.join(src_dir, "file1.txt")).write_text("content1")
            Path(os.path.join(src_dir, "file2.txt")).write_text("content2")
            
            files = get_files_to_copy(src_dir, dst_dir)
            
            assert len(files) == 2
            assert all(isinstance(pair, tuple) and len(pair) == 2 for pair in files)
    
    def test_nested_directory_structure(self):
        """Test getting files from nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            # Create nested directory structure
            os.makedirs(os.path.join(src_dir, "subdir"))
            Path(os.path.join(src_dir, "file1.txt")).write_text("content1")
            Path(os.path.join(src_dir, "subdir", "file2.txt")).write_text("content2")
            
            files = get_files_to_copy(src_dir, dst_dir)
            
            assert len(files) == 2
            # Check that nested files have correct destination
            dst_files = [dst for src, dst in files]
            assert any("subdir" in dst for dst in dst_files)
    
    def test_exclude_patterns(self):
        """Test excluding files by pattern."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            # Create files
            os.makedirs(src_dir)
            Path(os.path.join(src_dir, "file.txt")).write_text("content")
            Path(os.path.join(src_dir, "file.pyc")).write_text("compiled")
            Path(os.path.join(src_dir, "file.pyo")).write_text("compiled")
            
            files = get_files_to_copy(src_dir, dst_dir, exclude_patterns=[".pyc", ".pyo"])
            
            assert len(files) == 1
            assert "file.txt" in files[0][0]
    
    def test_empty_directory(self):
        """Test with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            os.makedirs(src_dir)
            
            files = get_files_to_copy(src_dir, dst_dir)
            
            assert files == []
    
    def test_multiple_exclude_patterns(self):
        """Test with multiple exclude patterns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            os.makedirs(src_dir)
            Path(os.path.join(src_dir, "file.txt")).write_text("content")
            Path(os.path.join(src_dir, "file.log")).write_text("log")
            Path(os.path.join(src_dir, "file.tmp")).write_text("temp")
            
            files = get_files_to_copy(
                src_dir, dst_dir, 
                exclude_patterns=[".log", ".tmp"]
            )
            
            assert len(files) == 1


class TestCopyFilesParallel:
    """Tests for copy_files_parallel function."""
    
    def test_copy_multiple_files(self):
        """Test copying multiple files in parallel."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            os.makedirs(src_dir)
            os.makedirs(dst_dir)
            
            # Create source files
            files = []
            for i in range(5):
                src_file = os.path.join(src_dir, f"file{i}.txt")
                dst_file = os.path.join(dst_dir, f"file{i}.txt")
                Path(src_file).write_text(f"content{i}")
                files.append((src_file, dst_file))
            
            # Copy files
            count = copy_files_parallel(files)
            
            assert count == 5
            for src, dst in files:
                assert os.path.exists(dst)
    
    def test_copy_empty_list(self):
        """Test with empty file list."""
        count = copy_files_parallel([])
        assert count == 0
    
    def test_copy_with_progress_callback(self):
        """Test with progress callback."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            os.makedirs(src_dir)
            os.makedirs(dst_dir)
            
            # Create source files
            files = []
            for i in range(3):
                src_file = os.path.join(src_dir, f"file{i}.txt")
                dst_file = os.path.join(dst_dir, f"file{i}.txt")
                Path(src_file).write_text(f"content{i}")
                files.append((src_file, dst_file))
            
            # Track callback calls
            callback_calls = []
            def progress_callback(filename, success):
                callback_calls.append((filename, success))
            
            # Copy files
            count = copy_files_parallel(files, progress_callback=progress_callback)
            
            assert count == 3
            assert len(callback_calls) == 3
    
    def test_copy_with_max_workers(self):
        """Test with specified max workers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            os.makedirs(src_dir)
            os.makedirs(dst_dir)
            
            # Create source files
            files = []
            for i in range(4):
                src_file = os.path.join(src_dir, f"file{i}.txt")
                dst_file = os.path.join(dst_dir, f"file{i}.txt")
                Path(src_file).write_text(f"content{i}")
                files.append((src_file, dst_file))
            
            # Copy with max_workers=2
            count = copy_files_parallel(files, max_workers=2)
            
            assert count == 4
    
    def test_copy_partial_failure(self):
        """Test when some files fail to copy."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            os.makedirs(src_dir)
            os.makedirs(dst_dir)
            
            # Create valid source files
            files = []
            for i in range(2):
                src_file = os.path.join(src_dir, f"file{i}.txt")
                dst_file = os.path.join(dst_dir, f"file{i}.txt")
                Path(src_file).write_text(f"content{i}")
                files.append((src_file, dst_file))
            
            # Add nonexistent files
            files.append(("/nonexistent/path/file3.txt", os.path.join(dst_dir, "file3.txt")))
            
            count = copy_files_parallel(files)
            
            # Only 2 files should succeed
            assert count == 2


class TestCopyDirectoryParallel:
    """Tests for copy_directory_parallel function."""
    
    def test_copy_simple_directory(self):
        """Test copying a simple directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            # Create source directory with files
            os.makedirs(src_dir)
            for i in range(3):
                Path(os.path.join(src_dir, f"file{i}.txt")).write_text(f"content{i}")
            
            # Copy directory
            count = copy_directory_parallel(src_dir, dst_dir)
            
            assert count == 3
            assert os.path.exists(dst_dir)
            for i in range(3):
                dst_file = os.path.join(dst_dir, f"file{i}.txt")
                assert os.path.exists(dst_file)
    
    def test_copy_nested_directory(self):
        """Test copying nested directory structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            # Create nested structure
            os.makedirs(os.path.join(src_dir, "subdir1", "subdir2"))
            Path(os.path.join(src_dir, "file1.txt")).write_text("content1")
            Path(os.path.join(src_dir, "subdir1", "file2.txt")).write_text("content2")
            Path(os.path.join(src_dir, "subdir1", "subdir2", "file3.txt")).write_text("content3")
            
            # Copy directory
            count = copy_directory_parallel(src_dir, dst_dir)
            
            assert count == 3
            assert os.path.exists(os.path.join(dst_dir, "subdir1", "subdir2", "file3.txt"))
    
    def test_copy_with_exclude_patterns(self):
        """Test copying with exclude patterns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            # Create files
            os.makedirs(src_dir)
            Path(os.path.join(src_dir, "file.txt")).write_text("content")
            Path(os.path.join(src_dir, "file.pyc")).write_text("compiled")
            Path(os.path.join(src_dir, "file.log")).write_text("log")
            
            # Copy with exclusions
            count = copy_directory_parallel(
                src_dir, dst_dir,
                exclude_patterns=[".pyc", ".log"]
            )
            
            assert count == 1
            assert os.path.exists(os.path.join(dst_dir, "file.txt"))
            assert not os.path.exists(os.path.join(dst_dir, "file.pyc"))
    
    def test_copy_with_progress_callback(self):
        """Test directory copy with progress callback."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            # Create files
            os.makedirs(src_dir)
            for i in range(3):
                Path(os.path.join(src_dir, f"file{i}.txt")).write_text(f"content{i}")
            
            # Track callbacks
            callbacks = []
            def progress_callback(filename, success):
                callbacks.append((filename, success))
            
            count = copy_directory_parallel(
                src_dir, dst_dir,
                progress_callback=progress_callback
            )
            
            assert count == 3
            assert len(callbacks) == 3
    
    def test_copy_empty_directory(self):
        """Test copying empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            src_dir = os.path.join(temp_dir, "src")
            dst_dir = os.path.join(temp_dir, "dst")
            
            os.makedirs(src_dir)
            
            count = copy_directory_parallel(src_dir, dst_dir)
            
            assert count == 0
