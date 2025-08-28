from agno.agent import Agent
from agno.app.fastapi import FastAPIApp
from agno.models.openai.chat import OpenAIChat
from agno.utils.log import log_info
from agno.workflow.v2 import Workflow
from dotenv import load_dotenv
import os
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType

# Load environment variables from .env file
load_dotenv()

# Verify API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  WARNING: OPENAI_API_KEY not found in .env file")
    print("Please create a .env file with: OPENAI_API_KEY=your-key-here")
else:
    print("✅ OPENAI_API_KEY loaded from .env file")

# Initialize vector database for RAG capabilities
try:
    os.makedirs("tmp", exist_ok=True)
    vector_db = LanceDb(
        table_name="customer_support_kb",
        uri="tmp/lancedb",
        search_type=SearchType.hybrid,
    )
    print("✅ Vector database initialized successfully")
except Exception as e:
    print(f"❌ Error initializing vector database: {e}")
    vector_db = None

agent_storage_file: str = "tmp/agents.db"

# Define agents
support_agent = Agent(
    name="RAG-Powered Solution Developer",
    model=OpenAIChat(id="gpt-4o"),
    instructions="""
    You are a RAG-powered Solution Developer Agent for customer support with access to a comprehensive knowledge base.

    KNOWLEDGE BASE CONTENTS:

    1. CUSTOMER SUPPORT GUIDE:
       - Account Access Issues: Login problems, password resets, 2FA, account lockouts
       - General Troubleshooting: Common errors, security best practices, prevention tips
       - Support Procedures: Contact info, escalation, response times

    2. TECHNICAL TROUBLESHOOTING:
       - System Diagnostics: Performance, memory, CPU, health checks
       - Network Issues: Connectivity, latency, firewall, security
       - Database Problems: Connections, performance, corruption, recovery
       - API and Integration: Authentication, rate limiting, third-party services

    3. BILLING AND SUBSCRIPTION:
       - Account Management: Setup, verification, permissions
       - Payment Issues: Declined payments, expired methods, fraud prevention
       - Subscription Management: Plan changes, cancellations, billing cycles
       - Invoice and Billing: Generation, discrepancies, tax compliance

    SOLUTION REQUIREMENTS:
    - Always provide step-by-step numbered instructions
    - Include verification steps for each solution
    - Offer alternative approaches when available
    - Provide prevention tips for future issues
    - Reference specific knowledge base sections
    - Use clear, customer-friendly language
    - Include troubleshooting steps for common failures

    RESPONSE FORMAT:
    1. Problem Analysis: Brief summary of the issue
    2. Step-by-Step Solution: Numbered, actionable steps
    3. Verification: How to confirm the solution worked
    4. Alternatives: Backup approaches if main solution fails
    5. Prevention: Tips to avoid similar issues
    6. Knowledge Source: Reference to relevant knowledge base section
    """,
    markdown=True,
)

triage_agent = Agent(
    name="Ticket Classifier",
    model=OpenAIChat(id="gpt-4o"),
    instructions="""
            You are a customer support ticket classifier. Your job is to analyze customer queries and extract key information.

            For each customer query, provide:
            1. Category (billing, technical, account_access, product_info, bug_report, feature_request)
            2. Priority (low, medium, high, urgent)
            3. Key tags/keywords (extract 3-5 relevant terms)
            4. Brief summary of the issue

            Format your response as:
            Category: [category]
            Priority: [priority]
            Tags: [tag1, tag2, tag3]
            Summary: [brief summary]
            """,
    markdown=True,
)


def cache_solution(workflow: Workflow, query: str, solution: str):
    if "solutions" not in workflow.workflow_session_state:
        workflow.workflow_session_state["solutions"] = {}
    workflow.workflow_session_state["solutions"][query] = solution


def customer_support_execution(workflow: Workflow, input_data) -> str:
    # Extract query from the input data
    if hasattr(input_data, 'workflow_input'):
        query = input_data.workflow_input
    elif hasattr(input_data, 'message'):
        query = input_data.message
    elif isinstance(input_data, dict) and 'workflow_input' in input_data:
        query = input_data['workflow_input']
    elif isinstance(input_data, str):
        query = input_data
    else:
        query = str(input_data)
    
    log_info(f"🚀 === STARTING RAG PROCESSING ===")
    log_info(f"📝 Query: {query}")
    
    cached_solution = workflow.workflow_session_state.get("solutions", {}).get(query)
    if cached_solution:
        log_info(f"🔄 Cache hit! Returning cached solution for query: {query}")
        return cached_solution

    log_info(f"🆕 No cached solution found, querying knowledge base...")

    # Step 1: Query the vector database for relevant knowledge
    log_info(f"🔍 Querying LanceDB vector database...")
    try:
        # Search for relevant documents in the knowledge base
        search_results = vector_db.search(query, limit=3)
        log_info(f"📚 Found {len(search_results)} relevant documents in knowledge base")
        
        # Extract content from search results
        knowledge_context = ""
        if search_results:
            for i, result in enumerate(search_results):
                log_info(f"📄 Document {i+1}: {result.get('title', 'Untitled')} (Score: {result.get('score', 'N/A')})")
                knowledge_context += f"\n--- Knowledge Base Document {i+1} ---\n{result.get('content', '')}\n"
        else:
            log_info(f"⚠️ No relevant documents found in knowledge base")
            knowledge_context = "No specific knowledge base documents found for this query."
        
        log_info(f"📏 Knowledge context length: {len(knowledge_context)} characters")
        
    except Exception as e:
        log_info(f"❌ Error querying vector database: {e}")
        knowledge_context = "Error accessing knowledge base."
    
    # Step 2: Classify the query
    log_info(f"🏷️ Classifying query with AI agent...")
    classification_response = triage_agent.run(query)
    classification = classification_response.content
    log_info(f"✅ Classification: {classification}")

    # Step 3: Generate solution using knowledge base context
    log_info(f"🤖 Generating solution using knowledge base context...")
    solution_context = f"""
    Customer Query: {query}

    Classification: {classification}

    Knowledge Base Context:
    {knowledge_context}

    Instructions:
    Please provide a clear, step-by-step solution for this customer issue.
    Make sure to format it in a customer-friendly way with clear instructions.
    
    IMPORTANT: Base your response on the knowledge base context provided above.
    If the knowledge base contains relevant information, use it as the primary source.
    If no relevant knowledge base documents are found, indicate this clearly.
    
    Always include a "Knowledge Source" section at the end showing which documents were referenced.
    """

    solution_response = support_agent.run(solution_context)
    solution = solution_response.content
    
    # Add knowledge base verification to the solution
    if search_results:
        kb_reference = "\n\n--- KNOWLEDGE BASE VERIFICATION ---\n"
        kb_reference += f"This solution was generated using {len(search_results)} relevant documents from your knowledge base:\n"
        for i, result in enumerate(search_results):
            kb_reference += f"- Document {i+1}: {result.get('title', 'Untitled')} (Relevance Score: {result.get('score', 'N/A')})\n"
        kb_reference += f"\nTotal knowledge context used: {len(knowledge_context)} characters"
        solution += kb_reference
    else:
        solution += "\n\n--- KNOWLEDGE BASE VERIFICATION ---\n⚠️ No relevant knowledge base documents found for this query. This response is generated from general AI knowledge."

    log_info(f"💾 Caching solution for future use...")
    cache_solution(workflow, query, solution)
    
    log_info(f"🎉 === RAG PROCESSING COMPLETED ===")
    log_info(f"📊 Solution summary: {len(solution)} characters, {len(search_results) if search_results else 0} KB documents used")

    return solution


# Create the customer support workflow
customer_support_workflow = Workflow(
    workflow_id="rag-customer-support-resolution-pipeline",
    name="RAG-Powered Customer Support Resolution Pipeline",
    description="AI-powered customer support with RAG knowledge base and intelligent caching",
    steps=customer_support_execution,
    workflow_session_state={},  # Initialize empty session state
)

fastapi_app = FastAPIApp(
    workflows=[customer_support_workflow],
    app_id="workflows-fastapi-app",
    name="Workflows FastAPI App",
)
app = fastapi_app.get_app(use_async=False)

if __name__ == "__main__":
    # Start the fastapi server
    fastapi_app.serve(app="fastapi_demo:app", reload=True)
