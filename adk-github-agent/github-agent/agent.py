import os
import json
import asyncio
import re
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
import logging
import sys

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("github_agent")

# Define both github_agent and root_agent (ADK framework looks for root_agent)
github_agent = None
root_agent = None

sensitive_substrings = [
    "token",
    "password",
]

def check_for_sensitive_info(pull_request: str) -> str:
    """
    Checks ALL files in a pull request for sensitive information that should not be in the code base.
    Performs comprehensive security analysis including tokens, passwords, keys, credentials, and suspicious files.

    Args:
        pull_request (str): The contents of a pull request (as a str)

    Returns:
        dict: A dictionary with the status and detailed security analysis

    Example:
        >>> check_for_sensitive_info(pull_request='TOKEN="123456789ABCDEFGHIJKLMNOP"')
        {'status': 'fail', 'message': 'Token discovered in pull request'}
    """
    # Convert to lowercase for initial basic checks
    pull_request_lower = pull_request.lower()
    pull_request_no_space = pull_request.strip()
    
    # Enhanced comprehensive security patterns
    security_findings = []
    
    # 1. Check original sensitive substrings (maintaining backwards compatibility)
    for substring in sensitive_substrings:
        check = substring + "="
        if check + '"' in pull_request_no_space or check + "'" in pull_request_no_space:
            security_findings.append(f'{substring} discovered in pull request')
    
    # 2. Advanced pattern matching for comprehensive security scan
    advanced_patterns = {
        "API Keys": [
            r'api[_-]?key[_-]?[=:]\s*["\']?([a-zA-Z0-9_\-\.]{20,})["\']?',
            r'apikey[_-]?[=:]\s*["\']?([a-zA-Z0-9_\-\.]{20,})["\']?'
        ],
        "GitHub Tokens": [
            r'ghp_[a-zA-Z0-9]{36}',  # GitHub personal access tokens
            r'github[_-]?token[_-]?[=:]\s*["\']?([a-zA-Z0-9_\-\.]{20,})["\']?'
        ],
        "AWS Credentials": [
            r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID
            r'aws[_-]?access[_-]?key[_-]?[=:]\s*["\']?([A-Z0-9]{20})["\']?',
            r'aws[_-]?secret[_-]?key[_-]?[=:]\s*["\']?([a-zA-Z0-9/+=]{40})["\']?'
        ],
        "Database URLs": [
            r'(postgresql|mysql|mongodb|redis)://[^\s\'"]+:[^\s\'"]+@[^\s\'"]+',
            r'database[_-]?url[_-]?[=:]\s*["\']?([^\s"\']+://[^\s"\']+)["\']?'
        ],
        "Private Keys": [
            r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
            r'-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----',
            r'-----BEGIN\s+EC\s+PRIVATE\s+KEY-----'
        ],
        "JWT Tokens": [
            r'eyJ[a-zA-Z0-9_\-]*\.eyJ[a-zA-Z0-9_\-]*\.[a-zA-Z0-9_\-]*'
        ],
        "Secrets & Passwords": [
            r'secret[_-]?[=:]\s*["\']?([a-zA-Z0-9_\-\.]{12,})["\']?',
            r'password[_-]?[=:]\s*["\']?([^\s"\']{6,})["\']?',
            r'pass[_-]?[=:]\s*["\']?([^\s"\']{6,})["\']?'
        ]
    }
    
    # Scan for advanced patterns
    for category, patterns in advanced_patterns.items():
        for pattern in patterns:
            if re.search(pattern, pull_request, re.IGNORECASE):
                security_findings.append(f'{category} pattern detected in pull request')
    
    # 3. Extract and analyze ALL file paths from PR diffs
    file_paths = set()
    diff_patterns = [
        r'diff --git a/(.*?) b/(.*?)(?:\n|$)',
        r'\+\+\+ b/(.*?)(?:\n|$)',
        r'--- a/(.*?)(?:\n|$)',
        r'rename from (.*?)(?:\n|$)',
        r'rename to (.*?)(?:\n|$)'
    ]
    
    for pattern in diff_patterns:
        matches = re.finditer(pattern, pull_request)
        for match in matches:
            for group in match.groups():
                if group and group.strip():
                    file_paths.add(group.strip())
    
    # 4. Check for suspicious files that commonly contain secrets
    suspicious_file_patterns = [
        r'\.env$', r'\.env\..*$',  # Environment files
        r'.*\.pem$', r'.*\.key$', r'.*\.p12$', r'.*\.pfx$',  # Certificate/key files
        r'id_rsa$', r'id_dsa$', r'id_ecdsa$',  # SSH keys
        r'\.ssh/.*$', r'\.aws/.*$',  # Config directories
        r'config\.json$', r'secrets\..*$', r'credentials$',  # Config files
        r'\.git-credentials$', r'\.netrc$',  # Git credentials
        r'docker-compose\.yml$', r'kubernetes\.yml$'  # Infrastructure files
    ]
    
    suspicious_files_found = []
    for file_path in file_paths:
        for pattern in suspicious_file_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                suspicious_files_found.append(file_path)
                security_findings.append(f'Suspicious file detected: {file_path}')
    
    # 5. Check for hidden/backup files that might leak secrets
    hidden_file_patterns = [r'^\.[a-zA-Z].*', r'.*\.bak$', r'.*\.backup$', r'.*\.tmp$', r'.*~$']
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        for pattern in hidden_file_patterns:
            if re.search(pattern, filename):
                security_findings.append(f'Hidden/backup file detected: {file_path}')
    
    # 6. Generate comprehensive response
    if security_findings:
        # Count different types of issues
        critical_count = len([f for f in security_findings if any(x in f.lower() for x in ['token', 'key', 'password', 'secret', 'credential'])])
        file_count = len([f for f in security_findings if 'file detected' in f])
        
        if critical_count > 0:
            status = 'fail'
            message = f'🚨 CRITICAL: {critical_count} high-severity security issues found! Files analyzed: {len(file_paths)}. Issues: {"; ".join(security_findings[:5])}'
        elif file_count > 0:
            status = 'fail'
            message = f'⚠️ WARNING: {file_count} suspicious files detected! Files analyzed: {len(file_paths)}. Issues: {"; ".join(security_findings[:5])}'
        else:
            status = 'fail'
            message = f'Security issues found in {len(file_paths)} files analyzed: {"; ".join(security_findings[:3])}'
    else:
        status = 'pass'
        message = f'✅ No sensitive information detected in {len(file_paths)} files analyzed. Good security practices!'
    
    return {'status': status, 'message': message}


def load_api_spec(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading API spec: {e}")
        return None

async def create_github_agent(api_spec_path=os.path.join(os.path.dirname(__file__), "api.github.com.fixed.json"), token_env_var="GITHUB_TOKEN", auth_prefix="token"):
    token = os.getenv(token_env_var)
    if not token:
        logger.error(f"GitHub token missing from environment variable: {token_env_var}")
        return None
        
    if not os.path.exists(api_spec_path):
        logger.error(f"GitHub API spec file not found: {api_spec_path}")
        return None
        
    spec = load_api_spec(api_spec_path)
    if not spec:
        return None
        
    try:
        auth_scheme, auth_credential = token_to_scheme_credential(
            "apikey", "header", "Authorization", f"{auth_prefix} {token}"
        )
        
        toolset = OpenAPIToolset(
            spec_str=json.dumps(spec),
            spec_str_type="json",
            auth_scheme=auth_scheme,
            auth_credential=auth_credential
        )
        
        all_tools = await toolset.get_tools()
        if not all_tools:
            logger.error("No tools found in GitHub API spec")
            return None
            
        logger.info(f"Found {len(all_tools)} GitHub API tools total")
        
        # Limit to 512 tools due to Gemini model constraints
        max_tools = 511
        if len(all_tools) > max_tools:
            logger.warning(f"Too many tools ({len(all_tools)}), limiting to {max_tools}")
            # Prioritize common GitHub operations by filtering tool names
            priority_keywords = [
                'repos', 'issues', 'pulls', 'users', 'orgs', 'contents', 
                'releases', 'branches', 'commits', 'search', 'wiki'
            ]
            
            # First, get tools with priority keywords
            priority_tools = []
            remaining_tools = []
            
            for tool in all_tools:
                tool_name_lower = tool.name.lower()
                if any(keyword in tool_name_lower for keyword in priority_keywords):
                    priority_tools.append(tool)
                else:
                    remaining_tools.append(tool)
            
            # Take priority tools first, then fill remaining slots
            tools = priority_tools[:max_tools]
            if len(tools) < max_tools:
                tools.extend(remaining_tools[:max_tools - len(tools)])
                
            logger.info(f"Selected {len(tools)} tools after filtering")
        else:
            tools = all_tools
            logger.info(f"Using all {len(tools)} GitHub API tools")

        tools.append(FunctionTool(func=check_for_sensitive_info))
        
        return Agent(
            name="github_agent",
            description="GitHub API Agent",
            instruction="""
            You are a GitHub API agent that interacts with GitHub's REST API.
            
            When working with the GitHub API:
            - Use parameters provided by the user
            - Ask for clarification if required parameters are missing
            - Format responses clearly for the user
            - Handle errors gracefully and explain issues in simple terms
            
            For content creation operations:
            - Use names and identifiers exactly as specified by the user
            - Add helpful descriptions when allowed by the API
            - Apply sensible defaults for optional parameters when not specified
            
            Always inform the user about the actions you're taking and the results received.
            """,
            model="gemini-2.5-pro",
            tools=tools
        )
    except Exception as e:
        logger.error(f"Error creating GitHub agent: {e}")
        return None

# Create the agent with GitHub configuration as default
def initialize_agent_sync():
    """Initialize the agent synchronously by running the async function."""
    global github_agent, root_agent
    
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is running, we need to create a task
            # This is a workaround for when called from an async context
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, create_github_agent())
                github_agent = future.result()
        else:
            # No running loop, safe to use asyncio.run
            github_agent = asyncio.run(create_github_agent())
    except RuntimeError:
        # Fallback: try with new event loop in thread
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, create_github_agent())
            github_agent = future.result()
    
    # Set root_agent to github_agent for compatibility with ADK framework
    root_agent = github_agent
    
    if github_agent:
        logger.info("GitHub agent created successfully")
        # Print available tools
        for tool in github_agent.tools:
            print(f"• {tool.name}")
        return github_agent
    else:
        logger.error("Failed to create GitHub agent")
        sys.exit(1)

# Initialize the agent
try:
    github_agent = initialize_agent_sync()
    root_agent = github_agent
except Exception as e:
    logger.error(f"Failed to initialize GitHub agent: {e}")
    sys.exit(1)


