#!/usr/bin/env python3
"""
Utility script to clean up old Django Silk profiling files.
This script can be run manually or scheduled to run periodically.

Usage:
    python utils/clean_profiles.py [days_to_keep] [path_to_profiles]

Example:
    python utils/clean_profiles.py 7 media
    This will keep the last 7 days of profiling files in the media directory.
"""

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

def clean_profiling_files(days_to_keep=7, path='media'):
    """
    Clean up profiling files older than the specified number of days.
    
    Args:
        days_to_keep: Number of days to keep profiling files. Default is 7.
        path: Path to the directory containing profiling files. Default is 'media'.
    """
    now = time.time()
    cutoff = now - (days_to_keep * 86400)  # 86400 seconds = 1 day
    count = 0
    size = 0
    
    print(f"Cleaning up profiling files older than {days_to_keep} days in {path}...")
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.prof'):
                file_path = os.path.join(root, file)
                file_mod_time = os.path.getmtime(file_path)
                if file_mod_time < cutoff:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    count += 1
                    size += file_size
    
    print(f"Removed {count} profiling files (total {size/1024/1024:.2f} MB).")
    return count, size

if __name__ == "__main__":
    # Get command line arguments
    days = 7
    path = 'media'
    
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number of days: {sys.argv[1]}. Using default: 7 days.")
    
    if len(sys.argv) > 2:
        path = sys.argv[2]
        if not os.path.exists(path):
            print(f"Path does not exist: {path}. Using default: media")
            path = 'media'
    
    # Clean up profiling files
    count, size = clean_profiling_files(days, path)
    
    if count == 0:
        print("No profiling files needed to be removed.")