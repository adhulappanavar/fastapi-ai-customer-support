# 🌐 AI Customer Support Web UI

A modern, responsive web interface for your RAG-powered AI customer support system.

## ✨ Features

- **Modern Design**: Sleek, professional interface with glassmorphism effects
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Real-time Chat**: Interactive chat interface with your AI agents
- **API Integration**: Connects directly to your FastAPI backend
- **Smart Formatting**: Automatically formats AI responses with proper styling
- **Quick Start Examples**: Pre-built example queries to get started
- **Status Monitoring**: Real-time API connection status
- **Keyboard Shortcuts**: Enhanced user experience with keyboard navigation

## 🚀 Quick Start

1. **Ensure your FastAPI server is running** on `http://localhost:7777`
2. **Open `index.html`** in your web browser
3. **Click on example queries** or type your own support question
4. **Start chatting** with your RAG-powered AI agent!

## 🎨 Design Features

### Visual Elements
- **Gradient Background**: Beautiful purple-blue gradient theme
- **Glassmorphism**: Translucent cards with backdrop blur effects
- **Smooth Animations**: Fade-in effects and hover animations
- **Icon Integration**: Font Awesome icons throughout the interface
- **Typography**: Clean Inter font for excellent readability

### Interactive Components
- **Welcome Screen**: Feature showcase with quick start examples
- **Chat Interface**: Professional chat layout with user/AI message distinction
- **Sidebar**: Support categories, agent status, and knowledge base info
- **Status Indicators**: Real-time connection status with visual feedback

## 🔧 Technical Details

### Frontend Technologies
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with flexbox, grid, and animations
- **JavaScript ES6+**: Class-based architecture with async/await
- **Responsive Design**: Mobile-first approach with breakpoints

### API Integration
- **Endpoint**: `/runs?workflow_id=rag-customer-support-resolution-pipeline`
- **Method**: POST with FormData
- **Format**: `workflow_input` field containing user query
- **Response**: JSON with `content` field containing AI solution

### Browser Compatibility
- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile Browsers**: iOS Safari, Chrome Mobile, Samsung Internet
- **Features**: ES6 modules, CSS Grid, Flexbox, Backdrop Filter

## 📱 Responsive Breakpoints

- **Desktop**: 1024px and above
- **Tablet**: 768px - 1023px
- **Mobile**: 480px - 767px
- **Small Mobile**: Below 480px

## ⌨️ Keyboard Shortcuts

- **Enter**: Send message (in chat input)
- **Ctrl/Cmd + Enter**: Force send message
- **Escape**: Return to welcome screen (from chat)

## 🎯 Usage Examples

### Example Queries
The interface includes pre-built example queries:
- **Login Issues**: "I can't log into my account after changing my password"
- **Payment Problems**: "My payment was declined when trying to renew my subscription"
- **Performance Issues**: "My app is running very slowly and keeps crashing"

### Custom Queries
Users can type any customer support question:
- Technical troubleshooting
- Account access issues
- Billing and subscription questions
- General support inquiries

## 🔌 API Configuration

### Backend Requirements
- **FastAPI Server**: Running on port 7777
- **Workflow ID**: `rag-customer-support-resolution-pipeline`
- **CORS**: Enabled for local development
- **Status Endpoint**: `/status` for health checks

### Environment Setup
```bash
# Start your FastAPI server
python3 fastapi_demo.py

# Open the web UI
open webui/index.html
```

## 🎨 Customization

### Colors
The UI uses a consistent color scheme:
- **Primary**: #667eea (Blue)
- **Secondary**: #764ba2 (Purple)
- **Success**: #48bb78 (Green)
- **Error**: #f56565 (Red)
- **Text**: #2d3748 (Dark Gray)

### Styling
- **CSS Variables**: Easy color customization
- **Component Classes**: Modular styling approach
- **Responsive Mixins**: Consistent breakpoint handling

## 🚀 Deployment

### Local Development
1. Clone the repository
2. Start your FastAPI server
3. Open `webui/index.html` in a browser

### Production Deployment
1. **Web Server**: Deploy to Apache, Nginx, or CDN
2. **HTTPS**: Enable SSL for secure connections
3. **CORS**: Configure for your production domain
4. **API URL**: Update `apiBaseUrl` in `script.js`

### Docker (Optional)
```dockerfile
FROM nginx:alpine
COPY webui/ /usr/share/nginx/html/
EXPOSE 80
```

## 🔍 Troubleshooting

### Common Issues
- **API Connection Failed**: Check if FastAPI server is running
- **CORS Errors**: Ensure backend allows frontend domain
- **Styling Issues**: Check browser compatibility
- **Responsive Problems**: Test on different screen sizes

### Debug Mode
Open browser console to see:
- API connection status
- Request/response logs
- JavaScript errors
- Performance metrics

## 📈 Performance

### Optimization Features
- **Lazy Loading**: Components load as needed
- **Efficient Rendering**: Minimal DOM manipulation
- **Smooth Animations**: 60fps animations with CSS transforms
- **Responsive Images**: Optimized for different screen densities

### Loading Times
- **Initial Load**: <500ms on modern devices
- **Chat Response**: Depends on AI processing time
- **Page Transitions**: <200ms with smooth animations

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test across different browsers
5. Submit a pull request

### Code Style
- **HTML**: Semantic markup with accessibility
- **CSS**: BEM methodology for class naming
- **JavaScript**: ES6+ with async/await patterns

## 📄 License

This web UI is part of the AI Customer Support project and follows the same licensing terms.

---

**Ready to provide amazing customer support?** 🚀

Open `index.html` and start chatting with your AI agents!
