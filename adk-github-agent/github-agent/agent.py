import os
import json
import asyncio
from google.adk.agents import Agent
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
        max_tools = 512
        if len(all_tools) > max_tools:
            logger.warning(f"Too many tools ({len(all_tools)}), limiting to {max_tools}")
            # Prioritize common GitHub operations by filtering tool names
            priority_keywords = [
                'repos', 'issues', 'pulls', 'users', 'orgs', 'contents', 
                'releases', 'branches', 'commits', 'search', 'gists'
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


