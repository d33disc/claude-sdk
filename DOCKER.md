# Claude SDK Docker Guide

This guide provides detailed instructions for building and running the Claude SDK in Docker.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- An Anthropic API key (set as environment variable `ANTHROPIC_API_KEY`)

## Quick Start

The fastest way to get started is using our build script:

```bash
# Make the script executable
chmod +x docker_build.sh

# Run the build script
./docker_build.sh
```

This script will:
1. Check if Docker is running
2. Ask for your Anthropic API key if not set
3. Clean up any existing containers
4. Build the Docker image
5. Run the container
6. Create a test script to verify the API

## Manual Setup

If you prefer to build and run manually:

### 1. Build the Docker image

```bash
# Standard build
docker build -t claude-sdk .

# OR using the enhanced Dockerfile (recommended)
docker build -t claude-sdk -f Dockerfile.enhanced .
```

### 2. Run the container

```bash
docker run -d \
  --name claude-sdk-container \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_api_key_here \
  -v "$(pwd)/claude_sdk:/app/claude_sdk" \
  --restart unless-stopped \
  claude-sdk
```

### 3. Check container logs

```bash
docker logs claude-sdk-container
```

## Container Management

We provide a management script to help with common operations:

```bash
# Make the script executable
chmod +x docker_manage.sh

# View container status
./docker_manage.sh status

# View container logs
./docker_manage.sh logs

# Stop the container
./docker_manage.sh stop

# Start the container
./docker_manage.sh start

# Restart the container
./docker_manage.sh restart

# Open a shell in the container
./docker_manage.sh shell

# Remove the container
./docker_manage.sh remove
```

## Testing the API

Once the container is running, you can test the API using:

```bash
# Using the test script (if created by docker_build.sh)
./test_claude_api.sh

# Or using curl directly
curl http://localhost:8000/

# For the API documentation
# Open in your browser: http://localhost:8000/docs
```

## Troubleshooting

### Container won't start

Check the logs for errors:

```bash
docker logs claude-sdk-container
```

Common issues include:
- Missing API key
- Port 8000 already in use
- Missing dependencies

### API not responding

Verify the container is running:

```bash
docker ps | grep claude-sdk
```

Check container networking:

```bash
docker inspect claude-sdk-container | grep IPAddress
```

### Container keeps restarting

This usually indicates a configuration or dependency issue. Check logs:

```bash
docker logs claude-sdk-container
```

## Advanced Configuration

### Using a custom port

To use a port other than 8000:

```bash
docker run -d \
  --name claude-sdk-container \
  -p 9000:8000 \  # Map external port 9000 to internal port 8000
  -e ANTHROPIC_API_KEY=your_api_key_here \
  claude-sdk
```

### Persistent data

To persist data between container restarts:

```bash
docker run -d \
  --name claude-sdk-container \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_api_key_here \
  -v "$(pwd)/data:/app/data" \  # Mount a data directory
  claude-sdk
```

## Security Notes

- Never build Docker images with your API key hardcoded
- Use Docker secrets for production environments
- Consider network security when exposing the API
- The container runs the API server on all interfaces (0.0.0.0)