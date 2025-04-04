#!/bin/bash

# docker_manage.sh - Helper script for managing the Claude SDK Docker container
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
CONTAINER_NAME="claude-sdk-container"
IMAGE_NAME="claude-sdk"

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
    if ! docker info > /dev/null 2>&1; then
        print_message "error" "Docker is not running. Please start Docker Desktop and try again."
        exit 1
    fi
}

# Function to display container status
show_status() {
    check_docker
    
    print_message "info" "Checking container status..."
    
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_message "success" "Container is running"
        
        # Get container details
        container_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$CONTAINER_NAME")
        container_ports=$(docker port "$CONTAINER_NAME")
        
        echo "Container ID: $(docker ps -q -f name="$CONTAINER_NAME")"
        echo "Container IP: $container_ip"
        echo "Exposed ports: $container_ports"
        echo "API URL: http://localhost:8000"
        echo "API docs: http://localhost:8000/docs"
        
        # Get container resource usage
        echo -e "\nResource usage:"
        docker stats "$CONTAINER_NAME" --no-stream --format "CPU: {{.CPUPerc}}  MEM: {{.MemUsage}}"
    elif docker ps -a -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_message "warning" "Container exists but is not running"
        echo "Container ID: $(docker ps -a -q -f name="$CONTAINER_NAME")"
        echo "Status: $(docker inspect -f '{{.State.Status}}' "$CONTAINER_NAME")"
        echo "Exit code: $(docker inspect -f '{{.State.ExitCode}}' "$CONTAINER_NAME")"
        
        # Show the last few lines of logs
        echo -e "\nLast 10 lines of logs:"
        docker logs "$CONTAINER_NAME" --tail 10
    else
        print_message "warning" "Container does not exist"
    fi
}

# Function to start the container
start_container() {
    check_docker
    
    if docker ps -a -q -f name="$CONTAINER_NAME" | grep -q .; then
        if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
            print_message "warning" "Container is already running"
        else
            print_message "info" "Starting existing container..."
            docker start "$CONTAINER_NAME"
            print_message "success" "Container started"
        fi
    else
        print_message "error" "Container does not exist. Please run './docker_build.sh' first"
        exit 1
    fi
}

# Function to stop the container
stop_container() {
    check_docker
    
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_message "info" "Stopping container..."
        docker stop "$CONTAINER_NAME"
        print_message "success" "Container stopped"
    else
        print_message "warning" "Container is not running"
    fi
}

# Function to view container logs
view_logs() {
    check_docker
    
    if docker ps -a -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_message "info" "Showing container logs (press Ctrl+C to exit)..."
        docker logs -f "$CONTAINER_NAME"
    else
        print_message "error" "Container does not exist"
        exit 1
    fi
}

# Function to restart the container
restart_container() {
    check_docker
    
    if docker ps -a -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_message "info" "Restarting container..."
        docker restart "$CONTAINER_NAME"
        print_message "success" "Container restarted"
    else
        print_message "error" "Container does not exist. Please run './docker_build.sh' first"
        exit 1
    fi
}

# Function to remove the container
remove_container() {
    check_docker
    
    if docker ps -a -q -f name="$CONTAINER_NAME" | grep -q .; then
        if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
            print_message "info" "Stopping running container..."
            docker stop "$CONTAINER_NAME"
        fi
        
        print_message "info" "Removing container..."
        docker rm "$CONTAINER_NAME"
        print_message "success" "Container removed"
    else
        print_message "warning" "Container does not exist"
    fi
}

# Function to run a shell inside the container
shell() {
    check_docker
    
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_message "info" "Opening shell in container (type 'exit' to return)..."
        docker exec -it "$CONTAINER_NAME" /bin/bash || docker exec -it "$CONTAINER_NAME" /bin/sh
    else
        print_message "error" "Container is not running"
        exit 1
    fi
}

# Function to display help
show_help() {
    echo -e "${BOLD}Claude SDK Docker Management Script${RESET}"
    echo
    echo "Usage: $0 [command]"
    echo
    echo "Commands:"
    echo "  status    Show container status and information"
    echo "  start     Start the container"
    echo "  stop      Stop the container"
    echo "  restart   Restart the container"
    echo "  logs      View container logs (follow mode)"
    echo "  remove    Remove the container"
    echo "  shell     Open a shell inside the container"
    echo "  help      Show this help message"
    echo
    echo "Example: $0 status"
}

# Main execution
case "$1" in
    "status")
        show_status
        ;;
    "start")
        start_container
        ;;
    "stop")
        stop_container
        ;;
    "restart")
        restart_container
        ;;
    "logs")
        view_logs
        ;;
    "remove")
        remove_container
        ;;
    "shell")
        shell
        ;;
    "help"|"")
        show_help
        ;;
    *)
        print_message "error" "Unknown command: $1"
        show_help
        exit 1
        ;;
esac