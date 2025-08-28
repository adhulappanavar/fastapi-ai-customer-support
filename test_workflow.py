#!/usr/bin/env python3
"""
Test script for the Agentic Customer Support Workflow
"""

import requests
import json

def test_single_query(query: str):
    """Test a single query and display the full AI response"""
    base_url = "http://localhost:7777"
    
    print(f"🧪 Testing Single Query: {query}")
    print("=" * 60)
    
    try:
        params = {"workflow_id": "customer-support-resolution-pipeline"}
        
        response = requests.post(
            f"{base_url}/runs",
            params=params,
            data={"workflow_input": query}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Run ID: {result.get('run_id', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
            
            # Display the full AI-generated content
            content = result.get('content', 'No content')
            if content and content != 'No content':
                print(f"\n🤖 Full AI-Generated Solution:")
                print("=" * 60)
                print(content)
                print("=" * 60)
            else:
                print(f"Output: {result.get('output', 'No output yet')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_workflow():
    """Test the customer support workflow with sample queries"""
    
    base_url = "http://localhost:7777"  # Updated port
    
    # Sample customer support queries
    test_queries = [
        "I can't log into my account after changing my password",
        "My subscription was charged twice this month",
        "The app crashes every time I try to upload a file",
        "How do I enable two-factor authentication?",
        "I need help with the new dashboard layout"
    ]
    
    print("🚀 Testing Agentic Customer Support Workflow\n")
    print(f"Server: {base_url}")
    print("=" * 60)
    
    # First, check system status
    try:
        status_response = requests.get(f"{base_url}/status")
        if status_response.status_code == 200:
            print("✅ System Status: Available")
        else:
            print(f"❌ System Status Error: {status_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return
    
    print("\n📝 Testing Workflow Execution:")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 60)
        
        try:
            # Use the correct Agno API structure - workflow_id as query parameter, workflow_input as form data
            params = {"workflow_id": "customer-support-resolution-pipeline"}
            
            response = requests.post(
                f"{base_url}/runs",
                params=params,
                data={"workflow_input": query}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success!")
                print(f"Run ID: {result.get('run_id', 'N/A')}")
                print(f"Status: {result.get('status', 'N/A')}")
                
                # Extract and display the actual AI-generated content
                content = result.get('content', 'No content')
                if content and content != 'No content':
                    print(f"\n🤖 AI-Generated Solution:")
                    print("-" * 40)
                    # Truncate long responses for readability
                    if len(content) > 500:
                        print(f"{content[:500]}...")
                        print(f"\n[Content truncated. Full response is {len(content)} characters]")
                    else:
                        print(content)
                else:
                    print(f"Output: {result.get('output', 'No output yet')}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the server is running")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        print("\n" + "=" * 80)

def test_workflow_status():
    """Test checking the status of workflow runs"""
    base_url = "http://localhost:7777"
    
    print("\n🔄 Testing Workflow Status Check:")
    print("-" * 40)
    
    try:
        # First create a run
        params = {"workflow_id": "customer-support-resolution-pipeline"}
        
        response = requests.post(f"{base_url}/runs", params=params, data={"workflow_input": "Test query for status check"})
        if response.status_code == 200:
            run_data = response.json()
            run_id = run_data.get('run_id')
            print(f"✅ Created run with ID: {run_id}")
            
            # Now check the status
            status_response = requests.get(f"{base_url}/runs/{run_id}")
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"✅ Run Status: {status_data}")
            else:
                print(f"❌ Status check failed: {status_response.status_code}")
        else:
            print(f"❌ Failed to create run: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Choose your test option:")
    print("1. Test single query with full output")
    print("2. Test all queries (truncated output)")
    print("3. Test workflow status")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        query = input("Enter your customer support query: ").strip()
        if query:
            test_single_query(query)
        else:
            test_single_query("I cannot log into my account after changing my password")
    elif choice == "2":
        test_workflow()
        test_workflow_status()
    elif choice == "3":
        test_workflow_status()
    else:
        print("Invalid choice. Running default test...")
        test_single_query("I cannot log into my account after changing my password")
