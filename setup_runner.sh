#!/bin/bash

# Script to setup and run GitHub Actions Runner for claude-sdk

# Set variables
GITHUB_REPO="https://github.com/d33disc/claude-sdk"
GITHUB_TOKEN="BAHFVMKV4WLAHDK6HH2AXX3H5332G"
RUNNER_DIR="/Users/chrisdavis/actions-runner/actions-runner"

# Check if runner directory exists
if [ ! -d "$RUNNER_DIR" ]; then
    echo "Error: Runner directory not found at $RUNNER_DIR"
    exit 1
fi

# Navigate to runner directory
cd "$RUNNER_DIR"

# Configure the runner
echo "Configuring GitHub Actions runner..."
./config.sh --url "$GITHUB_REPO" --token "$GITHUB_TOKEN"

# Check if configuration was successful
if [ $? -eq 0 ]; then
    echo "Configuration successful! Starting runner..."
    # Run the runner
    ./run.sh
else
    echo "Configuration failed. Please check your repository URL and token."
    exit 1
fi