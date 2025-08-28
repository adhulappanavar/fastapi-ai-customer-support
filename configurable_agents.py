#!/usr/bin/env python3
"""
Configurable, Data-Driven AI Agents for Customer Support
This version uses configuration files instead of hard-coded instructions
"""

import json
import yaml
from typing import Dict, List, Any
from agno.agent import Agent
from agno.models.openai.chat import OpenAIChat

# Configuration files
CATEGORIES_CONFIG = "config/categories.yaml"
PRIORITY_CONFIG = "config/priority_rules.yaml"
TAG_TAXONOMY = "config/tag_taxonomy.yaml"
SOLUTION_TEMPLATES = "config/solution_templates.yaml"

class ConfigurableTicketClassifier:
    """Data-driven ticket classifier that loads rules from configuration"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.categories = self._load_categories()
        self.priority_rules = self._load_priority_rules()
        self.tag_taxonomy = self._load_tag_taxonomy()
        
    def _load_categories(self) -> Dict[str, Dict[str, Any]]:
        """Load category definitions from YAML"""
        try:
            with open(f"{self.config_dir}/categories.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_categories()
    
    def _load_priority_rules(self) -> Dict[str, List[str]]:
        """Load priority scoring rules from YAML"""
        try:
            with open(f"{self.config_dir}/priority_rules.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_priority_rules()
    
    def _load_tag_taxonomy(self) -> Dict[str, List[str]]:
        """Load tag taxonomy from YAML"""
        try:
            with open(f"{self.config_dir}/tag_taxonomy.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_tag_taxonomy()
    
    def _get_default_categories(self) -> Dict[str, Dict[str, Any]]:
        """Default category definitions"""
        return {
            "billing": {
                "description": "Payment, subscription, and billing issues",
                "keywords": ["payment", "billing", "subscription", "charge", "refund", "invoice"],
                "priority_weight": 0.8,
                "auto_escalate": True
            },
            "technical": {
                "description": "System errors, crashes, and technical problems",
                "keywords": ["error", "crash", "bug", "broken", "not working", "issue"],
                "priority_weight": 0.9,
                "auto_escalate": True
            },
            "account_access": {
                "description": "Login, authentication, and account access issues",
                "keywords": ["login", "password", "authentication", "access", "locked", "2fa"],
                "priority_weight": 0.85,
                "auto_escalate": True
            },
            "product_info": {
                "description": "How-to questions and feature information",
                "keywords": ["how to", "feature", "setup", "configure", "guide", "help"],
                "priority_weight": 0.4,
                "auto_escalate": False
            },
            "bug_report": {
                "description": "Specific bug reports and unexpected behavior",
                "keywords": ["bug", "unexpected", "wrong", "incorrect", "problem", "issue"],
                "priority_weight": 0.7,
                "auto_escalate": False
            },
            "feature_request": {
                "description": "Requests for new features or improvements",
                "keywords": ["request", "feature", "improvement", "enhancement", "new", "add"],
                "priority_weight": 0.3,
                "auto_escalate": False
            }
        }
    
    def _get_default_priority_rules(self) -> Dict[str, List[str]]:
        """Default priority scoring rules"""
        return {
            "urgent": [
                "system down", "crash", "broken", "urgent", "asap", "emergency",
                "cannot access", "data loss", "security breach", "payment failed"
            ],
            "high": [
                "cannot login", "billing error", "subscription issue", "important",
                "blocked", "locked out", "critical", "major issue"
            ],
            "medium": [
                "help needed", "question", "setup", "configuration", "how to",
                "feature request", "improvement", "suggestion"
            ],
            "low": [
                "information", "general", "curiosity", "learning", "documentation",
                "tutorial", "guide", "example"
            ]
        }
    
    def _get_default_tag_taxonomy(self) -> Dict[str, List[str]]:
        """Default tag taxonomy"""
        return {
            "authentication": ["login", "password", "2fa", "mfa", "auth", "security"],
            "billing": ["payment", "subscription", "charge", "refund", "invoice", "billing"],
            "technical": ["error", "crash", "bug", "performance", "system", "technical"],
            "user_interface": ["ui", "ux", "interface", "dashboard", "layout", "design"],
            "data": ["data", "export", "import", "backup", "sync", "storage"],
            "mobile": ["mobile", "app", "ios", "android", "phone", "tablet"]
        }
    
    def generate_agent_instructions(self) -> str:
        """Generate dynamic instructions based on configuration"""
        categories_text = "\n".join([
            f"- {cat}: {details['description']}" 
            for cat, details in self.categories.items()
        ])
        
        priority_text = "\n".join([
            f"- {level}: {', '.join(rules)}" 
            for level, rules in self.priority_rules.items()
        ])
        
        return f"""
        You are a data-driven customer support ticket classifier. Use the following configuration:

        AVAILABLE CATEGORIES:
        {categories_text}

        PRIORITY INDICATORS:
        {priority_text}

        TASK: For each customer query, provide:
        1. Category (select from available categories above)
        2. Priority (urgent/high/medium/low based on indicators)
        3. Key tags (extract 3-5 relevant terms)
        4. Brief summary of the issue
        5. Confidence score (0-100%)

        Format your response as:
        Category: [category]
        Priority: [priority]
        Tags: [tag1, tag2, tag3]
        Summary: [brief summary]
        Confidence: [score]%
        """

class ConfigurableSolutionDeveloper:
    """Data-driven solution developer that uses templates and rules"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.solution_templates = self._load_solution_templates()
        self.response_styles = self._load_response_styles()
    
    def _load_solution_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load solution templates from YAML"""
        try:
            with open(f"{self.config_dir}/solution_templates.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_templates()
    
    def _load_response_styles(self) -> Dict[str, str]:
        """Load response style configurations"""
        try:
            with open(f"{self.config_dir}/response_styles.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_styles()
    
    def _get_default_templates(self) -> Dict[str, Dict[str, Any]]:
        """Default solution templates"""
        return {
            "troubleshooting": {
                "structure": [
                    "Problem Diagnosis",
                    "Step-by-Step Solution",
                    "Alternative Approaches",
                    "Prevention Tips"
                ],
                "tone": "helpful and patient",
                "include_verification": True
            },
            "how_to": {
                "structure": [
                    "Overview",
                    "Prerequisites",
                    "Step-by-Step Instructions",
                    "Verification",
                    "Troubleshooting"
                ],
                "tone": "clear and encouraging",
                "include_verification": True
            },
            "billing": {
                "structure": [
                    "Issue Confirmation",
                    "Verification Steps",
                    "Resolution Process",
                    "Prevention Measures"
                ],
                "tone": "professional and reassuring",
                "include_verification": True
            },
            "bug_report": {
                "structure": [
                    "Problem Description",
                    "Steps to Reproduce",
                    "Expected vs Actual Behavior",
                    "Temporary Workarounds",
                    "Escalation Path"
                ],
                "tone": "analytical and helpful",
                "include_verification": False
            }
        }
    
    def _get_default_styles(self) -> Dict[str, str]:
        """Default response styles"""
        return {
            "professional": "Use formal language, clear structure, and professional tone",
            "friendly": "Use warm, encouraging language with personal touches",
            "technical": "Use precise technical language with detailed explanations",
            "simple": "Use basic language, avoid jargon, focus on clarity"
        }
    
    def generate_agent_instructions(self) -> str:
        """Generate dynamic instructions based on configuration"""
        templates_text = "\n".join([
            f"- {template}: {details['structure']}" 
            for template, details in self.solution_templates.items()
        ])
        
        styles_text = "\n".join([
            f"- {style}: {description}" 
            for style, description in self.response_styles.items()
        ])
        
        return f"""
        You are a data-driven solution developer for customer support. Use the following configuration:

        SOLUTION TEMPLATES:
        {templates_text}

        RESPONSE STYLES:
        {styles_text}

        TASK: Based on the query classification, generate a comprehensive solution using:
        1. Appropriate template structure
        2. Suitable response style
        3. Clear, actionable steps
        4. Alternative approaches
        5. Prevention tips

        Always consider:
        - User skill level and technical expertise
        - Problem complexity and urgency
        - Available resources and tools
        - Customer experience and satisfaction
        """

def create_configurable_agents():
    """Create agents with dynamic, data-driven instructions"""
    
    # Initialize configurable components
    classifier_config = ConfigurableTicketClassifier()
    solution_config = ConfigurableSolutionDeveloper()
    
    # Create agents with dynamic instructions
    triage_agent = Agent(
        name="Data-Driven Ticket Classifier",
        model=OpenAIChat(id="gpt-4o"),
        instructions=classifier_config.generate_agent_instructions(),
        markdown=True,
    )
    
    solution_agent = Agent(
        name="Data-Driven Solution Developer",
        model=OpenAIChat(id="gpt-4o"),
        instructions=solution_config.generate_agent_instructions(),
        markdown=True,
    )
    
    return triage_agent, solution_agent

if __name__ == "__main__":
    # Example usage
    triage_agent, solution_agent = create_configurable_agents()
    print("✅ Configurable agents created successfully!")
    print("📁 Configuration files can be modified without code changes")
    print("🔄 Agents will automatically adapt to new rules and templates")
