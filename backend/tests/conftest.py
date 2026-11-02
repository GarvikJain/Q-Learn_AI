# conftest.py — pytest configuration for QLearnAI backend tests
import sys
import os

# Ensure the backend root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Pytest configuration
collect_ignore_glob = []
