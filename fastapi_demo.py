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
    
    log_info(f"🚀 === STARTING RAG-FIRST PROCESSING ===")
    log_info(f"📝 Query: {query}")
    
    cached_solution = workflow.workflow_session_state.get("solutions", {}).get(query)
    if cached_solution:
        log_info(f"🔄 Cache hit! Returning cached solution for query: {query}")
        return cached_solution

    log_info(f"🆕 No cached solution found, querying knowledge base...")

    # Step 1: Query the vector database for relevant knowledge (PRIMARY SOURCE)
    log_info(f"🔍 Querying LanceDB vector database as PRIMARY source...")
    
    # Initialize variables outside try block
    search_results = []
    knowledge_context = ""
    
    try:
        # Search for relevant documents in the knowledge base with higher limit for comprehensive coverage
        search_results = vector_db.search(query, limit=5)
        log_info(f"📚 Found {len(search_results)} relevant documents in knowledge base")
        
        # Extract content from search results
        if search_results:
            for i, result in enumerate(search_results):
                log_info(f"📄 Document {i+1}: {result.get('title', 'Untitled')} (Score: {result.get('score', 'N/A')})")
                knowledge_context += f"\n--- Knowledge Base Document {i+1} ---\n{result.get('content', '')}\n"
            
            # If we have good knowledge base coverage, use it directly
            if len(search_results) >= 2 or any(result.get('score', 0) > 0.7 for result in search_results):
                log_info(f"✅ Strong knowledge base coverage found - generating RAG-first solution")
                solution = generate_rag_first_solution(query, search_results, knowledge_context)
            else:
                log_info(f"⚠️ Limited knowledge base coverage - using AI agent with KB constraints")
                solution = generate_ai_enhanced_solution(query, search_results, knowledge_context)
        else:
            log_info(f"⚠️ No relevant documents found in knowledge base")
            knowledge_context = "No specific knowledge base documents found for this query."
            solution = generate_fallback_solution(query)
        
        log_info(f"📏 Knowledge context length: {len(knowledge_context)} characters")
        
    except Exception as e:
        log_info(f"❌ Error querying vector database: {e}")
        knowledge_context = "Error accessing knowledge base."
        search_results = []
        solution = generate_fallback_solution(query)
    
    # Step 2: Solution generation is now handled by helper functions based on KB coverage
    log_info(f"🔧 Solution generation strategy determined by knowledge base coverage")
    
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


def generate_rag_first_solution(query: str, search_results: list, knowledge_context: str) -> str:
    """Generate solution primarily from knowledge base content with minimal AI processing"""
    log_info(f"🔧 Generating RAG-first solution from knowledge base...")
    
    # Extract the most relevant content and structure it
    primary_docs = []
    for result in search_results:
        if result.get('score', 0) > 0.5:  # Only use high-confidence matches
            primary_docs.append({
                'title': result.get('title', 'Untitled'),
                'content': result.get('content', ''),
                'score': result.get('score', 0)
            })
    
    if not primary_docs:
        primary_docs = search_results[:2]  # Fallback to first 2 results
    
    # Structure the solution directly from knowledge base
    solution = f"# Solution for: {query}\n\n"
    solution += "## Based on Knowledge Base Documents\n\n"
    
    for i, doc in enumerate(primary_docs):
        solution += f"### From: {doc['title']}\n"
        # Extract key steps and information from the document content
        content_lines = doc['content'].split('\n')
        step_count = 1
        
        for line in content_lines:
            line = line.strip()
            if line and len(line) > 10:  # Filter out very short lines
                if any(keyword in line.lower() for keyword in ['step', 'solution', 'fix', 'resolve', 'troubleshoot']):
                    solution += f"{step_count}. {line}\n"
                    step_count += 1
                elif line.startswith('-') or line.startswith('•'):
                    solution += f"{step_count}. {line[1:].strip()}\n"
                    step_count += 1
                elif len(line) > 50:  # Longer descriptive lines
                    solution += f"{step_count}. {line}\n"
                    step_count += 1
        
        solution += "\n"
    
    solution += "## Verification Steps\n"
    solution += "1. Follow the steps above in order\n"
    solution += "2. Test the solution to confirm it resolves the issue\n"
    solution += "3. If the issue persists, check for additional error messages\n\n"
    
    solution += "## Knowledge Source\n"
    solution += f"This solution is directly derived from {len(primary_docs)} knowledge base documents with relevance scores above 0.5."
    
    return solution


def generate_ai_enhanced_solution(query: str, search_results: list, knowledge_context: str) -> str:
    """Generate solution using AI agent but heavily constrained by knowledge base content"""
    log_info(f"🤖 Generating AI-enhanced solution with KB constraints...")
    
    # Use AI agent but with strict instructions to prioritize KB content
    solution_context = f"""
    Customer Query: {query}

    KNOWLEDGE BASE CONTENT (PRIMARY SOURCE):
    {knowledge_context}

    CRITICAL INSTRUCTIONS:
    1. Your response MUST be based PRIMARILY on the knowledge base content above
    2. Do NOT provide generic AI solutions unless the KB content is insufficient
    3. If KB content exists, use it as the foundation and only enhance with formatting
    4. Structure the response as: Problem Analysis → Solution Steps → Verification → Prevention
    5. Reference specific KB documents and their relevance scores
    6. If KB content is missing critical information, clearly indicate what's missing
    """

    solution_response = support_agent.run(solution_context)
    return solution_response.content


def generate_fallback_solution(query: str) -> str:
    """Generate fallback solution when no KB content is available"""
    log_info(f"⚠️ Generating fallback solution - no KB content available")
    
    fallback_context = f"""
    Customer Query: {query}

    IMPORTANT: No relevant knowledge base documents were found for this query.
    
    INSTRUCTIONS:
    1. Provide a general troubleshooting approach
    2. Suggest contacting support for specific guidance
    3. Offer basic diagnostic steps
    4. Clearly indicate this is NOT from the knowledge base
    5. Recommend uploading relevant documentation to improve future responses
    """

    solution_response = support_agent.run(fallback_context)
    return solution_response.content


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
