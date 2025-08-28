# 🤖 User Manual Automation Script

This directory contains an automated Playwright script that captures screenshots of your AI Customer Support System and generates a comprehensive user manual.

## 🚀 Quick Start

### Prerequisites
- React app running on `http://localhost:3000`
- FastAPI backend running on `http://localhost:7777` (for AI features)
- Ticketing API running on `http://localhost:8000` (for ticket data)

### Generate User Manual
```bash
npm run generate-manual
```

## 📸 What Gets Captured

The automation script will capture screenshots of:

1. **Home Tab** - System overview and navigation
2. **AI Chat Tab** - AI support interface with sample query
3. **Tickets Tab** - Ticket management interface
4. **AI Resolution Feature** - AI-generated ticket solutions
5. **Knowledge Base Tab** - Knowledge base management
6. **Knowledge Base Upload** - PDF upload interface
7. **Knowledge Base Build** - Vector database building process
8. **Responsive Design** - Mobile/tablet view

## 🎯 Output Files

After running the script, you'll get:

- **`screenshots/`** directory with all captured images
- **`USER_MANUAL.md`** - Complete user manual in Markdown format
- **High-quality screenshots** with 2x device scale factor

## ⚙️ Configuration

### Viewport Settings
- **Desktop**: 1280x720 pixels
- **Mobile**: 768x1024 pixels
- **Quality**: 2x device scale factor for crisp screenshots

### Timing
- **Page Load**: Waits for network idle state
- **Animations**: 1-3 second delays for smooth captures
- **AI Responses**: Extended waits for AI processing

## 🔧 Customization

### Modify Screenshot Selection
Edit `generate-user-manual.js` to:
- Change viewport sizes
- Adjust timing delays
- Add new screenshot locations
- Modify image quality settings

### Customize User Manual
The script generates a comprehensive manual including:
- System overview
- Feature descriptions
- Troubleshooting guides
- Performance optimization tips

## 🐛 Troubleshooting

### Common Issues

#### "Page not found" Error
- Ensure React app is running on port 3000
- Check that all services are started

#### Screenshots Not Capturing
- Verify browser automation is working
- Check file permissions for screenshots directory
- Ensure viewport settings are valid

#### AI Features Not Working
- Verify FastAPI backend is running
- Check OpenAI API key configuration
- Ensure workflow IDs are correct

### Debug Mode
Set `headless: false` in the script to see the browser automation in action.

## 📚 Generated Manual Features

The automated user manual includes:

- **Interactive Table of Contents**
- **Screenshot Integration** with proper paths
- **Step-by-step Instructions** for each feature
- **Troubleshooting Section** with common issues
- **System Requirements** and optimization tips
- **Responsive Design** documentation

## 🎉 Benefits

- **Time Saving**: Automated screenshot capture
- **Consistency**: Standardized image quality and format
- **Comprehensive**: Covers all system features
- **Professional**: Ready-to-use documentation
- **Maintainable**: Easy to update and regenerate

## 📞 Support

For issues with the automation script:
- Check Playwright documentation
- Verify all dependencies are installed
- Ensure target applications are running
- Review console output for error messages

---

*This automation script uses Playwright for reliable cross-browser automation and high-quality screenshot capture.*
