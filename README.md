# Claude Python SDK

A comprehensive Python SDK for interacting with Anthropic's Claude AI models, including Claude 3 Opus, Sonnet, Haiku, and Claude 3.5/3.7.

[![CI/CD](https://github.com/d33disc/claude-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/d33disc/claude-sdk/actions/workflows/ci.yml)

## Features

- Support for all Claude models (Claude 3 Opus, Sonnet, Haiku, Claude 3.5, Claude 3.7 Sonnet)
- Streaming responses
- Function calling and tool use
- Asynchronous API support
- Docker containerization for easy deployment
- Environment variable management
- Comprehensive test suite

## Installation

### Prerequisites

- Python 3.7+
- An API key from Anthropic

### Using pip

```bash
pip install claude-sdk
```

### Using Docker

```bash
docker pull ghcr.io/d33disc/claude-sdk:latest
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your_api_key ghcr.io/d33disc/claude-sdk:latest
```

### From Source

```bash
git clone https://github.com/d33disc/claude-sdk.git
cd claude-sdk
pip install -e .
```

## Quick Start

### Basic Usage

```python
from claude_sdk import Claude

# Initialize the client with an API key
client = Claude(api_key="your_api_key")

# Or initialize using environment variables (recommended)
# export ANTHROPIC_API_KEY=your_api_key
client = Claude()

# Generate a response
response = client.generate(
    model="claude-3-7-sonnet-20250219",
    prompt="What is the capital of France?",
    max_tokens=1000,
    temperature=0.7
)

print(response)
```

### Advanced Usage with System Prompt

```python
response = client.generate(
    model="claude-3-7-sonnet-20250219",
    prompt="Explain the concept of reinforcement learning.",
    system_prompt="You are an AI tutor specialized in explaining complex concepts simply.",
    max_tokens=2000,
    temperature=0.5
)
```

### Using the Messages API

```python
response = client.messages_create(
    model="claude-3-7-sonnet-20250219",
    messages=[
        {"role": "user", "content": "How do I implement a binary search tree in Python?"},
        {"role": "assistant", "content": "I'd be happy to help you implement a binary search tree. Let's start with the basic structure."},
        {"role": "user", "content": "Could you add method for tree traversal?"}
    ],
    max_tokens=1500,
    temperature=0.7
)
```

### Streaming Responses

```python
for chunk in client.generate(
    model="claude-3-7-sonnet-20250219",
    prompt="Write a poem about artificial intelligence.",
    max_tokens=500,
    temperature=0.8,
    stream=True
):
    print(chunk, end="", flush=True)
```

### Async API

```python
import asyncio
from claude_sdk import AsyncClaude

async def main():
    client = AsyncClaude(api_key="your_api_key")
    
    response = await client.generate(
        model="claude-3-7-sonnet-20250219",
        prompt="What are the benefits of quantum computing?",
        max_tokens=1000
    )
    
    print(response)

asyncio.run(main())
```

### Tool Use / Function Calling

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The unit of temperature"
                }
            },
            "required": ["location"]
        }
    }
]

response = client.generate(
    model="claude-3-7-sonnet-20250219",
    prompt="What's the weather like in New York?",
    tools=tools,
    max_tokens=1000
)
```

## Environment Configuration

We recommend using environment variables for configuration, especially for sensitive information like API keys. Create a `.env` file in your project root:

```
# .env file
ANTHROPIC_API_KEY=your_api_key
BASE_URL=https://api.anthropic.com  # Optional, defaults to this value
LOG_LEVEL=INFO
```

Then use our environment loader:

```python
from claude_sdk.utils import load_env
load_env()  # Loads variables from .env file

from claude_sdk import Claude
client = Claude()  # Will use ANTHROPIC_API_KEY from environment
```

## Available Models

- `claude-3-7-sonnet-20250219` - Latest flagship model
- `claude-3-5-sonnet-20240620` - High capability model
- `claude-3-opus-20240229` - Most capable model
- `claude-3-sonnet-20240229` - Balanced capability and speed
- `claude-3-haiku-20240307` - Fastest and most affordable

## Error Handling

```python
from claude_sdk import Claude
from claude_sdk.exceptions import ClaudeAPIError, RateLimitError

client = Claude()

try:
    response = client.generate(
        model="claude-3-7-sonnet-20250219",
        prompt="What is the meaning of life?",
        max_tokens=1000
    )
except RateLimitError:
    print("Rate limit exceeded. Please try again later.")
except ClaudeAPIError as e:
    print(f"API error: {e}")
```

## Command Line Interface

The SDK also includes a CLI for quick testing and usage:

```bash
# Install with CLI support
pip install "claude-sdk[cli]"

# Use the CLI
claude-cli generate "What is the capital of France?" --model claude-3-7-sonnet-20250219

# Stream responses
claude-cli generate "Write a short story about time travel." --stream
```

## Docker Deployment

For containerized usage, we provide a ready-to-use Docker image with the SDK pre-installed:

```bash
# Pull the image
docker pull ghcr.io/d33disc/claude-sdk:latest

# Run the container with your API key
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your_api_key ghcr.io/d33disc/claude-sdk:latest

# Run with local configuration
docker run -p 8000:8000 -v $(pwd)/.env:/app/.env ghcr.io/d33disc/claude-sdk:latest
```

The API server will be available at `http://localhost:8000/api/v1/`.

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/d33disc/claude-sdk.git
cd claude-sdk

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Using the Self-hosted GitHub Actions Runner

For contributors who want to use our self-hosted runner:

1. Configure your workflow to use `runs-on: self-hosted`
2. Push your changes to a branch
3. Create a pull request
4. The tests will automatically run on our self-hosted runner

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code passes all tests and adheres to our coding standards.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Anthropic](https://www.anthropic.com/) for creating Claude
- All contributors who have helped improve this SDK