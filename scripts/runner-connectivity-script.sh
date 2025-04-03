#!/bin/bash
# GitHub Actions Self-Hosted Runner Connectivity Test Script
# Tests connection to required GitHub domains and reports status

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo "===== GitHub Actions Runner Connectivity Test ====="
echo "Testing connection to required GitHub domains..."
echo ""

# Test function
test_domain() {
  local domain=$1
  local port=${2:-443}
  local description=${3:-"Required Domain"}
  
  echo -n "Testing ${domain}:${port} (${description})... "
  
  # Try curl first with a timeout
  if curl -s --connect-timeout 5 --max-time 10 -o /dev/null https://${domain}; then
    echo -e "${GREEN}SUCCESS${NC}"
    return 0
  else
    if command -v nc > /dev/null; then
      if nc -z -w 5 ${domain} ${port} 2>/dev/null; then
        echo -e "${YELLOW}PARTIAL SUCCESS${NC} (TCP connection works, but HTTPS failed)"
        return 1
      else
        echo -e "${RED}FAILED${NC} (nc failed)"
      fi
    elif command -v telnet > /dev/null; then
      if echo | telnet ${domain} ${port} 2>/dev/null | grep -q "Connected"; then
        echo -e "${YELLOW}PARTIAL SUCCESS${NC} (TCP connection works, but HTTPS failed)"
        return 1
      else
        echo -e "${RED}FAILED${NC} (telnet failed)"
      fi
    else
      echo -e "${RED}FAILED${NC} (nc and telnet not found)"
      return 2
    fi
}

# Core domains
echo "== Core Domains =="
test_domain "github.com" 443 "Main GitHub site"
GITHUB_STATUS=$?
test_domain "api.github.com" 443 "GitHub API"
API_STATUS=$?

# Actions domains
echo -e "\n== Actions Domains =="
test_domain "actions.githubusercontent.com" 443 "GitHub Actions content"
ACTIONS_STATUS=$?
test_domain "pipelines.actions.githubusercontent.com" 443 "GitHub Actions pipelines"
PIPELINES_STATUS=$?
test_domain "vstoken.actions.githubusercontent.com" 443 "GitHub Actions token service"
TOKEN_STATUS=$?

# Package domains
echo -e "\n== Package Domains =="
test_domain "ghcr.io" 443 "GitHub Container Registry"
GHCR_STATUS=$?
test_domain "pkg.github.com" 443 "GitHub Packages"
PKG_STATUS=$?

# Downloads and storage domains
echo -e "\n== Content Domains =="
test_domain "objects.githubusercontent.com" 443 "GitHub LFS objects"
OBJECTS_STATUS=$?
test_domain "github-releases.githubusercontent.com" 443 "GitHub release assets"
RELEASES_STATUS=$?
test_domain "codeload.github.com" 443 "GitHub code download"
CODELOAD_STATUS=$?

# Check DNS resolution
echo -e "\n== DNS Resolution Test =="
echo -n "Testing DNS resolution for github.com... "
if nslookup github.com > /dev/null 2>&1; then
  echo -e "${GREEN}SUCCESS${NC}"
  DNS_STATUS=0
else
  echo -e "${RED}FAILED${NC}"
  DNS_STATUS=1
fi

# Summarize results
echo -e "\n===== Results Summary ====="
TOTAL_TESTS=9
FAILED_TESTS=0

if [ $GITHUB_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $API_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $ACTIONS_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $PIPELINES_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $TOKEN_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $GHCR_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $PKG_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $OBJECTS_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $RELEASES_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $CODELOAD_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi
if [ $DNS_STATUS -gt 0 ]; then FAILED_TESTS=$((FAILED_TESTS+1)); fi

PASSED_TESTS=$((TOTAL_TESTS-FAILED_TESTS))

echo "Successful connections: $PASSED_TESTS of $TOTAL_TESTS"
echo "Failed connections: $FAILED_TESTS of $TOTAL_TESTS"

# Provide guidance based on results
echo -e "\n===== Recommendations ====="
if [ $FAILED_TESTS -eq 0 ]; then
  echo -e "${GREEN}All connectivity tests passed!${NC} Your runner should be able to communicate with GitHub services."
  echo "You can now configure your GitHub Actions workflow to use your self-hosted runner."
else
  echo -e "${RED}Some connectivity tests failed.${NC} Your runner may have trouble communicating with GitHub."
  echo "Please check the following:"
  
  if [ $DNS_STATUS -gt 0 ]; then
    echo "- DNS resolution is not working properly. Check your DNS settings."
  fi
  
  if [ $GITHUB_STATUS -gt 0 ] || [ $API_STATUS -gt 0 ]; then
    echo "- Core GitHub domains are not accessible. These are required for basic functionality."
    echo "  Ensure github.com and api.github.com are allowed in your firewall/proxy."
  fi
  
  if [ $ACTIONS_STATUS -gt 0 ] || [ $PIPELINES_STATUS -gt 0 ] || [ $TOKEN_STATUS -gt 0 ]; then
    echo "- GitHub Actions domains are not accessible. These are required for runner operation."
    echo "  Ensure *.actions.githubusercontent.com is allowed in your firewall/proxy."
  fi
  
  echo ""
  echo "For detailed information on required domains and IP ranges, refer to:"
  echo "- github-ip-allowlist.md in this directory"
  echo "- https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners"
fi

# Detect if running behind a proxy
echo -e "\n== Proxy Detection =="
if [ -n "$http_proxy" ] || [ -n "$https_proxy" ] || [ -n "$HTTP_PROXY" ] || [ -n "$HTTPS_PROXY" ]; then
  echo -e "${YELLOW}Proxy environment variables detected:${NC}"
  [ -n "$http_proxy" ] && echo "http_proxy=$http_proxy"
  [ -n "$https_proxy" ] && echo "https_proxy=$https_proxy"
  [ -n "$HTTP_PROXY" ] && echo "HTTP_PROXY=$HTTP_PROXY"
  [ -n "$HTTPS_PROXY" ] && echo "HTTPS_PROXY=$HTTPS_PROXY"
  [ -n "$no_proxy" ] && echo "no_proxy=$no_proxy"
  [ -n "$NO_PROXY" ] && echo "NO_PROXY=$NO_PROXY"
  
  echo -e "\nIf your proxy requires authentication, ensure it's configured correctly in your runner's .env file."
else
  echo "No proxy environment variables detected."
fi

echo -e "\n===== GitHub IP Range Information ====="
echo "To get the current list of GitHub IP ranges, run:"
echo "curl -s https://api.github.com/meta | jq"
echo ""
echo "Script completed at $(date)"