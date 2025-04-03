# GitHub IP Allowlist Configuration

This document provides configuration information for allowing GitHub Actions self-hosted runners to communicate with GitHub services.

## Essential Domains for Self-Hosted Runners

These domains **MUST** be accessible from your self-hosted runner for basic functionality:

| Domain | Purpose |
|--------|---------|
| `github.com` | Main GitHub site and API access |
| `api.github.com` | GitHub REST API endpoints |
| `*.actions.githubusercontent.com` | Action downloads, artifact storage, and communication |

## GitHub Action Domains by Service

### Core Action Services
```
github.com
api.github.com
codeload.github.com
*.actions.githubusercontent.com
vstoken.actions.githubusercontent.com
broker.actions.githubusercontent.com
launch.actions.githubusercontent.com
run-actions-*.actions.githubusercontent.com
setup-tools.actions.githubusercontent.com
```

### GitHub Packages Domains
```
ghcr.io
*.pkg.github.com
pkg.actions.githubusercontent.com
```

### GitHub Content and Storage Domains
```
objects.githubusercontent.com
objects-origin.githubusercontent.com
github-releases.githubusercontent.com
github-registry-files.githubusercontent.com
results-receiver.actions.githubusercontent.com
*.blob.core.windows.net
```

## IP Range Configuration

If your network requires IP-based firewall rules rather than domain-based rules, you can use the GitHub REST API to get a current list of GitHub IP addresses:

```sh
gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /meta
```

Or via curl:

```sh
curl -H "Accept: application/vnd.github+json" \
     -H "X-GitHub-Api-Version: 2022-11-28" \
     https://api.github.com/meta
```

### Key GitHub Services IP Ranges

You should allow outbound traffic to the IP ranges listed in these sections of the API response:

- `actions`: GitHub Actions service ranges
- `actions_macos`: GitHub-hosted MacOS runners
- `api`: GitHub API endpoints
- `git`: Git operations 
- `hooks`: GitHub webhooks service
- `web`: GitHub website
- `packages`: GitHub Packages
- `pages`: GitHub Pages

## Example Configurations

### macOS Network Filter Rule (pf)
```
# In /etc/pf.conf
# Allow GitHub domains
pass out proto tcp from any to github.com port 443
pass out proto tcp from any to api.github.com port 443
pass out proto tcp from any to *.actions.githubusercontent.com port 443
```

### Linux iptables Rules
```
# Allow GitHub domains via iptables
iptables -A OUTPUT -p tcp -d github.com --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp -d api.github.com --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp -d actions.githubusercontent.com --dport 443 -j ACCEPT
```

### Windows Firewall Rules
```powershell
# Allow GitHub domains via PowerShell
New-NetFirewallRule -DisplayName "Allow GitHub" -Direction Outbound -RemoteAddress github.com -Protocol TCP -RemotePort 443 -Action Allow
New-NetFirewallRule -DisplayName "Allow GitHub API" -Direction Outbound -RemoteAddress api.github.com -Protocol TCP -RemotePort 443 -Action Allow
New-NetFirewallRule -DisplayName "Allow GitHub Actions" -Direction Outbound -RemoteAddress actions.githubusercontent.com -Protocol TCP -RemotePort 443 -Action Allow
```

## Proxy Configuration

If your network uses a proxy, configure your self-hosted runner to use it:

1. Create or edit the `.env` file in your runner directory
2. Add the following configuration (with your actual proxy values):

```
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://proxy.example.com:8080
NO_PROXY=localhost,127.0.0.1
```

3. Restart the runner service

## Troubleshooting Connection Issues

1. Test basic connectivity to required domains:

```bash
curl -v https://github.com
curl -v https://api.github.com
curl -v https://pipelines.actions.githubusercontent.com
```

2. Check DNS resolution:

```bash
nslookup github.com
nslookup api.github.com
nslookup actions.githubusercontent.com
```

3. Verify TLS/SSL connectivity:

```bash
openssl s_client -connect github.com:443
openssl s_client -connect api.github.com:443
```

4. Check runner logs for connection errors:

```bash
cat ~/actions-runner/_diag/Runner_*.log | grep -i error
```

## Maintaining Up-to-date IP Addresses

GitHub's IP addresses may change over time. To ensure your configuration remains current:

1. Set up a scheduled job to fetch current IP ranges:

```bash
# Add to crontab
0 0 * * 0 curl -s https://api.github.com/meta > /path/to/github-meta.json
```

2. Consider automating firewall updates based on the fetched data

## Security Best Practices

1. Only allow the specific domains and IP ranges needed
2. Use HTTPS (port 443) exclusively for all GitHub communications
3. Implement network monitoring for unusual traffic patterns
4. Place runners in dedicated network segments when possible
5. Regularly update allowed IP ranges using the GitHub API

## References

- [GitHub Actions self-hosted runner networking documentation](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#communication-between-self-hosted-runners-and-github)
- [GitHub meta API documentation](https://docs.github.com/en/rest/meta/meta#get-github-meta-information)
- [Managing Dependabot on self-hosted runners](https://docs.github.com/en/code-security/dependabot/maintain-dependencies/managing-dependabot-on-self-hosted-runners)