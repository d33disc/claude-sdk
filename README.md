# Claude Python SDK

A comprehensive Python SDK for interacting with Anthropic's Claude AI models, including Claude Compute and Desktop features.

## Features

- Support for all Claude models (Claude 3 Opus, Sonnet, Haiku, Claude 3.5, Claude 3.7 Sonnet)
- Streaming responses
- Function calling and tool use
- Asynchronous API support
- Docker containerization for easy deployment
- Support for Claude Compute features

## Installation

### Using pip

```bash
pip install claude-sdk
```

### Using Docker

```bash
docker pull claude-sdk/claude-sdk
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your_api_key claude-sdk/claude-sdk
```

## Quick Start

```python
from claude_sdk import Claude

# Initialize the client
client = Claude(api_key="your_api_key")

# Generate a response
response = client.generate(
    model="claude-3-7-sonnet-20250219",
    prompt="What is the capital of France?"
)

print(response)
```

## Documentation

For detailed documentation, please visit [https://claude-sdk.readthedocs.io](https://claude-sdk.readthedocs.io)

## License

MIT
