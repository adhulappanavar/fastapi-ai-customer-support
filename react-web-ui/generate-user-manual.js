const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function generateUserManual() {
  console.log('🚀 Starting User Manual Generation...');
  
  // Create screenshots directory
  const screenshotsDir = path.join(__dirname, 'screenshots');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir);
  }

  const browser = await chromium.launch({ 
    headless: false, // Set to true for production
    slowMo: 1000 // Slow down for better screenshots
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    deviceScaleFactor: 2 // Higher quality screenshots
  });
  
  const page = await context.newPage();
  
  try {
    // Navigate to the React app
    console.log('📱 Loading React App...');
    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');
    
    // Wait for the app to fully load
    await page.waitForTimeout(2000);
    
    // 1. HOME TAB SCREENSHOT
    console.log('🏠 Capturing Home Tab...');
    await page.click('text=HOME');
    await page.waitForTimeout(1000);
    await page.screenshot({ 
      path: path.join(screenshotsDir, '01-home-tab.png'),
      fullPage: true 
    });
    
    // 2. AI CHAT TAB SCREENSHOT
    console.log('💬 Capturing AI Chat Tab...');
    await page.click('text=AI CHAT');
    await page.waitForTimeout(1000);
    
    // Try to find and interact with the input field
    try {
      // Wait for the input field to be available
      await page.waitForSelector('input', { timeout: 10000 });
      
      // Try multiple selectors for the input field
      const inputField = await page.$('input[placeholder*="Type your message here"]') ||
                        await page.$('input[placeholder*="message"]') ||
                        await page.$('input[type="text"]') ||
                        await page.$('textarea');
      
      if (inputField) {
        await inputField.fill('I cannot log into my account');
        
        // Try to find and click the send button
        const sendButton = await page.$('button:has-text("Send")') ||
                          await page.$('button[title*="Send"]') ||
                          await page.$('button svg'); // Look for button with icon
        
        if (sendButton) {
          await sendButton.click();
          await page.waitForTimeout(2000);
        }
      }
    } catch (error) {
      console.log('⚠️ Could not interact with chat input, taking screenshot anyway');
    }
    
    await page.screenshot({ 
      path: path.join(screenshotsDir, '02-ai-chat-tab.png'),
      fullPage: true 
    });
    
    // 3. TICKETS TAB SCREENSHOT
    console.log('🎫 Capturing Tickets Tab...');
    await page.click('text=TICKETS');
    await page.waitForTimeout(1000);
    
    // Wait for tickets to load
    await page.waitForSelector('table', { timeout: 10000 });
    await page.waitForTimeout(1000);
    
    await page.screenshot({ 
      path: path.join(screenshotsDir, '03-tickets-tab.png'),
      fullPage: true 
    });
    
    // 4. TICKET WITH AI RESOLUTION SCREENSHOT
    console.log('🤖 Capturing AI Resolution Feature...');
    
    // Try to find and click AI Resolution button for first ticket
    try {
      const aiButtons = await page.$$('button[title*="AI"]');
      if (aiButtons.length > 0) {
        await aiButtons[0].click();
        await page.waitForTimeout(3000); // Wait for AI response
        
        await page.screenshot({ 
          path: path.join(screenshotsDir, '04-ai-resolution-feature.png'),
          fullPage: true 
        });
      } else {
        console.log('⚠️ AI Resolution button not found, skipping this screenshot');
        // Take a screenshot anyway to show the tickets tab
        await page.screenshot({ 
          path: path.join(screenshotsDir, '04-ai-resolution-feature.png'),
          fullPage: true 
        });
      }
    } catch (error) {
      console.log('⚠️ Error capturing AI Resolution, taking fallback screenshot');
      await page.screenshot({ 
        path: path.join(screenshotsDir, '04-ai-resolution-feature.png'),
        fullPage: true 
      });
    }
    
    // 5. KNOWLEDGE BASE TAB SCREENSHOT
    console.log('📚 Capturing Knowledge Base Tab...');
    await page.click('text=KNOWLEDGE BASE');
    await page.waitForTimeout(1000);
    
    await page.screenshot({ 
      path: path.join(screenshotsDir, '05-knowledge-base-tab.png'),
      fullPage: true 
    });
    
    // 6. KNOWLEDGE BASE UPLOAD SCREENSHOT
    console.log('📤 Capturing Knowledge Base Upload...');
    
    // Try to click upload button if available
    try {
      const uploadButtons = await page.$$('button:has-text("Upload")');
      if (uploadButtons.length > 0) {
        await uploadButtons[0].click();
        await page.waitForTimeout(1000);
      }
    } catch (error) {
      console.log('⚠️ Could not click upload button, taking screenshot anyway');
    }
    
    await page.screenshot({ 
      path: path.join(screenshotsDir, '06-knowledge-base-upload.png'),
      fullPage: true 
    });
    
    // 7. KNOWLEDGE BASE BUILD SCREENSHOT
    console.log('🔨 Capturing Knowledge Base Build...');
    
    // Try to click build button if available
    try {
      const buildButtons = await page.$$('button:has-text("Build")');
      if (buildButtons.length > 0) {
        await buildButtons[0].click();
        await page.waitForTimeout(2000);
      }
    } catch (error) {
      console.log('⚠️ Could not click build button, taking screenshot anyway');
    }
    
    await page.screenshot({ 
      path: path.join(screenshotsDir, '07-knowledge-base-build.png'),
      fullPage: true 
    });
    
    // 8. RESPONSIVE DESIGN SCREENSHOT
    console.log('📱 Capturing Responsive Design...');
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(1000);
    
    await page.screenshot({ 
      path: path.join(screenshotsDir, '08-responsive-mobile.png'),
      fullPage: true 
    });
    
    // Reset viewport
    await page.setViewportSize({ width: 1280, height: 720 });
    
    console.log('✅ All screenshots captured successfully!');
    
    // Generate the user manual
    await generateMarkdownManual(screenshotsDir);
    
  } catch (error) {
    console.error('❌ Error during screenshot capture:', error);
  } finally {
    await browser.close();
  }
}

async function generateMarkdownManual(screenshotsDir) {
  console.log('📝 Generating User Manual...');
  
  const manual = `# 🤖 AI Customer Support System - User Manual

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [Home Tab](#home-tab)
4. [AI Chat Tab](#ai-chat-tab)
5. [Tickets Tab](#tickets-tab)
6. [Knowledge Base Tab](#knowledge-base-tab)
7. [AI Resolution Feature](#ai-resolution-feature)
8. [Responsive Design](#responsive-design)
9. [Troubleshooting](#troubleshooting)

## 🎯 System Overview

The AI Customer Support System is a comprehensive solution that combines:
- **React-based Web Interface** for intuitive user experience
- **AI-powered Chat Support** using OpenAI GPT models
- **Ticket Management System** with SQLite database
- **Knowledge Base Management** with vector database integration
- **AI Resolution Generation** for automatic ticket solutions

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ installed
- Python 3.8+ installed
- OpenAI API key configured

### Installation
\`\`\`bash
# Install React dependencies
cd react-web-ui
npm install

# Install Python dependencies
pip install -r requirements.txt
\`\`\`

### Starting the System
\`\`\`bash
# Terminal 1: Start FastAPI Backend
python3 fastapi_demo.py

# Terminal 2: Start Ticketing API
cd ticketing_tool
python3 main.py

# Terminal 3: Start React Frontend
cd react-web-ui
npm start
\`\`\`

## 🏠 Home Tab

The Home tab provides an overview of the system and quick access to key features.

![Home Tab](${path.relative(process.cwd(), path.join(screenshotsDir, '01-home-tab.png'))})

**Features:**
- System overview and welcome message
- Quick navigation to all tabs
- System status information

## 💬 AI Chat Tab

The AI Chat tab allows users to interact directly with the AI support system.

![AI Chat Tab](${path.relative(process.cwd(), path.join(screenshotsDir, '02-ai-chat-tab.png'))})

**How to Use:**
1. Type your support query in the input field
2. Click "Send" or press Enter
3. The AI will analyze your query and provide a comprehensive solution
4. Responses include step-by-step instructions and troubleshooting tips

**Example Queries:**
- "I cannot log into my account"
- "My payment was charged twice"
- "The system is running very slow"
- "How do I reset my password?"

## 🎫 Tickets Tab

The Tickets tab provides comprehensive ticket management capabilities.

![Tickets Tab](${path.relative(process.cwd(), path.join(screenshotsDir, '03-tickets-tab.png'))})

**Features:**
- **Search & Filter**: Find tickets by status, priority, or category
- **Ticket List**: View all tickets with key information
- **Ticket Details**: Click the eye icon to view full ticket information
- **AI Resolution**: Get AI-generated solutions for each ticket

**Ticket Information Displayed:**
- Ticket number and title
- User information
- Category and priority
- Status and creation date
- Action buttons

## 🤖 AI Resolution Feature

The AI Resolution feature automatically generates comprehensive solutions for support tickets.

![AI Resolution Feature](${path.relative(process.cwd(), path.join(screenshotsDir, '04-ai-resolution-feature.png'))})

**How to Use:**
1. Navigate to the Tickets tab
2. Locate the ticket you want to resolve
3. Click the robot icon (🤖) in the Actions column
4. Wait for the AI to generate a solution
5. View the detailed resolution below the ticket

**AI Resolution Includes:**
- Step-by-step troubleshooting
- Prevention tips
- Alternative solutions
- Related documentation links

## 📚 Knowledge Base Tab

The Knowledge Base tab allows administrators to manage the system's knowledge base.

![Knowledge Base Tab](${path.relative(process.cwd(), path.join(screenshotsDir, '05-knowledge-base-tab.png'))})

**Features:**
- **PDF Management**: Upload and manage PDF documents
- **Knowledge Building**: Build vector database from uploaded documents
- **Statistics**: View vector database statistics
- **Document List**: Browse all uploaded knowledge base documents

### Uploading PDFs
![Knowledge Base Upload](${path.relative(process.cwd(), path.join(screenshotsDir, '06-knowledge-base-upload.png'))})

**Steps:**
1. Click "Choose File" to select a PDF
2. Ensure the PDF contains relevant support information
3. Click "Upload PDF" to add it to the system
4. The PDF will appear in the documents list

### Building Knowledge Base
![Knowledge Base Build](${path.relative(process.cwd(), path.join(screenshotsDir, '07-knowledge-base-build.png'))})

**Steps:**
1. Upload all necessary PDF documents
2. Click "Build Knowledge Base" to process documents
3. Wait for the vector database to be updated
4. View statistics to confirm successful processing

## 📱 Responsive Design

The system is designed to work seamlessly across all device sizes.

![Responsive Mobile](${path.relative(process.cwd(), path.join(screenshotsDir, '08-responsive-mobile.png'))})

**Responsive Features:**
- **Desktop**: Full-featured interface with side-by-side layouts
- **Tablet**: Optimized layouts for medium screens
- **Mobile**: Touch-friendly interface with stacked layouts
- **Cross-platform**: Works on Windows, macOS, Linux, iOS, and Android

## 🔧 Troubleshooting

### Common Issues and Solutions

#### AI Chat Not Responding
- **Check**: FastAPI backend is running on port 7777
- **Solution**: Ensure \`python3 fastapi_demo.py\` is running
- **Verify**: Check console for error messages

#### Tickets Not Loading
- **Check**: Ticketing API is running on port 8000
- **Solution**: Ensure \`python3 main.py\` is running in ticketing_tool directory
- **Verify**: Check browser console for API errors

#### Knowledge Base Build Failing
- **Check**: OpenAI API key is configured
- **Solution**: Verify \`.env\` file contains valid \`OPENAI_API_KEY\`
- **Verify**: Check API quota and limits

#### React App Not Starting
- **Check**: Node.js version (requires 16+)
- **Solution**: Run \`npm install\` to install dependencies
- **Verify**: Check for port conflicts on 3000

### System Requirements

- **Frontend**: Node.js 16+, npm 8+
- **Backend**: Python 3.8+, pip 20+
- **Database**: SQLite 3.0+ (included with Python)
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### Performance Optimization

- **Vector Database**: Use SSD storage for better performance
- **API Caching**: Enable Redis for production deployments
- **Image Optimization**: Compress screenshots for faster loading
- **CDN**: Use CDN for static assets in production

## 📞 Support

For technical support or feature requests:
- **GitHub Issues**: Create an issue in the repository
- **Documentation**: Check the README.md for detailed setup instructions
- **API Docs**: Visit http://localhost:7777/docs for interactive API documentation

---

*This user manual was automatically generated using Playwright automation. Last updated: ${new Date().toLocaleDateString()}*
`;

  const manualPath = path.join(__dirname, 'USER_MANUAL.md');
  fs.writeFileSync(manualPath, manual);
  
  console.log(`✅ User manual generated: ${manualPath}`);
  console.log(`📸 Screenshots saved in: ${screenshotsDir}`);
  console.log('\n🎉 User Manual Generation Complete!');
}

// Run the automation
generateUserManual().catch(console.error);
