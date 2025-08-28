#!/usr/bin/env python3
"""
Demo script for the Agentic Customer Support Workflow
Shows how the AI agents work together to solve customer issues
"""

def demo_workflow():
    """Demonstrate the workflow logic without requiring external dependencies"""
    
    print("🤖 Agentic Customer Support Workflow Demo")
    print("=" * 60)
    
    # Sample customer queries
    queries = [
        "I can't log into my account after changing my password",
        "My subscription was charged twice this month",
        "The app crashes every time I try to upload a file"
    ]
    
    print("\n📋 Sample Customer Queries:")
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")
    
    print("\n🔄 Workflow Process:")
    print("1. Customer submits query")
    print("2. Ticket Classifier Agent analyzes and categorizes:")
    print("   - Category: technical/account_access/billing")
    print("   - Priority: low/medium/high/urgent")
    print("   - Tags: relevant keywords")
    print("   - Summary: brief description")
    print("3. Solution Developer Agent generates solution:")
    print("   - Problem diagnosis")
    print("   - Step-by-step instructions")
    print("   - Alternative approaches")
    print("   - Prevention tips")
    print("4. Response returned with full analysis")
    
    print("\n💡 Key Features:")
    print("✅ Intelligent classification and prioritization")
    print("✅ Context-aware solution generation")
    print("✅ Smart caching for similar queries")
    print("✅ AI-powered understanding of customer issues")
    print("✅ Professional, customer-friendly responses")
    
    print("\n🚀 To run the full system:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Start the server: python fastapi_demo.py")
    print("4. Test with: python test_workflow.py")
    
    print("\n🌐 API Endpoint:")
    print("POST /runs")
    print("Body: {\"workflow_id\": \"customer-support-resolution-pipeline\", \"input\": {\"query\": \"your customer issue here\"}}")
    
    print("\n📚 Interactive Documentation:")
    print("http://localhost:7777/docs (Swagger UI)")

if __name__ == "__main__":
    demo_workflow()
