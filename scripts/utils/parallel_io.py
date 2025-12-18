"""Parallel file operations for improved performance.

This module provides utilities for parallel file copying and processing.
"""

import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Callable, Optional
from pathlib import Path


def copy_file_with_progress(src: str, dst: str) -> Tuple[str, bool]:
    """Copy a single file and return status.
    
    Args:
        src: Source file path
        dst: Destination file path
    
    Returns:
        Tuple of (filename, success)
    """
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        return (os.path.basename(src), True)
    except Exception as e:
        return (os.path.basename(src), False)


def copy_files_parallel(file_pairs: List[Tuple[str, str]], 
                       max_workers: Optional[int] = None,
                       progress_callback: Optional[Callable] = None) -> int:
    """Copy multiple files in parallel.
    
    Args:
        file_pairs: List of (source, destination) tuples
        max_workers: Maximum number of worker threads (default: CPU count)
        progress_callback: Optional callback function called after each file
    
    Returns:
        Number of successfully copied files
    
    Example:
        files = [
            ('src/file1.txt', 'dst/file1.txt'),
            ('src/file2.txt', 'dst/file2.txt'),
        ]
        count = copy_files_parallel(files)
    """
    if not file_pairs:
        return 0
    
    success_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all copy tasks
        futures = {
            executor.submit(copy_file_with_progress, src, dst): (src, dst)
            for src, dst in file_pairs
        }
        
        # Process completed tasks
        for future in as_completed(futures):
            filename, success = future.result()
            if success:
                success_count += 1
            
            # Call progress callback if provided
            if progress_callback:
                progress_callback(filename, success)
    
    return success_count


def get_files_to_copy(src_dir: str, dst_dir: str, 
                     exclude_patterns: Optional[List[str]] = None) -> List[Tuple[str, str]]:
    """Get list of files to copy from source to destination.
    
    Args:
        src_dir: Source directory
        dst_dir: Destination directory
        exclude_patterns: Optional list of patterns to exclude
    
    Returns:
        List of (source, destination) file pairs
    """
    file_pairs = []
    exclude_patterns = exclude_patterns or []
    
    for root, dirs, files in os.walk(src_dir):
        # Calculate relative path
        rel_path = os.path.relpath(root, src_dir)
        
        for file in files:
            # Check exclusions
            if any(pattern in file for pattern in exclude_patterns):
                continue
            
            src_file = os.path.join(root, file)
            
            if rel_path == '.':
                dst_file = os.path.join(dst_dir, file)
            else:
                dst_file = os.path.join(dst_dir, rel_path, file)
            
            file_pairs.append((src_file, dst_file))
    
    return file_pairs


def copy_directory_parallel(src_dir: str, dst_dir: str,
                           exclude_patterns: Optional[List[str]] = None,
                           max_workers: Optional[int] = None,
                           progress_callback: Optional[Callable] = None) -> int:
    """Copy entire directory in parallel.
    
    Args:
        src_dir: Source directory
        dst_dir: Destination directory
        exclude_patterns: Optional list of patterns to exclude
        max_workers: Maximum number of worker threads
        progress_callback: Optional progress callback
    
    Returns:
        Number of successfully copied files
    
    Example:
        count = copy_directory_parallel(
            'templates/proposal',
            'output/my-project',
            exclude_patterns=['.git', '__pycache__']
        )
    """
    file_pairs = get_files_to_copy(src_dir, dst_dir, exclude_patterns)
    return copy_files_parallel(file_pairs, max_workers, progress_callback)
