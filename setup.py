"""
Setup script for the Claude SDK.
"""

import os
from setuptools import setup, find_packages

# This setup.py file is maintained for backward compatibility.
# The project configuration is in pyproject.toml.

# Read the version from claude_sdk/version.py
with open(os.path.join("claude_sdk", "version.py"), encoding="utf-8") as f:
    exec(f.read())

setup(
    name="claude-sdk",
    version=__version__,
)
