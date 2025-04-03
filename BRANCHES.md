# Branch Overview

This document provides an overview of all branches in the repository and their purpose.

## Main Branch

- **main** - The main branch containing the stable code

## Feature Branches

### GitHub Actions & CI/CD

- **add-basic-workflow** - Basic GitHub Actions workflow for CI/CD
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/add-basic-workflow

- **add-advanced-workflows** - Advanced GitHub Actions workflows with Dependabot integration
  - MERGED to main: PR #3

- **add-connectivity-test** - GitHub Actions connectivity test workflow
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/add-connectivity-test

- **update-ci-workflow** - Updated CI workflow for multi-platform testing and Docker builds
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/update-ci-workflow

- **update-ci-python** - Enhanced CI workflow for Python package building
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/update-ci-python

### Documentation & Tools

- **add-connectivity-tools** - Tools and documentation for GitHub connectivity
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/add-connectivity-tools

- **add-api-integration** - API integration workflows and token management guide
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/add-api-integration

### SDK Implementation

- **fix-tests** - Fixed test assertions to match implementation
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/fix-tests

- **add-env-config** - Environment configuration and example code
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/add-env-config

- **comprehensive-sdk-update** - Complete SDK overhaul with documentation
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/comprehensive-sdk-update

### Build & Packaging

- **fix-npm-lock** - Added package.json and lock file to fix CI errors
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/fix-npm-lock

- **add-python-packaging** - Python packaging configuration and requirements files
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/add-python-packaging

- **add-dockerfile** - Dockerfile for containerization
  - PR Link: https://github.com/d33disc/claude-sdk/pull/new/add-dockerfile

## Recommended Merge Order

For optimal integration, consider merging branches in this order:

1. **fix-tests** - Fix test assertions
2. **fix-npm-lock** - Add package.json and lock file
3. **add-python-packaging** - Add Python packaging configuration
4. **add-env-config** - Add environment configuration
5. **comprehensive-sdk-update** - Complete SDK overhaul
6. **add-basic-workflow** - Add basic GitHub Actions workflow
7. **update-ci-workflow** - Update CI workflow for multi-platform testing
8. **update-ci-python** - Update CI workflow for Python package building
9. **add-api-integration** - Add API integration workflows
10. **add-connectivity-tools** - Add connectivity tools and documentation
11. **add-connectivity-test** - Add GitHub Actions connectivity test
12. **add-dockerfile** - Add Dockerfile