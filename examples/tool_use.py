"""
Example demonstrating tool use with the Claude SDK.
"""

import os
import json
from claude_sdk import Claude

# Initialize the client
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Claude(api_key=api_key)

# Define a tool
tools = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g., San Francisco, CA",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The unit of temperature to use",
                },
            },
            "required": ["location"],
        },
    }
]

# Generate a response using the tool
response = client.messages_create(
    model="claude-3-haiku-20240307",
    messages=[
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ],
    tools=tools,
    max_tokens=1000,
    temperature=0.7,
)

print("Tool use response:", json.dumps(response, indent=2))

# Handle tool use response
if hasattr(response, "content") and isinstance(response.content, list):
    for content_block in response.content:
        if content_block.get("type") == "tool_use":
            tool_name = content_block.get("name")
            tool_input = content_block.get("input")
            
            print(f"Tool called: {tool_name}")
            print(f"Tool input: {json.dumps(tool_input, indent=2)}")
            
            # Here you would implement actual tool functionality
            # For this example, we'll just return some dummy data
            weather_data = {
                "temperature": 72,
                "unit": tool_input.get("unit", "fahrenheit"),
                "condition": "sunny",
                "location": tool_input.get("location"),
            }
            
            # Send the tool result back to Claude
            tool_response = client.messages_create(
                model="claude-3-haiku-20240307",
                messages=[
                    {"role": "user", "content": "What's the weather like in San Francisco?"},
                    {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "tool_use",
                                "name": tool_name,
                                "input": tool_input,
                                "id": content_block.get("id"),
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": content_block.get("id"),
                                "result": json.dumps(weather_data),
                            }
                        ],
                    },
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            
            print("Final response:", json.dumps(tool_response, indent=2))
