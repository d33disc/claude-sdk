"""
Environment configuration loader for Claude SDK.
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
        # Try to find .env in the project root
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"
    
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
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                        
                    env_vars[key] = value
                    os.environ[key] = value
    
    return env_vars

if __name__ == "__main__":
    # If run directly, load the environment and print status
    env_file = sys.argv[1] if len(sys.argv) > 1 else None
    loaded_vars = load_env(env_file)
    
    if loaded_vars:
        print(f"Loaded {len(loaded_vars)} environment variables:")
        for key in loaded_vars:
            # Show first few characters of sensitive values
            value = loaded_vars[key]
            if "key" in key.lower() or "secret" in key.lower() or "token" in key.lower() or "password" in key.lower():
                if len(value) > 8:
                    value = f"{value[:4]}...{value[-4:]}"
                else:
                    value = "******"
            print(f"  - {key}: {value}")
    else:
        print("No environment variables loaded.")