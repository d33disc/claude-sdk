# API Token Management Guide for Self-Hosted Runners

This guide provides instructions for setting up and managing API tokens securely with GitHub Actions on self-hosted runners.

## Required API Tokens

The following API tokens should be configured as GitHub Secrets for our workflows:

| Secret Name | Purpose | Scope | Service |
|-------------|---------|-------|---------|
| `API_TOKEN` | GitHub API access | repo | GitHub |
| `NPM_TOKEN` | NPM package publishing | publish | npm Registry |
| `DOCS_API_TOKEN` | Documentation updates | write | Documentation Platform |
| `CICD_API_TOKEN` | External CI/CD triggers | trigger_build | CI/CD Platform |
| `MONITORING_API_TOKEN` | Metrics reporting | write | Monitoring Service |
| `SECURITY_API_TOKEN` | Security scanning | scan | Security Platform |

## Setting Up Tokens

### GitHub Personal Access Token (PAT)

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token" → "Fine-grained token"
3. Name: "Claude SDK CI/CD"
4. Set expiration to 90 days
5. Select repository access: "Only select repositories" → Choose relevant repos
6. Permissions required:
   - Repository permissions:
     - Actions: Read and write
     - Contents: Read and write
     - Issues: Read
     - Pull requests: Read and write
     - Workflows: Read and write
7. Copy the token immediately after creation

### NPM Registry Token

1. Log in to npmjs.com
2. Go to your profile → Access Tokens
3. Create a new token with "Automation" type
4. Copy the token immediately after creation

### Documentation Platform Token

1. Log in to your documentation platform
2. Navigate to API access or Developer settings
3. Generate a new token with write access
4. Set appropriate scopes for documentation updates
5. Copy the token immediately after creation

### Other Platform-Specific Tokens

Follow similar procedures for other platforms, ensuring you request the minimum necessary permissions.

## Adding Tokens to GitHub Secrets

1. Go to your GitHub repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: Use the corresponding secret name (e.g., `API_TOKEN`)
4. Value: Paste the token value
5. Click "Add secret"
6. Repeat for each token required

## Token Rotation Schedule

| Token Type | Rotation Frequency | Next Rotation Date | Owner |
|------------|-------------------|-------------------|-------|
| GitHub PAT | Every 90 days | [Add date] | [Add owner] |
| NPM Token | Every 180 days | [Add date] | [Add owner] |
| Documentation Token | Every 180 days | [Add date] | [Add owner] |
| CI/CD Token | Every 90 days | [Add date] | [Add owner] |
| Monitoring Token | Every 180 days | [Add date] | [Add owner] |
| Security Token | Every 90 days | [Add date] | [Add owner] |

## Self-Hosted Runner Security Considerations

When using API tokens with self-hosted runners, implement the following security measures:

1. **Environment Isolation**
   - Run the GitHub Actions runner in an isolated environment
   - Consider using Docker containers for additional isolation

2. **Network Security**
   - Use a dedicated network or VLAN for runners
   - Implement firewall rules to limit outbound connections
   - Consider using a proxy for API calls
   - Ensure the following essential domains are accessible:
     - `github.com`
     - `api.github.com`
     - `*.actions.githubusercontent.com`

3. **File System Protection**
   - Mount the runner's workspace as a temporary file system
   - Clean up workspace after each job completes
   - Ensure sensitive files are securely deleted

4. **Access Control**
   - Limit who can access the self-hosted runner machine
   - Use dedicated service accounts with minimal permissions
   - Implement audit logging for access

5. **Token Protection**
   - GitHub automatically masks secrets in logs
   - Avoid printing or logging token values in custom scripts
   - Don't store tokens in environment variables for longer than needed

## Troubleshooting API Token Issues

### Common Issues and Solutions

1. **Token Expired**
   - Error: "401 Unauthorized" or "Token expired"
   - Solution: Generate a new token and update the GitHub Secret

2. **Insufficient Permissions**
   - Error: "403 Forbidden"
   - Solution: Check if the token has the necessary scopes and permissions

3. **Rate Limiting**
   - Error: "429 Too Many Requests"
   - Solution: Implement exponential backoff or reduce API call frequency

4. **Network Issues**
   - Error: Connection timeout or network unreachable
   - Solution: Check network configuration of self-hosted runner

### Support Resources

- GitHub API Documentation: https://docs.github.com/en/rest
- NPM API Documentation: https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md
- GitHub Actions Troubleshooting: https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows

## Audit and Compliance

Implement the following practices for audit and compliance:

1. Regularly review action logs to monitor token usage
2. Document all token creations and rotations
3. Maintain an inventory of tokens and their access levels
4. Review workflow files for any accidental token leakage
5. Use tools like "gitleaks" to scan for unintentional token commits