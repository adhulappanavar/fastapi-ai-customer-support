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
    
    log_info(f"Processing query: {query}")
    
    cached_solution = workflow.workflow_session_state.get("solutions", {}).get(query)
    if cached_solution:
        log_info(f"Cache hit! Returning cached solution for query: {query}")
        return cached_solution

    log_info(f"No cached solution found for query: {query}")

    classification_response = triage_agent.run(query)
    classification = classification_response.content

    solution_context = f"""
    Customer Query: {query}

    Classification: {classification}

    Please provide a clear, step-by-step solution for this customer issue.
    Make sure to format it in a customer-friendly way with clear instructions.
    """

    solution_response = support_agent.run(solution_context)
    solution = solution_response.content

    cache_solution(workflow, query, solution)

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
