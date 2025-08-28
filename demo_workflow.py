#!/usr/bin/env python3
"""
Demo script for the Agentic Customer Support Workflow
Automatically tests the workflow and shows AI-generated responses
"""

import requests
import time

def demo_workflow():
    """Demonstrate the AI workflow with sample queries"""
    
    main_api_url = "http://localhost:7777"
    ticketing_api_url = "http://localhost:8000"
    frontend_url = "http://localhost:3000"
    
    # Sample queries to demonstrate different capabilities
    demo_queries = [
        "I cannot log into my account after changing my password",
        "How do I enable two-factor authentication?",
        "My subscription was charged twice this month"
    ]
    
    print("🤖 Agentic Customer Support Workflow Demo")
    print("=" * 60)
    print(f"Main API: {main_api_url}")
    print(f"Ticketing API: {ticketing_api_url}")
    print(f"Frontend: {frontend_url}")
    print("=" * 60)
    
    # Check system status
    try:
        status_response = requests.get(f"{main_api_url}/status")
        if status_response.status_code == 200:
            print("✅ Main API Status: Available")
        else:
            print(f"❌ Main API Status Error: {status_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Main API Connection Error: {e}")
        return
    
    # Check ticketing API status
    try:
        ticketing_response = requests.get(f"{ticketing_api_url}/health")
        if ticketing_response.status_code == 200:
            print("✅ Ticketing API Status: Available")
        else:
            print(f"⚠️  Ticketing API Status: {ticketing_response.status_code}")
    except Exception as e:
        print(f"⚠️  Ticketing API Connection: {e}")
    
    print("\n🚀 Testing AI Workflow with Sample Queries:")
    print("=" * 60)
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n📝 Demo {i}: {query}")
        print("-" * 60)
        
        try:
            params = {"workflow_id": "rag-customer-support-resolution-pipeline"}
            
            response = requests.post(
                f"{main_api_url}/runs",
                params=params,
                data={"workflow_input": query}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success!")
                print(f"Run ID: {result.get('run_id', 'N/A')}")
                print(f"Status: {result.get('status', 'N/A')}")
                
                # Display the AI-generated content
                content = result.get('content', 'No content')
                if content and content != 'No content':
                    print(f"\n🤖 AI-Generated Solution:")
                    print("-" * 40)
                    
                    # Show first part of the response
                    lines = content.split('\n')
                    for line in lines[:15]:  # Show first 15 lines
                        print(line)
                    
                    if len(lines) > 15:
                        print(f"\n... [Content truncated. Full response has {len(lines)} lines]")
                        print(f"Full response length: {len(content)} characters")
                    
                    print("-" * 40)
                else:
                    print(f"Output: {result.get('output', 'No output yet')}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 80)
        
        # Small delay between requests
        if i < len(demo_queries):
            time.sleep(1)
    
    print("\n🎉 Demo Complete!")
    print("\n💡 What You've Seen:")
    print("✅ AI-powered problem classification")
    print("✅ Intelligent solution generation")
    print("✅ Professional, structured responses")
    print("✅ Different solution types for different queries")
    print("✅ Scalable workflow automation")
    
    print(f"\n🌐 Interactive API Documentation:")
    print(f"   Main API: {main_api_url}/docs")
    print(f"   Ticketing API: {ticketing_api_url}/docs")
    print(f"   Frontend: {frontend_url}")
    print("🚀 Your AI workflow is ready for production use!")

if __name__ == "__main__":
    demo_workflow()
