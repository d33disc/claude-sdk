# Network Requirements for GitHub Actions Self-Hosted Runners

## Essential Domains

The following domains **MUST** be accessible from your self-hosted runner:

| Domain | Port | Purpose |
|--------|------|--------|
| `github.com` | 443 | GitHub website and basic API access |
| `api.github.com` | 443 | GitHub REST API endpoints |
| `*.actions.githubusercontent.com` | 443 | Action downloads and artifact storage |

## Additional Recommended Domains

Depending on your workflow needs, these additional domains may be required:

| Domain | Port | Purpose |
|--------|------|--------|
| `github-releases.githubusercontent.com` | 443 | GitHub release asset downloads |
| `codeload.github.com` | 443 | Repository archive downloads |
| `pkg.github.com` | 443 | GitHub Packages access |
| `objects.githubusercontent.com` | 443 | GitHub LFS objects |

## Firewall Configuration

Ensure your network firewall allows outbound HTTPS (TCP 443) traffic to the domains listed above.

Example firewall rule (pseudo-syntax):
```
allow outbound tcp to github.com:443
allow outbound tcp to api.github.com:443
allow outbound tcp to *.actions.githubusercontent.com:443
```

## Proxy Configuration

If your network requires a proxy, configure the self-hosted runner to use it:

```shell
# Add these lines to the .env file in your runner directory
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://proxy.example.com:8080
NO_PROXY=localhost,127.0.0.1
```

Restart the runner after making these changes.

## Testing Network Connectivity

Use these commands to test connectivity to the required domains:

```shell
# Test basic connectivity
curl -s https://github.com > /dev/null && echo "GitHub.com: OK" || echo "GitHub.com: FAIL"
curl -s https://api.github.com > /dev/null && echo "API GitHub.com: OK" || echo "API GitHub.com: FAIL"

# Test runner-specific endpoint
# Replace the URL with a valid Actions URL if you know one
curl -s https://pipelines.actions.githubusercontent.com > /dev/null && echo "Actions: OK" || echo "Actions: FAIL"
```

## Troubleshooting Network Issues

If you encounter connectivity problems:

1. Verify DNS resolution works for the required domains
2. Check if TLS inspection is interfering with connections
3. Ensure any content filtering or deep packet inspection systems allow GitHub domains
4. Check for corporate proxies that might require additional configuration
5. Review your runner's logs for network-related errors

## Security Considerations

While you need to allow access to these domains, consider these security measures:

1. Use firewall rules that allow only the specific domains needed, not all outbound traffic
2. Implement TLS inspection carefully if required by your security policy
3. Consider network-level monitoring for unusual traffic patterns
4. Place runners in a dedicated network segment with appropriate controls
5. Use IP allow-listing when possible to restrict traffic to GitHub's IP ranges