# Installation Guide

This guide covers various ways to install and use the Claude SDK.

## Prerequisites

- Python 3.7 or higher
- An Anthropic API key (sign up at [console.anthropic.com](https://console.anthropic.com))
- For Docker: Docker and Docker Compose

## Installation Methods

### 1. Install using pip

```bash
pip install claude-sdk
```

### 2. Install from source

```bash
git clone https://github.com/your-username/claude-sdk.git
cd claude-sdk
pip install -e .
```

### 3. Using Docker

#### Option A: Pull the pre-built image

```bash
docker pull ghcr.io/your-username/claude-sdk:latest
```

#### Option B: Build from source

```bash
git clone https://github.com/your-username/claude-sdk.git
cd claude-sdk
docker build -t claude-sdk .
```

#### Run with Docker

```bash
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your_api_key claude-sdk
```

### 4. Using Docker Compose

```bash
git clone https://github.com/your-username/claude-sdk.git
cd claude-sdk
export ANTHROPIC_API_KEY=your_api_key
docker-compose up
```

## Setting up your API key

### Environment Variable

Set the `ANTHROPIC_API_KEY` environment variable:

```bash
# Linux/macOS
export ANTHROPIC_API_KEY=your_api_key

# Windows (Command Prompt)
set ANTHROPIC_API_KEY=your_api_key

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your_api_key"
```

### In code

```python
from claude_sdk import Claude

client = Claude(api_key="your_api_key")
```

## Verifying Installation

Test your installation with:

```python
from claude_sdk import Claude

client = Claude()
response = client.generate(
    model="claude-3-7-sonnet-20250219",
    prompt="Hello, Claude!",
    max_tokens=100
)
print(response)
```
