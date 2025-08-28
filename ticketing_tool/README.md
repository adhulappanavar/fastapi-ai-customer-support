# 🎫 Ticket Management System

A comprehensive, independent ticketing system built with FastAPI and SQLite for customer support operations.

## ✨ Features

### **Core Functionality**
- **Ticket Management**: Create, read, update tickets with full CRUD operations
- **User Management**: Support for customers, agents, and administrators
- **Category System**: Organized ticket categorization with SLA tracking
- **Priority Levels**: Configurable priority system with color coding
- **Status Tracking**: Complete ticket lifecycle management
- **Assignment System**: Route tickets to appropriate support agents

### **Advanced Features**
- **Search & Filtering**: Find tickets by content, status, priority, or category
- **Statistics & Analytics**: Comprehensive reporting and dashboard data
- **Audit Trail**: Complete history of all ticket changes
- **Comment System**: Internal and external communication tracking
- **SLA Management**: Service level agreement monitoring
- **Tag System**: Flexible ticket labeling and organization

### **Technical Features**
- **RESTful API**: Clean, documented API endpoints
- **SQLite Database**: Lightweight, file-based database
- **FastAPI Framework**: Modern, fast Python web framework
- **Pydantic Models**: Data validation and serialization
- **CORS Support**: Cross-origin resource sharing enabled
- **Auto-generated Docs**: Interactive API documentation

## 🏗️ Architecture

### **Database Schema**
```
├── users (customers, agents, admins)
├── categories (ticket types with SLA)
├── priority_levels (urgency levels)
├── statuses (ticket states)
├── tickets (main ticket data)
├── ticket_comments (communication)
└── ticket_history (audit trail)
```

### **API Endpoints**
- **`/tickets`** - Ticket CRUD operations
- **`/categories`** - Category management
- **`/priorities`** - Priority level management
- **`/statuses`** - Status management
- **`/users`** - User management
- **`/stats`** - Analytics and reporting
- **`/search`** - Ticket search functionality
- **`/dashboard`** - Dashboard data aggregation

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
cd ticketing_tool
pip install -r requirements.txt
```

### **2. Start the Server**
```bash
python3 main.py
```

The server will start on `http://localhost:8000` with:
- ✅ Database initialized with sample data
- ✅ API endpoints ready
- ✅ Interactive documentation at `/docs`
- ✅ Alternative docs at `/redoc`

### **3. Test the System**
```bash
python3 test_tickets.py
```

## 📊 Sample Data

The system comes pre-loaded with realistic sample data:

### **Users**
- **Customers**: John Doe, Jane Smith, Bob Wilson
- **Support Agents**: Sarah Johnson, Mike Chen
- **Administrator**: Admin User

### **Categories**
- **Account Access** (4h SLA) - Login and account issues
- **Billing & Payments** (6h SLA) - Payment and subscription
- **Technical Support** (8h SLA) - Bugs and performance
- **Product Features** (12h SLA) - How-to and requests
- **Security Issues** (2h SLA) - Security concerns
- **General Support** (24h SLA) - Other inquiries

### **Priority Levels**
- **Critical** (1h SLA) - System down, security breach
- **High** (4h SLA) - Cannot access account
- **Medium** (8h SLA) - Feature not working
- **Low** (24h SLA) - General questions

### **Sample Tickets**
- Login issues after password change
- Payment declined for subscription
- App crashes on settings page
- 2FA setup assistance
- Suspicious login detection
- Dashboard performance issues
- Missing invoice requests
- Feature requests (dark mode)

## 🔧 API Usage Examples

### **Get All Tickets**
```bash
curl "http://localhost:8000/tickets?limit=10"
```

### **Get Specific Ticket**
```bash
curl "http://localhost:8000/tickets/1"
```

### **Create New Ticket**
```bash
curl -X POST "http://localhost:8000/tickets" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New support request",
    "description": "I need help with my account",
    "user_id": 1,
    "category_id": 1,
    "priority_id": 2,
    "tags": "account,help"
  }'
```

### **Update Ticket**
```bash
curl -X PUT "http://localhost:8000/tickets/1?user_id=4" \
  -H "Content-Type: application/json" \
  -d '{
    "status_id": 2,
    "assigned_to": 4
  }'
```

### **Search Tickets**
```bash
curl "http://localhost:8000/search?query=login&limit=5"
```

### **Get Statistics**
```bash
curl "http://localhost:8000/stats"
```

## 📱 Sample Ticket Data

### **Ticket TKT-001: Login Issues**
```
Title: Cannot log into account after password change
Description: I changed my password yesterday and now I cannot log into my account...
Category: Account Access
Priority: High
Status: Open
User: John Doe
Tags: login,password,account
```

### **Ticket TKT-002: Payment Problems**
```
Title: Payment declined for subscription renewal
Description: My credit card payment was declined when trying to renew...
Category: Billing & Payments
Priority: High
Status: Open
User: Jane Smith
Tags: payment,subscription,billing
```

## 🔍 API Documentation

### **Interactive Documentation**
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### **Endpoint Reference**

#### **Tickets**
- `GET /tickets` - List tickets with filtering
- `GET /tickets/{id}` - Get specific ticket
- `POST /tickets` - Create new ticket
- `PUT /tickets/{id}` - Update ticket

#### **Reference Data**
- `GET /categories` - List all categories
- `GET /priorities` - List priority levels
- `GET /statuses` - List ticket statuses
- `GET /users` - List all users

#### **Analytics**
- `GET /stats` - Ticket statistics
- `GET /dashboard` - Dashboard data
- `GET /search` - Search tickets

## 🎯 Integration Points

### **Future Agno Integration**
The system is designed for easy integration with your Agno workflow:

1. **Ticket Creation**: Automatically create tickets from AI agent interactions
2. **Status Updates**: Update ticket status based on AI resolution
3. **Assignment**: Route tickets to appropriate AI agents or human agents
4. **Escalation**: Escalate complex tickets from AI to human support
5. **Knowledge Base**: Link resolved tickets to knowledge base articles

### **Webhook Support**
- Ticket creation events
- Status change notifications
- Assignment updates
- Resolution confirmations

### **API Extensions**
- Custom field support
- Workflow integration
- External system connectors
- Reporting and analytics

## 🛠️ Development

### **Project Structure**
```
ticketing_tool/
├── main.py              # FastAPI application
├── database.py          # Database operations
├── requirements.txt     # Python dependencies
├── test_tickets.py      # Test script
├── README.md           # This file
└── tickets.db          # SQLite database (auto-created)
```

### **Database Operations**
- **Connection Management**: Automatic connection handling
- **Transaction Support**: ACID compliance for data integrity
- **Indexing**: Performance optimization for queries
- **Backup**: Simple file-based backup system

### **Error Handling**
- **Validation**: Input validation with Pydantic
- **Error Responses**: Consistent error message format
- **Logging**: Comprehensive error logging
- **Graceful Degradation**: System continues operating on errors

## 📈 Performance

### **Optimization Features**
- **Database Indexes**: Fast query performance
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Optimized SQL queries
- **Caching**: Response caching for static data

### **Scalability Considerations**
- **Lightweight**: Minimal resource usage
- **Modular**: Easy to extend and modify
- **Stateless**: API can be load balanced
- **Database**: Can migrate to PostgreSQL/MySQL

## 🔒 Security

### **Current Features**
- **Input Validation**: Pydantic model validation
- **SQL Injection Protection**: Parameterized queries
- **CORS Configuration**: Configurable cross-origin access

### **Production Considerations**
- **Authentication**: JWT or OAuth2 implementation
- **Authorization**: Role-based access control
- **Rate Limiting**: API usage throttling
- **HTTPS**: SSL/TLS encryption
- **Audit Logging**: Comprehensive security logging

## 🚀 Deployment

### **Local Development**
```bash
python3 main.py
```

### **Production Deployment**
```bash
# Using Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t ticketing-system .
docker run -p 8000:8000 ticketing-system
```

### **Environment Variables**
```bash
# Database configuration
DATABASE_URL=sqlite:///tickets.db

# Server configuration
HOST=0.0.0.0
PORT=8000

# Security
CORS_ORIGINS=["http://localhost:3000"]
```

## 🔧 Customization

### **Adding New Fields**
1. Update database schema in `database.py`
2. Modify Pydantic models in `main.py`
3. Update API endpoints as needed

### **Custom Categories**
```python
# Add to database.py
new_categories = [
    ('Custom Category', 'Description', 12),
]
```

### **Custom Statuses**
```python
# Add to database.py
new_statuses = [
    ('Custom Status', 'Description', '#color'),
]
```

## 📚 Resources

### **Documentation**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

### **Testing**
- **Unit Tests**: Pytest framework ready
- **Integration Tests**: API endpoint testing
- **Performance Tests**: Load testing scripts

### **Monitoring**
- **Health Checks**: `/health` endpoint
- **Metrics**: Performance monitoring ready
- **Logging**: Structured logging support

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### **Code Standards**
- **Python**: PEP 8 compliance
- **API**: RESTful design principles
- **Database**: SQL best practices
- **Documentation**: Clear and comprehensive

## 📄 License

This ticketing system is part of the AI Customer Support project and follows the same licensing terms.

---

**Ready to manage your support tickets?** 🎫

Start the server and explore the API documentation to get started!
