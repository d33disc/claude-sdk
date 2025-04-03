"""
Utility functions for the Claude SDK.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional


def load_env(env_file: Optional[str] = None) -> Dict[str, str]:
    """
    Load environment variables from a .env file.

    Args:
        env_file (str, optional): Path to the .env file. Defaults to None,
            which will look for a .env file in the project root.

    Returns:
        Dict[str, str]: Dictionary of loaded environment variables.
    """
    if env_file is None:
        # Try to find .env in the current directory
        env_file = ".env"

        # If not found, try to find in the project root
        if not os.path.exists(env_file):
            # Try to find the project root
            current_dir = Path.cwd()
            while current_dir != current_dir.parent:
                test_file = current_dir / ".env"
                if os.path.exists(test_file):
                    env_file = str(test_file)
                    break
                current_dir = current_dir.parent

    env_vars = {}

    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    # Remove quotes if present
                    if (value.startswith('"') and value.endswith('"')) or (
                        value.startswith("'") and value.endswith("'")
                    ):
                        value = value[1:-1]

                    env_vars[key] = value
                    os.environ[key] = value

    return env_vars


def get_version():
    """
    Get the current version of the package.

    Returns:
        str: Version string
    """
    from .version import __version__

    return __version__


def validate_api_key(api_key: Optional[str] = None) -> str:
    """
    Validate and retrieve API key.

    Args:
        api_key (str, optional): API key. If not provided, will try to read
            from ANTHROPIC_API_KEY environment variable.

    Returns:
        str: Valid API key

    Raises:
        ValueError: If API key is not provided and not in environment.
    """
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "API key must be provided either as an argument or through "
            "the ANTHROPIC_API_KEY environment variable."
        )

    # Basic validation
    if not api_key.startswith("sk-"):
        raise ValueError("Invalid API key format. API keys typically start with 'sk-'")

    return api_key
