"""
Setup script for the Claude SDK.
"""

import os
from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read the version from claude_sdk/version.py
with open(os.path.join("claude_sdk", "version.py"), encoding="utf-8") as f:
    exec(f.read())

setup(
    name="claude-sdk",
    version=__version__,
    description="A comprehensive Python SDK for Anthropic's Claude AI models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/claude-sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.8.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
)
