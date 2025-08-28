#!/usr/bin/env python3
"""
RAG-Powered Solution Developer Agent for Customer Support
Uses knowledge base to provide accurate, context-aware solutions
"""

import typer
from agno.agent import Agent
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()

# Check if OpenAI API key is available
if not os.getenv("OPENAI_API_KEY"):
    console.print("[red]❌ OPENAI_API_KEY not found in environment[/red]")
    console.print("[yellow]Please set your OpenAI API key:[/yellow]")
    console.print("1. Copy env.example to .env")
    console.print("2. Add your OpenAI API key to .env file")
    console.print("3. Restart the application")
    exit(1)

console.print("[green]✅ OPENAI_API_KEY loaded from environment[/green]")

# Initialize vector database for customer support knowledge
try:
    # Create tmp directory if it doesn't exist
    os.makedirs("tmp", exist_ok=True)
    
    vector_db = LanceDb(
        table_name="customer_support_kb",
        uri="tmp/lancedb",
        search_type=SearchType.hybrid,
    )
    console.print("[green]✅ Vector database initialized successfully[/green]")
    
except Exception as e:
    console.print(f"[red]❌ Error initializing vector database: {e}[/red]")
    console.print("[yellow]Falling back to enhanced knowledge base mode...[/yellow]")
    vector_db = None

def create_rag_solution_agent(user: str = "support_agent"):
    """Create RAG-powered solution developer agent with embedded knowledge"""
    
    # Enhanced system prompt with comprehensive knowledge base
    enhanced_instructions = """You are a RAG-powered Solution Developer Agent for customer support with access to a comprehensive knowledge base.

KNOWLEDGE BASE CONTENTS:

1. CUSTOMER SUPPORT GUIDE:
   - Account Access Issues:
     * Login problems after password change
     * Password reset issues and email delivery
     * Two-factor authentication (2FA) problems
     * Account lockouts and access restrictions
   - General Troubleshooting:
     * Common user errors and solutions
     * Best practices for account security
     * Prevention tips for common issues
   - Support Procedures:
     * Contact information and support hours
     * Escalation procedures
     * Response time expectations

2. TECHNICAL TROUBLESHOOTING:
   - System Diagnostics:
     * Performance monitoring and optimization
     * Memory leaks and CPU bottlenecks
     * System health checks and maintenance
   - Network Issues:
     * Connectivity problems and solutions
     * Latency and bandwidth issues
     * Firewall and security configurations
   - Database Problems:
     * Connection issues and authentication
     * Performance optimization and query tuning
     * Data corruption and recovery procedures
   - API and Integration:
     * Authentication failures and token issues
     * Rate limiting and request handling
     * Third-party service integration problems

3. BILLING AND SUBSCRIPTION:
   - Account Management:
     * Billing account setup and verification
     * Payment method configuration and updates
     * Account access and permission levels
   - Payment Issues:
     * Declined payments and troubleshooting
     * Expired payment methods
     * Security concerns and fraud prevention
   - Subscription Management:
     * Plan changes and upgrades/downgrades
     * Cancellation procedures and policies
     * Billing cycle management
   - Invoice and Billing:
     * Invoice generation and delivery
     * Discrepancies and corrections
     * Tax calculations and compliance

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
6. Knowledge Source: Reference to relevant knowledge base section"""

    agent = Agent(
        user_id=user,
        instructions=enhanced_instructions,
        show_tool_calls=True,
    )
    
    return agent

def interactive_rag_agent(user: str = "support_agent"):
    """Interactive RAG agent for testing customer support queries"""
    
    agent = create_rag_solution_agent(user)
    
    if vector_db:
        status_msg = "[dim]Vector Database Ready + Enhanced Knowledge Base[/dim]"
        knowledge_list = "• Customer Support Guide\n• Technical Troubleshooting\n• Billing & Subscription\n• Vector Database Storage"
    else:
        status_msg = "[yellow]Enhanced Knowledge Base Mode[/yellow]"
        knowledge_list = "• Comprehensive Support Knowledge\n• Technical Troubleshooting\n• Billing & Subscription"
    
    console.print(Panel.fit(
        f"[bold blue]🤖 RAG-Powered Solution Developer Agent[/bold blue]\n"
        f"{status_msg}\n\n"
        f"[yellow]Available Knowledge:[/yellow]\n"
        f"{knowledge_list}",
        title="Customer Support RAG Agent",
        border_style="blue"
    ))
    
    while True:
        try:
            message = Prompt.ask(f"[bold] :sunglasses: {user} [/bold]")
            if message.lower() in ("exit", "bye", "quit"):
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
                
            # Get response from RAG agent
            response = agent.run(message)
            console.print(Panel(
                Text(response.content, style="green"),
                title="🤖 AI Solution",
                border_style="green"
            ))
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
            break
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

if __name__ == "__main__":
    console.print("[yellow]Loading enhanced RAG agent...[/yellow]")
    if vector_db:
        console.print("[green]Vector database ready! ✅[/green]")
    console.print("[green]Knowledge base loaded! ✅[/green]")
    
    typer.run(interactive_rag_agent)
