"""
Basic usage example for the Claude SDK.
"""

import os
from claude_sdk import Claude

# Initialize the client
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Claude(api_key=api_key)

# Generate a response
response = client.generate(
    model="claude-3-7-sonnet-20250219",
    prompt="What is the capital of France?",
    max_tokens=100,
    temperature=0.7,
)

print("Response:", response)

# Using the messages API
messages_response = client.messages_create(
    model="claude-3-7-sonnet-20250219",
    messages=[
        {"role": "user", "content": "What is the capital of Italy?"}
    ],
    max_tokens=100,
    temperature=0.7,
)

print("Messages API Response:", messages_response)
