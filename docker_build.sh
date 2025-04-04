#!/bin/bash

# docker_build.sh - A comprehensive script to build and run the Claude SDK Docker container
# Optimized for Docker Desktop
# Author: Claude

set -e  # Exit immediately if a command exits with a non-zero status

# Text formatting
BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
RED="\033[31m"
RESET="\033[0m"

# Container configuration
IMAGE_NAME="claude-sdk"
CONTAINER_NAME="claude-sdk-container"
API_PORT="8000"

# Function to print formatted messages
print_message() {
    local type=$1
    local message=$2
    
    case $type in
        "info")
            echo -e "${BLUE}${BOLD}[INFO]${RESET} $message"
            ;;
        "success")
            echo -e "${GREEN}${BOLD}[SUCCESS]${RESET} $message"
            ;;
        "warning")
            echo -e "${YELLOW}${BOLD}[WARNING]${RESET} $message"
            ;;
        "error")
            echo -e "${RED}${BOLD}[ERROR]${RESET} $message"
            ;;
        *)
            echo -e "$message"
            ;;
    esac
}

# Function to check if Docker is running
check_docker() {
    print_message "info" "Checking if Docker is running..."
    
    if ! docker info > /dev/null 2>&1; then
        print_message "error" "Docker is not running. Please start Docker Desktop and try again."
        exit 1
    fi
    
    print_message "success" "Docker is running."
}

# Function to check if the API key is set
check_api_key() {
    print_message "info" "Checking Anthropic API key..."
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        print_message "warning" "ANTHROPIC_API_KEY environment variable is not set."
        
        read -p "Do you want to enter your Anthropic API key now? (y/n): " response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            read -p "Enter your Anthropic API key: " api_key
            export ANTHROPIC_API_KEY="$api_key"
            print_message "success" "API key set for this session."
        else
            print_message "warning" "Continuing without API key. The container will need an API key to function correctly."
        fi
    else
        print_message "success" "Anthropic API key is set."
    fi
}

# Function to clean up existing containers
cleanup() {
    print_message "info" "Checking for existing containers..."
    
    # Check if the container is already running
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_message "warning" "Container '$CONTAINER_NAME' is already running."
        read -p "Do you want to stop and remove it? (y/n): " response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            print_message "info" "Stopping container '$CONTAINER_NAME'..."
            docker stop "$CONTAINER_NAME" > /dev/null
            print_message "info" "Removing container '$CONTAINER_NAME'..."
            docker rm "$CONTAINER_NAME" > /dev/null
            print_message "success" "Removed existing container."
        else
            print_message "error" "Cannot proceed with an existing container. Exiting."
            exit 1
        fi
    elif docker ps -a -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_message "info" "Removing stopped container '$CONTAINER_NAME'..."
        docker rm "$CONTAINER_NAME" > /dev/null
        print_message "success" "Removed stopped container."
    else
        print_message "success" "No existing containers found."
    fi
}

# Function to build the Docker image
build_image() {
    print_message "info" "Building Docker image '$IMAGE_NAME'..."
    
    # Create a temporary .dockerignore file if it doesn't exist
    if [ ! -f .dockerignore ]; then
        cat > .dockerignore << EOF
.git
.github
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.venv
.coverage
htmlcov/
.tox/
.nox/
.hypothesis/
.pytest_cache/
.coverage.*
coverage.xml
*.cover
tests/
EOF
        print_message "info" "Created temporary .dockerignore file."
    fi
    
    # Build the Docker image with proper error handling
    if docker build -t "$IMAGE_NAME" . ; then
        print_message "success" "Docker image built successfully."
    else
        print_message "error" "Failed to build Docker image. See error above."
        exit 1
    fi
}

# Function to run the Docker container
run_container() {
    print_message "info" "Starting container '$CONTAINER_NAME'..."
    
    # Add additional fast-api related requirements
    if ! grep -q "fastapi" requirements.txt && ! grep -q "uvicorn" requirements.txt; then
        print_message "warning" "FastAPI and uvicorn are required for the API server but not found in requirements.txt."
        print_message "info" "Adding temporary requirements file for the container..."
        cat > requirements-docker.txt << EOF
# Requirements for Docker container
-r requirements.txt
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0
EOF
    fi
    
    # Run the Docker container
    if docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$API_PORT:$API_PORT" \
        -e "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" \
        -v "$(pwd)/claude_sdk:/app/claude_sdk" \
        --restart unless-stopped \
        "$IMAGE_NAME"; then
        
        print_message "success" "Container started successfully."
    else
        print_message "error" "Failed to start container. See error above."
        exit 1
    fi
}

# Function to check container status
check_container() {
    print_message "info" "Checking container status..."
    
    # Wait a moment for the container to start
    sleep 2
    
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_message "success" "Container is running."
        
        # Log the container output
        print_message "info" "Container logs (first 10 lines):"
        docker logs "$CONTAINER_NAME" --tail 10
        
        # Show container details
        container_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$CONTAINER_NAME")
        print_message "info" "Container IP: $container_ip"
        print_message "info" "API available at: http://localhost:$API_PORT"
        print_message "info" "API docs available at: http://localhost:$API_PORT/docs"
    else
        print_message "error" "Container is not running. Check Docker logs for details."
        docker logs "$CONTAINER_NAME"
        exit 1
    fi
}

# Function to create simple test script
create_test_script() {
    print_message "info" "Creating test script..."
    
    cat > test_claude_api.sh << 'EOF'
#!/bin/bash

# Test script for Claude SDK API
API_URL="http://localhost:8000"

# Test the root endpoint
echo "Testing root endpoint..."
curl -s "$API_URL/" | jq .

# If API key is available, test the messages endpoint
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo -e "\nTesting messages endpoint..."
    curl -s -X POST \
        "$API_URL/messages" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "claude-3-sonnet-20240229",
            "messages": [{"role": "user", "content": "Hello, Claude. How are you today?"}],
            "max_tokens": 100
        }' | jq .
fi

echo -e "\nTest completed."
EOF
    
    chmod +x test_claude_api.sh
    print_message "success" "Test script created: test_claude_api.sh"
    print_message "info" "You can run this script to test the API once the container is running."
}

# Main execution
main() {
    print_message "info" "===== Claude SDK Docker Build Script ====="
    
    # Check prerequisites
    check_docker
    check_api_key
    
    # Clean up existing containers
    cleanup
    
    # Build and run
    build_image
    run_container
    check_container
    create_test_script
    
    print_message "success" "===== Container setup complete! ====="
    print_message "info" "To stop the container, run: docker stop $CONTAINER_NAME"
    print_message "info" "To start the container again, run: docker start $CONTAINER_NAME"
    print_message "info" "To view logs, run: docker logs $CONTAINER_NAME"
}

# Run the main function
main