# 🚀 Data-Driven AI Agents Setup Guide

## 📋 **What's New**

This version replaces hard-coded AI agent instructions with **configurable, data-driven rules** loaded from YAML files.

## 🔧 **Quick Setup**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Set Up Environment**
```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your OpenAI API key
nano .env
```

### **3. Start the Server**
```bash
python3 fastapi_demo.py
```

## 📁 **Configuration Files**

### **Categories & Business Rules**
- **File**: `config/categories.yaml`
- **Purpose**: Define support categories, keywords, priority weights, SLA requirements
- **Example**: Add new category without code changes

### **Priority Scoring Rules**
- **File**: `config/priority_rules.yaml`
- **Purpose**: Define how query priority is calculated
- **Features**: Scoring algorithms, escalation rules, business logic

## 🎯 **Key Benefits**

| Feature | Before (Hard-Coded) | After (Data-Driven) |
|---------|---------------------|---------------------|
| **Add Categories** | Code change + deploy | Edit YAML + restart |
| **Change Priorities** | Code change + deploy | Edit YAML + restart |
| **Business Rules** | Embedded in code | External configuration |
| **Risk Level** | High (code changes) | Low (config only) |
| **Update Speed** | Days/weeks | Minutes |

## 🔄 **Migration Path**

### **Option 1: Use Both Systems**
- Keep existing `fastapi_demo.py` (hard-coded)
- Add new `configurable_agents.py` alongside
- Gradually migrate categories and rules

### **Option 2: Full Migration**
- Replace existing agents with configurable ones
- Move all business logic to YAML files
- Update workflow to use new agents

## 📊 **Example: Adding New Category**

### **Before (Hard-Coded)**
1. Modify `fastapi_demo.py`
2. Update agent instructions
3. Test locally
4. Deploy to production
5. Risk of breaking existing functionality

### **After (Data-Driven)**
1. Edit `config/categories.yaml`
2. Add new category with metadata
3. Restart service
4. New category immediately available
5. Zero risk to existing functionality

### **Example YAML Addition**
```yaml
api_integration:
  description: "API integration and development issues"
  keywords:
    - "api"
    - "integration"
    - "webhook"
    - "endpoint"
  priority_weight: 0.75
  auto_escalate: true
  sla_hours: 6
  team: "developer_support"
```

## 🧪 **Testing the New System**

### **1. Test Configuration Loading**
```bash
python3 configurable_agents.py
```

### **2. Test with Sample Queries**
```bash
python3 test_workflow.py
```

### **3. Modify Configuration**
- Edit YAML files
- Restart service
- Test new behavior

## 🚨 **Important Notes**

### **Security**
- ✅ `.env` files are automatically ignored by git
- ✅ API keys are never checked in
- ✅ Use `env.example` for team setup

### **Performance**
- ⚠️ Slightly slower startup (file loading)
- ✅ Same runtime performance
- ✅ Massive flexibility improvement

### **Maintenance**
- ✅ Business teams can modify rules
- ✅ No developer involvement for config changes
- ✅ Version control for business rules

## 🔍 **Troubleshooting**

### **Common Issues**

#### **1. YAML Syntax Errors**
```bash
# Validate YAML files
python3 -c "import yaml; yaml.safe_load(open('config/categories.yaml'))"
```

#### **2. Configuration Not Loading**
- Check file paths in `configurable_agents.py`
- Ensure YAML files are valid
- Check file permissions

#### **3. Agents Not Responding**
- Verify OpenAI API key is set
- Check agent instructions generation
- Review configuration file structure

## 📚 **Next Steps**

### **Phase 1: Basic Configuration**
- ✅ Set up YAML files
- ✅ Test basic functionality
- ✅ Validate configuration loading

### **Phase 2: Enhanced Features**
- Add dynamic template selection
- Implement A/B testing
- Add configuration validation

### **Phase 3: Advanced Capabilities**
- Real-time configuration updates
- Configuration versioning
- Business rule analytics

## 🎉 **Success Metrics**

- **Business Rule Updates**: 10x faster
- **Risk Reduction**: Near zero for config changes
- **Team Empowerment**: Business teams own support logic
- **Maintenance Overhead**: Significantly reduced

---

**Ready to make your AI agents truly configurable? Start with the categories and priority rules!** 🚀
