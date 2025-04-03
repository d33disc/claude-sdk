#!/bin/bash

# This script sets up a GitHub repository for the Claude SDK

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install Git first."
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI is not installed. Please install it first."
    echo "Visit https://cli.github.com/ for installation instructions."
    exit 1
fi

# Check if logged in to GitHub
echo "Checking GitHub login status..."
if ! gh auth status &> /dev/null; then
    echo "Please log in to GitHub using 'gh auth login' first."
    exit 1
fi

# Get GitHub username
USERNAME=$(gh api user | jq -r ".login")
if [ -z "$USERNAME" ]; then
    echo "Could not get GitHub username. Please log in using 'gh auth login'."
    exit 1
fi

echo "Creating GitHub repository..."
REPO_NAME="claude-sdk"
REPO_DESC="A comprehensive Python SDK for Anthropic's Claude AI models"

# Create the repository
echo "Creating repository $USERNAME/$REPO_NAME..."
gh repo create "$REPO_NAME" --public --description "$REPO_DESC" --source=. --remote=origin

# Initialize Git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
fi

# Add files
echo "Adding files to repository..."
git add .

# Initial commit
echo "Creating initial commit..."
git commit -m "Initial commit for Claude SDK"

# Push to GitHub
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "Repository setup complete!"
echo "Your repository is now available at: https://github.com/$USERNAME/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Go to https://github.com/$USERNAME/$REPO_NAME/settings/secrets/actions"
echo "2. Add any required secrets for GitHub Actions"
echo "3. Begin using your new Claude SDK!"
