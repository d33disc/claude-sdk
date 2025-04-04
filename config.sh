#!/bin/bash

# GitHub Actions Runner Configuration Script
# Configures a self-hosted runner for GitHub Actions

# Set default values
RUNNER_NAME=$(hostname)
RUNNER_DIR="$HOME/actions-runner"
LABELS="claude-sdk,self-hosted"

# Process command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --url)
      REPO_URL="$2"
      shift 2
      ;;
    --token)
      TOKEN="$2"
      shift 2
      ;;
    --name)
      RUNNER_NAME="$2"
      shift 2
      ;;
    --labels)
      LABELS="$2"
      shift 2
      ;;
    --dir)
      RUNNER_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown parameter: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [ -z "$REPO_URL" ] || [ -z "$TOKEN" ]; then
  echo "Error: Repository URL and token are required"
  echo "Usage: $0 --url <repository_url> --token <token> [--name <runner_name>] [--labels <labels>] [--dir <runner_directory>]"
  exit 1
fi

# Create runner directory if it doesn't exist
mkdir -p "$RUNNER_DIR"
cd "$RUNNER_DIR" || exit 1

# Determine OS and architecture for downloading the correct runner package
OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"

if [ "$ARCH" == "x86_64" ]; then
  ARCH="x64"
elif [ "$ARCH" == "aarch64" ] || [ "$ARCH" == "arm64" ]; then
  ARCH="arm64"
else
  echo "Unsupported architecture: $ARCH"
  exit 1
fi

# Determine latest runner version
echo "Determining latest runner version..."
LATEST_VERSION=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | grep tag_name | cut -d '"' -f 4 | cut -c 2-)

if [ -z "$LATEST_VERSION" ]; then
  echo "Error: Could not determine latest runner version"
  exit 1
fi

echo "Latest runner version: $LATEST_VERSION"

# Download and extract the runner package
RUNNER_PACKAGE="actions-runner-${OS}-${ARCH}-${LATEST_VERSION}.tar.gz"
RUNNER_URL="https://github.com/actions/runner/releases/download/v${LATEST_VERSION}/${RUNNER_PACKAGE}"

echo "Downloading runner package from $RUNNER_URL"
curl -o "$RUNNER_PACKAGE" -L "$RUNNER_URL"

echo "Extracting runner package..."
tar xzf "$RUNNER_PACKAGE"
rm "$RUNNER_PACKAGE"

# Test connectivity to GitHub
echo "Testing connectivity to GitHub..."
bash ./scripts/runner-connectivity-script.sh

# Configure the runner
echo "Configuring runner with name: $RUNNER_NAME"
echo "Labels: $LABELS"
echo "Repository URL: $REPO_URL"

./config.sh --url "$REPO_URL" --token "$TOKEN" --name "$RUNNER_NAME" --labels "$LABELS" --unattended

# Create a .env file for runner configuration
cat > .env << EOF
# Runner Configuration
RUNNER_NAME=$RUNNER_NAME
REPO_URL=$REPO_URL
RUNNER_LABELS=$LABELS

# Add any proxy settings below if needed
# HTTP_PROXY=http://proxy.example.com:8080
# HTTPS_PROXY=http://proxy.example.com:8080
# NO_PROXY=localhost,127.0.0.1
EOF

echo "Runner configured successfully!"
echo "To start the runner, run: ./run.sh"