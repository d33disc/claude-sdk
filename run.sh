#!/bin/bash

# GitHub Actions Runner Execution Script
# Starts the GitHub Actions runner as a foreground process

RUNNER_DIR="$HOME/actions-runner"

# Check if runner directory exists
if [ ! -d "$RUNNER_DIR" ]; then
  echo "Error: Runner directory not found at $RUNNER_DIR"
  echo "Please run ./config.sh first to set up the runner"
  exit 1
fi

# Change to runner directory
cd "$RUNNER_DIR" || exit 1

# Load environment variables if .env exists
if [ -f .env ]; then
  echo "Loading configuration from .env file"
  set -a
  source .env
  set +a
fi

# Start the runner in foreground mode
echo "Starting GitHub Actions runner..."
echo "Press Ctrl+C to stop the runner"
echo "-----------------------------------"
./run.sh