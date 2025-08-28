#!/usr/bin/env python3
"""
Test script to verify that responses are coming from the knowledge base
"""

import requests
import json
import time

def test_knowledge_base_integration():
    """Test that responses include knowledge base verification"""
    
    base_url = "http://localhost:7777"
    
    # Test queries that should have knowledge base content
    test_queries = [
        "My payment was declined when trying to renew my subscription",
        "I can't log into my account after changing my password",
        "App crashes when opening settings page",
        "How do I reset my password?",
        "Billing subscription issues"
    ]
    
    print("🧪 Testing Knowledge Base Integration")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 40)
        
        try:
            # Make API call
            response = requests.post(
                f"{base_url}/runs?workflow_id=rag-customer-support-resolution-pipeline",
                data={"workflow_input": query}
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('content', '')
                
                print("✅ API call successful")
                print(f"📏 Response length: {len(content)} characters")
                
                # Check for knowledge base verification
                if "KNOWLEDGE BASE VERIFICATION" in content:
                    print("🔍 Knowledge Base verification found!")
                    
                    # Extract verification section
                    kb_start = content.find("--- KNOWLEDGE BASE VERIFICATION ---")
                    if kb_start != -1:
                        kb_section = content[kb_start:]
                        print("📚 Knowledge Base details:")
                        print(kb_section)
                        
                        # Check if documents were used
                        if "relevant documents from your knowledge base" in kb_section:
                            print("✅ Response uses knowledge base documents")
                        else:
                            print("⚠️ Response indicates no KB documents found")
                    else:
                        print("❌ Could not parse KB verification section")
                else:
                    print("❌ No Knowledge Base verification found in response")
                    print("⚠️ This might be a generic AI response")
                
                # Check for specific knowledge base content
                if "Knowledge Base Document" in content:
                    print("✅ Knowledge base document content detected")
                elif "No specific knowledge base documents found" in content:
                    print("⚠️ Response indicates no KB documents were found")
                else:
                    print("❓ Cannot determine knowledge base usage")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
        time.sleep(1)  # Small delay between requests
    
    print("\n🎯 Knowledge Base Integration Test Summary:")
    print("=" * 60)
    print("✅ Look for 'KNOWLEDGE BASE VERIFICATION' sections")
    print("✅ Check for document references and relevance scores")
    print("✅ Verify response length and content quality")
    print("⚠️ Generic responses won't have KB verification")
    print("🔍 Check FastAPI logs for RAG processing details")

if __name__ == "__main__":
    test_knowledge_base_integration()
