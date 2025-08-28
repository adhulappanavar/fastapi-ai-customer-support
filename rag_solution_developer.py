#!/usr/bin/env python3
"""
RAG-Powered Solution Developer Agent for Customer Support
Uses knowledge base to provide accurate, context-aware solutions
"""

import typer
from agno.agent import Agent
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import os

console = Console()

# Initialize vector database for customer support knowledge
vector_db = LanceDb(
    table_name="customer_support_kb",
    uri="tmp/lancedb",
    search_type=SearchType.hybrid,
)

# Knowledge base with local customer support documentation
knowledge_base = PDFUrlKnowledgeBase(
    urls=[
        # Local PDF files - these will be created by create_pdfs.py
        "knowledge_base/customer_support_guide.pdf",
        "knowledge_base/technical_troubleshooting_guide.pdf", 
        "knowledge_base/billing_subscription_guide.pdf"
    ],
    vector_db=vector_db,
)

def create_rag_solution_agent(user: str = "support_agent"):
    """Create RAG-powered solution developer agent"""
    
    agent = Agent(
        user_id=user,
        knowledge=knowledge_base,
        search_knowledge=True,
        show_tool_calls=True,
        instructions="""
        You are a RAG-powered Solution Developer Agent for customer support.
        
        Your capabilities:
        1. Access customer support knowledge base for accurate solutions
        2. Provide step-by-step troubleshooting guides
        3. Reference official documentation and best practices
        4. Offer multiple solution approaches
        5. Include relevant links and resources
        
        Knowledge Base Contents:
        - Customer Support Guide: General support procedures and best practices
        - Technical Troubleshooting: Advanced technical diagnostics and solutions
        - Billing & Subscription: Payment, subscription, and billing issues
        
        Always:
        - Base your solutions on the knowledge base
        - Provide actionable, numbered steps
        - Include verification steps
        - Suggest alternatives if available
        - Reference specific documentation when possible
        - Use the most relevant knowledge base section for the query
        """,
    )
    
    return agent

def interactive_rag_agent(user: str = "support_agent"):
    """Interactive RAG agent for testing customer support queries"""
    
    agent = create_rag_solution_agent(user)
    
    console.print(Panel.fit(
        "[bold blue]🤖 RAG-Powered Solution Developer Agent[/bold blue]\n"
        "[dim]Customer Support Knowledge Base Ready[/dim]\n\n"
        "[yellow]Available Knowledge:[/yellow]\n"
        "• Customer Support Guide\n"
        "• Technical Troubleshooting\n"
        "• Billing & Subscription",
        title="Customer Support RAG Agent",
        border_style="blue"
    ))
    
    while True:
        message = Prompt.ask(f"[bold] :sunglasses: {user} [/bold]")
        if message.lower() in ("exit", "bye", "quit"):
            console.print("[yellow]Goodbye! 👋[/yellow]")
            break
            
        try:
            # Get response from RAG agent
            response = agent.run(message)
            console.print(Panel(
                Text(response.content, style="green"),
                title="🤖 AI Solution",
                border_style="green"
            ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

def get_rag_solution(query: str, user: str = "support_agent") -> str:
    """Get RAG-powered solution for a customer support query"""
    
    agent = create_rag_solution_agent(user)
    
    try:
        response = agent.run(query)
        return response.content
    except Exception as e:
        return f"Error generating solution: {e}"

def check_knowledge_base():
    """Check if knowledge base PDFs exist"""
    pdf_files = [
        "knowledge_base/customer_support_guide.pdf",
        "knowledge_base/technical_troubleshooting_guide.pdf",
        "knowledge_base/billing_subscription_guide.pdf"
    ]
    
    missing_files = []
    for pdf_file in pdf_files:
        if not os.path.exists(pdf_file):
            missing_files.append(pdf_file)
    
    if missing_files:
        console.print("[red]❌ Missing knowledge base PDFs:[/red]")
        for file in missing_files:
            console.print(f"  - {file}")
        console.print("\n[yellow]Please run: python3 create_pdfs.py[/yellow]")
        return False
    
    console.print("[green]✅ All knowledge base PDFs found![/green]")
    return True

if __name__ == "__main__":
    # Check if knowledge base exists
    if not check_knowledge_base():
        exit(1)
    
    # Load knowledge base
    console.print("[yellow]Loading knowledge base...[/yellow]")
    try:
        knowledge_base.load(recreate=False)
        console.print("[green]Knowledge base loaded! ✅[/green]")
    except Exception as e:
        console.print(f"[red]Error loading knowledge base: {e}[/red]")
        console.print("[yellow]Please ensure PDFs are properly formatted and accessible[/yellow]")
        exit(1)
    
    typer.run(interactive_rag_agent)
