# Security Scanner Usage Examples

The GitHub Agent now includes a custom security scanner tool that can detect sensitive information in commits, PRs, and code files.

## How to Use the Security Scanner

### 1. Scan a Commit
```
"Can you get the latest commit from my repository and scan it for any sensitive information?"
```

### 2. Scan a Pull Request
```
"Please check pull request #123 in my repo for any secrets or sensitive data"
```

### 3. Scan File Content
```
"Get the content of .env file from my repository and scan it for security issues"
```

### 4. Scan Commit Diff
```
"Show me the diff for commit abc123 and check if there are any security concerns"
```

## What the Scanner Detects

### High Severity Issues:
- **API Keys**: Various API key patterns (api_key, apikey)
- **GitHub Tokens**: Personal access tokens (ghp_*)
- **AWS Keys**: Access keys and secret keys
- **Database URLs**: Connection strings with credentials
- **Private Keys**: RSA, OpenSSH private keys
- **JWT Tokens**: JSON Web Tokens
- **Generic Secrets**: passwords, tokens, secrets

### Medium Severity Issues:
- **Suspicious Files**: .env, .pem, .key, config files
- **SSH Keys**: id_rsa, id_dsa files
- **Certificate Files**: .p12, .pfx files
- **Configuration Directories**: .ssh/, .aws/

### Low Severity Issues:
- **Hidden Files**: Files starting with dot (.)
- **Backup Files**: .bak, .tmp, ~ files

## Example Commands

### Basic Security Scan
```
User: "Scan this code for security issues: api_key = 'sk-1234567890abcdef'"
Agent: Uses security_scanner tool and reports findings with recommendations
```

### Repository Security Audit
```
User: "Can you check my latest 5 commits for any accidentally committed secrets?"
Agent: 
1. Gets latest 5 commits using GitHub API
2. For each commit, gets the diff
3. Runs security scanner on each diff
4. Provides comprehensive security report
```

### Pull Request Security Review
```
User: "Before I merge PR #456, can you check it for security issues?"
Agent:
1. Gets PR details and changes
2. Scans the PR diff for sensitive information
3. Provides security recommendations
```

## Security Scanner Response Format

The scanner returns structured results:

```json
{
    "scan_summary": {
        "total_findings": 3,
        "high_severity": 2,
        "medium_severity": 1,
        "low_severity": 0,
        "scan_type": "commit",
        "file_path": ".env"
    },
    "findings": [
        {
            "type": "API Keys",
            "pattern": "api[_-]?key[_-]?[=:]\\s*[\"']?([a-zA-Z0-9_-]{20,})[\"']?",
            "match": "api_key = 'sk-1234567890abcdef'",
            "line": 5,
            "severity": "HIGH"
        }
    ],
    "recommendation": "🚨 CRITICAL: 2 high-severity issues found! Review and remove sensitive data immediately."
}
```

## Integration with GitHub Operations

The security scanner works seamlessly with GitHub API operations:

1. **Automated Scanning**: When you request commit or PR information, you can ask the agent to automatically scan for security issues
2. **Batch Operations**: Scan multiple commits, files, or PRs in one request
3. **Repository Audits**: Perform comprehensive security audits of entire repositories

## Best Practices

1. **Regular Scanning**: Ask the agent to scan commits before pushing
2. **PR Reviews**: Always scan PRs before merging
3. **File Audits**: Regularly scan configuration and environment files
4. **Historical Analysis**: Scan historical commits to find previously committed secrets

## Example Workflow

```
User: "I want to do a security audit of my repository 'my-app'"

Agent Response:
1. "I'll help you perform a comprehensive security audit. Let me start by:"
2. "Getting your recent commits..."
3. "Scanning each commit for sensitive information..."
4. "Checking for suspicious files..."
5. "Generating a security report with recommendations..."

Final Report:
- ✅ 15 commits scanned
- ⚠️  2 high-severity issues found
- 📝 Recommendations provided
- 🔧 Remediation steps suggested
```

This security scanner adds an extra layer of protection to your GitHub workflow by automatically detecting sensitive information that might accidentally be committed to your repository.
