"""
Tests for the Claude SDK client.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import json

from claude_sdk import Claude

class TestClaude(unittest.TestCase):
    """
    Tests for the Claude client.
    """
    
    def setUp(self):
        """
        Set up the test environment.
        """
        # Set a dummy API key for testing
        os.environ["ANTHROPIC_API_KEY"] = "test_api_key"
        
        # Create a client
        self.client = Claude()
    
    @patch("requests.post")
    def test_generate(self, mock_post):
        """
        Test the generate method.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"content": "This is a test response."}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.client.generate(
            model="claude-3-7-sonnet-20250219",
            prompt="This is a test prompt.",
            max_tokens=100,
            temperature=0.7,
        )
        
        # Check the response
        self.assertEqual(response, {"content": "This is a test response."})
        
        # Check the call
        mock_post.assert_called_once()
        
        # Check the payload
        args, kwargs = mock_post.call_args
        payload = kwargs["json"]
        
        self.assertEqual(payload["model"], "claude-3-7-sonnet-20250219")
        self.assertEqual(payload["max_tokens"], 100)
        self.assertEqual(payload["temperature"], 0.7)
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(payload["messages"][0]["content"], "This is a test prompt.")
    
    @patch("requests.post")
    def test_messages_create(self, mock_post):
        """
        Test the messages_create method.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"content": "This is a test response."}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.client.messages_create(
            model="claude-3-7-sonnet-20250219",
            messages=[
                {"role": "user", "content": "This is a test message."}
            ],
            max_tokens=100,
            temperature=0.7,
        )
        
        # Check the response
        self.assertEqual(response, {"content": "This is a test response."})
        
        # Check the call
        mock_post.assert_called_once()
        
        # Check the payload
        args, kwargs = mock_post.call_args
        payload = kwargs["json"]
        
        self.assertEqual(payload["model"], "claude-3-7-sonnet-20250219")
        self.assertEqual(payload["max_tokens"], 100)
        self.assertEqual(payload["temperature"], 0.7)
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(payload["messages"][0]["content"], "This is a test message.")

if __name__ == "__main__":
    unittest.main()
