"""
Basic example of using the Claude SDK.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the environment loader
from scripts.load_env import load_env
# Load environment variables from .env file
load_env()

from claude_sdk import Claude
import unittest
from unittest.mock import patch, MagicMock

# Check if this is being run in a test environment
if os.environ.get("TESTING", "false").lower() == "true":
    # Example with mock responses for testing
    with patch("requests.post") as mock_post:
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": [{"type": "text", "text": "Paris is the capital of France."}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Initialize the client
        client = Claude(api_key="test_api_key")
        
        # Generate a response
        response = client.generate(
            model="claude-3-7-sonnet-20250219",
            prompt="What is the capital of France?"
        )
        
        print("Response:", response)
        
        # Verify the call
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["json"]["model"] == "claude-3-7-sonnet-20250219"
        assert kwargs["json"]["messages"][0]["content"] == "What is the capital of France?"
        
        print("Basic test completed successfully!")
else:
    # Real usage example (requires API key)
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set the ANTHROPIC_API_KEY environment variable.")
        exit(1)
    
    # Initialize the client
    client = Claude(api_key=api_key)
    
    # Generate a response
    response = client.generate(
        model="claude-3-7-sonnet-20250219",
        prompt="What is the capital of France?"
    )
    
    print("Response:", response)

if __name__ == "__main__":
    # Run in test mode by default
    if "TESTING" not in os.environ:
        os.environ["TESTING"] = "true"