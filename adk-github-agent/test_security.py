#!/usr/bin/env python3
"""
Test script to demonstrate the SecurityScannerTool functionality
"""

# Import the security scanner from the agent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'github-agent'))

# Test content with various sensitive patterns
test_samples = {
    "environment_file": """
# .env file content
DATABASE_URL=postgresql://user:password123@localhost:5432/mydb
API_KEY=sk-1234567890abcdef1234567890abcdef
GITHUB_TOKEN=ghp_1234567890abcdef1234567890abcdef123456
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
""",
    
    "commit_diff": """
diff --git a/.env b/.env
new file mode 100644
index 0000000..1234567
--- /dev/null
+++ b/.env
@@ -0,0 +1,3 @@
+DATABASE_URL=postgresql://user:secret@localhost/db
+API_TOKEN=abc123def456ghi789
+SECRET_KEY=super-secret-key-12345
""",
    
    "source_code": """
import os
import requests

# Bad practice - hardcoded secrets
api_key = "sk-abcd1234567890abcdef1234567890ab"
github_token = "ghp_abcdefghijklmnopqrstuvwxyz123456789"

def make_request():
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-GitHub-Token": github_token
    }
    return requests.get("https://api.example.com", headers=headers)
""",
    
    "private_key": """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAwJKE8K7Q2M9J3rN8K9Q2M9J3rN8K9Q2M9J3rN8K9Q2M9J3rN
8K9Q2M9J3rN8K9Q2M9J3rN8K9Q2M9J3rN8K9Q2M9J3rN8K9Q2M9J3rN8K9Q2M9J
-----END RSA PRIVATE KEY-----
""",
    
    "clean_code": """
import os
import requests

def make_request():
    # Good practice - using environment variables
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable not set")
    
    headers = {"Authorization": f"Bearer {api_key}"}
    return requests.get("https://api.example.com", headers=headers)
"""
}

def test_security_scanner():
    """Test the security scanner with different types of content."""
    try:
        # Import after adding to path
        from agent import security_scanner
        
        print("🔍 Security Scanner Test Results")
        print("=" * 50)
        
        for sample_name, content in test_samples.items():
            print(f"\n📄 Testing: {sample_name}")
            print("-" * 30)
            
            # Simulate different file paths for testing
            file_paths = {
                "environment_file": ".env",
                "commit_diff": None,
                "source_code": "app.py",
                "private_key": "private.key",
                "clean_code": "secure_app.py"
            }
            
            result = security_scanner(
                content=content,
                file_path=file_paths.get(sample_name),
                scan_type="file"
            )
            
            # Display results
            summary = result["scan_summary"]
            print(f"Total findings: {summary['total_findings']}")
            print(f"High severity: {summary['high_severity']}")
            print(f"Medium severity: {summary['medium_severity']}")
            print(f"Low severity: {summary['low_severity']}")
            
            if "recommendation" in result:
                print(f"Recommendation: {result['recommendation']}")
            
            if result["findings"]:
                print("\nDetailed findings:")
                for finding in result["findings"][:3]:  # Show first 3 findings
                    print(f"  • {finding['type']}: {finding['match']} (Line {finding['line']})")
                
                if len(result["findings"]) > 3:
                    print(f"  ... and {len(result['findings']) - 3} more findings")
        
        print("\n✅ Security scanner test completed!")
        
    except ImportError as e:
        print(f"❌ Could not import security_scanner: {e}")
        print("Make sure the agent.py file is in the github-agent directory")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_security_scanner()
