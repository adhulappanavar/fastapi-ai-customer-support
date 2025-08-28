#!/bin/bash

echo "🚀 Setting up Agentic Customer Support Workflow Environment"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY environment variable is not set."
    echo "Please set it with: export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    read -p "Enter your OpenAI API key: " api_key
    if [ ! -z "$api_key" ]; then
        export OPENAI_API_KEY="$api_key"
        echo "✅ OPENAI_API_KEY set for this session"
        echo "💡 To make it permanent, add to your ~/.bashrc or ~/.zshrc:"
        echo "   export OPENAI_API_KEY='$api_key'"
    else
        echo "❌ No API key provided. The AI agents won't work without it."
        exit 1
    fi
else
    echo "✅ OPENAI_API_KEY is set"
fi

# Create tmp directory for agent storage
mkdir -p tmp
echo "✅ Created tmp directory for agent storage"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "To start the AI workflow:"
echo "  python3 fastapi_demo.py"
echo ""
echo "To test the workflow:"
echo "  python3 test_workflow.py"
echo ""
echo "API will be available at: http://localhost:7777"
echo "Interactive docs at: http://localhost:7777/docs"
