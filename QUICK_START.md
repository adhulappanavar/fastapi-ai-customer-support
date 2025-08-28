# 🚀 Quick Start: Agentic Customer Support Workflow

## ✅ **What's Working**

Your AI workflow is **successfully running** and the system is working correctly! The 502 error you're seeing is just because the OpenAI API key needs to be set.

## 🔑 **Set Your OpenAI API Key**

### Option 1: Environment Variable (Recommended)
```bash
export OPENAI_API_KEY="your-actual-openai-api-key-here"
```

### Option 2: In Your Shell Profile
Add to `~/.bashrc`, `~/.zshrc`, or `~/.profile`:
```bash
export OPENAI_API_KEY="your-actual-openai-api-key-here"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

## 🧪 **Test the System**

### 1. **Start the Main API Server** (Terminal 1)
```bash
export OPENAI_API_KEY="your-key-here"
python3 fastapi_demo.py
```

### 2. **Start the Ticketing API Server** (Terminal 2)
```bash
cd ticketing_tool
python3 main.py
```

### 3. **Start the React Frontend** (Terminal 3)
```bash
cd react-web-ui
npm start
```

### 4. **Test with curl**
```bash
curl -X POST "http://localhost:7777/runs?workflow_id=customer-support-resolution-pipeline" \
  -F "workflow_input=I cannot log into my account"
```

### 5. **Test with Python**
```bash
python3 test_workflow.py
```

## 🌐 **System Endpoints**

- **Main API Server**: http://localhost:7777
- **Ticketing API Server**: http://localhost:8000
- **React Frontend**: http://localhost:3000
- **Interactive Docs**: http://localhost:7777/docs
- **Ticketing Docs**: http://localhost:8000/docs
- **Workflow Execution**: `POST /runs?workflow_id=customer-support-resolution-pipeline`

## 🎯 **What Happens When You Submit a Query**

1. **Query Received** → Workflow engine processes it
2. **Ticket Classifier Agent** → Analyzes and categorizes the issue
3. **Solution Developer Agent** → Generates intelligent solution
4. **Response Returned** → With full analysis and step-by-step solution
5. **Smart Caching** → Similar queries get instant responses

## 🔍 **Troubleshooting**

### **502 Bad Gateway Error**
- ✅ **Good news**: Your workflow is working!
- ❌ **Issue**: OpenAI API key not set
- **Solution**: Set `OPENAI_API_KEY` environment variable

### **Workflow Not Found**
- ✅ **Good news**: Workflow ID is correct
- ❌ **Issue**: Server not running
- **Solution**: Start server with `python3 fastapi_demo.py`

### **Port Issues**
- **Default Port**: 7777 (not 8000)
- **Check**: `curl http://localhost:7777/status`

## 🎉 **Success Indicators**

When everything is working correctly, you'll see:
- ✅ Server starts without errors
- ✅ `curl http://localhost:7777/status` returns `{"status":"available"}`
- ✅ Workflow execution returns a run ID and status
- ✅ AI agents process queries and return intelligent solutions

## 🚀 **Next Steps**

1. **Get your OpenAI API key** from [OpenAI Platform](https://platform.openai.com/)
2. **Set the environment variable**
3. **Restart the server**
4. **Test with real customer support queries**
5. **Watch the AI agents work their magic!**

Your agentic workflow is ready to revolutionize customer support! 🎯
