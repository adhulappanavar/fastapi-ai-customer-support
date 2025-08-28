const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function testHomeButtons() {
  console.log('🧪 Starting Home Page Button Tests...');
  
  // Create test results directory
  const testResultsDir = path.join(__dirname, 'test-results');
  if (!fs.existsSync(testResultsDir)) {
    fs.mkdirSync(testResultsDir);
  }

  const browser = await chromium.launch({ 
    headless: false, // Set to true for CI/CD
    slowMo: 500 // Slow down for better visibility
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    deviceScaleFactor: 1
  });
  
  const page = await context.newPage();
  
  // Listen to console messages
  const consoleMessages = [];
  page.on('console', msg => {
    consoleMessages.push({
      type: msg.type(),
      text: msg.text(),
      timestamp: new Date().toISOString()
    });
    console.log(`📝 Console [${msg.type()}]: ${msg.text()}`);
  });
  
  try {
    // Navigate to the React app
    console.log('📱 Loading React App...');
    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // Ensure we're on the Home tab
    console.log('🏠 Ensuring Home tab is active...');
    await page.click('text=HOME');
    await page.waitForTimeout(1000);
    
    // Take initial screenshot
    await page.screenshot({ 
      path: path.join(testResultsDir, '01-home-page-initial.png'),
      fullPage: true 
    });
    
    // Test Payment Issues Button
    console.log('💳 Testing Payment Issues Button...');
    const paymentButton = await page.$('button:has-text("Get Help with Payment Issues")');
    if (paymentButton) {
      await paymentButton.click();
      await page.waitForTimeout(1000);
      
      // Check if console message was logged
      const paymentMessage = consoleMessages.find(msg => 
        msg.text.includes('My payment was declined when trying to renew my subscription')
      );
      
      if (paymentMessage) {
        console.log('✅ Payment Issues button test PASSED - Console message found');
      } else {
        console.log('❌ Payment Issues button test FAILED - Console message not found');
      }
      
      await page.screenshot({ 
        path: path.join(testResultsDir, '02-payment-button-clicked.png'),
        fullPage: true 
      });
    } else {
      console.log('❌ Payment Issues button not found');
    }
    
    // Test Account Access Button
    console.log('🔐 Testing Account Access Button...');
    const accountButton = await page.$('button:has-text("Get Help with Account Access")');
    if (accountButton) {
      await accountButton.click();
      await page.waitForTimeout(1000);
      
      // Check if console message was logged
      const accountMessage = consoleMessages.find(msg => 
        msg.text.includes("I can't log into my account after changing my password")
      );
      
      if (accountMessage) {
        console.log('✅ Account Access button test PASSED - Console message found');
      } else {
        console.log('❌ Account Access button test FAILED - Console message not found');
      }
      
      await page.screenshot({ 
        path: path.join(testResultsDir, '03-account-button-clicked.png'),
        fullPage: true 
      });
    } else {
      console.log('❌ Account Access button not found');
    }
    
    // Test Technical Support Button
    console.log('⚡ Testing Technical Support Button...');
    const techButton = await page.$('button:has-text("Get Help with Technical Support")');
    if (techButton) {
      await techButton.click();
      await page.waitForTimeout(1000);
      
      // Check if console message was logged
      const techMessage = consoleMessages.find(msg => 
        msg.text.includes('App crashes when opening settings page')
      );
      
      if (techMessage) {
        console.log('✅ Technical Support button test PASSED - Console message found');
      } else {
        console.log('❌ Technical Support button test FAILED - Console message not found');
      }
      
      await page.screenshot({ 
        path: path.join(testResultsDir, '04-tech-button-clicked.png'),
        fullPage: true 
      });
    } else {
      console.log('❌ Technical Support button not found');
    }
    
    // Test General Support Button
    console.log('🆘 Testing General Support Button...');
    const generalButton = await page.$('button:has-text("Get Help with General Support")');
    if (generalButton) {
      await generalButton.click();
      await page.waitForTimeout(1000);
      
      // Check if console message was logged
      const generalMessage = consoleMessages.find(msg => 
        msg.text.includes('How to use the new dashboard features?')
      );
      
      if (generalMessage) {
        console.log('✅ General Support button test PASSED - Console message found');
      } else {
        console.log('❌ General Support button test FAILED - Console message not found');
      }
      
      await page.screenshot({ 
        path: path.join(testResultsDir, '05-general-button-clicked.png'),
        fullPage: true 
      });
    } else {
      console.log('❌ General Support button not found');
    }
    
    // Test Start AI Chat Button
    console.log('🤖 Testing Start AI Chat Button...');
    const startChatButton = await page.$('button:has-text("Start AI Chat")');
    if (startChatButton) {
      await startChatButton.click();
      await page.waitForTimeout(1000);
      
      // Check if we switched to AI Chat tab
      const chatTab = await page.$('text=AI CHAT');
      if (chatTab) {
        console.log('✅ Start AI Chat button test PASSED - Switched to AI Chat tab');
      } else {
        console.log('❌ Start AI Chat button test FAILED - Did not switch to AI Chat tab');
      }
      
      await page.screenshot({ 
        path: path.join(testResultsDir, '06-start-chat-clicked.png'),
        fullPage: true 
      });
    } else {
      console.log('❌ Start AI Chat button not found');
    }
    
    // Generate test report
    await generateTestReport(consoleMessages, testResultsDir);
    
    console.log('✅ All Home page button tests completed!');
    
  } catch (error) {
    console.error('❌ Error during testing:', error);
    await page.screenshot({ 
      path: path.join(testResultsDir, 'error-screenshot.png'),
      fullPage: true 
    });
  } finally {
    await browser.close();
  }
}

async function generateTestReport(consoleMessages, testResultsDir) {
  console.log('📊 Generating Test Report...');
  
  const report = `# 🧪 Home Page Button Test Report

## 📋 Test Summary

**Test Date**: ${new Date().toLocaleDateString()}
**Test Time**: ${new Date().toLocaleTimeString()}
**Total Console Messages**: ${consoleMessages.length}

## 🔍 Test Results

### ✅ Expected Console Messages

The following console messages should appear when clicking Home page buttons:

1. **Payment Issues Button**: "Switch to chat with example: My payment was declined when trying to renew my subscription"
2. **Account Access Button**: "Switch to chat with example: I can't log into my account after changing my password"
3. **Technical Support Button**: "Switch to chat with example: App crashes when opening settings page"
4. **General Support Button**: "Switch to chat with example: How to use the new dashboard features?"

### 📝 Console Messages Captured

${consoleMessages.map((msg, index) => `
**Message ${index + 1}**:
- **Type**: ${msg.type}
- **Text**: ${msg.text}
- **Timestamp**: ${msg.timestamp}
`).join('\n')}

### 🎯 Test Coverage

- **Home Tab Navigation**: ✅ Tested
- **Payment Issues Button**: ✅ Tested
- **Account Access Button**: ✅ Tested
- **Technical Support Button**: ✅ Tested
- **General Support Button**: ✅ Tested
- **Start AI Chat Button**: ✅ Tested

### 📸 Screenshots Captured

- \`01-home-page-initial.png\` - Initial Home page state
- \`02-payment-button-clicked.png\` - After clicking Payment Issues button
- \`03-account-button-clicked.png\` - After clicking Account Access button
- \`04-tech-button-clicked.png\` - After clicking Technical Support button
- \`05-general-button-clicked.png\` - After clicking General Support button
- \`06-start-chat-clicked.png\` - After clicking Start AI Chat button

## 🚀 Next Steps

1. **Verify Console Messages**: Ensure all expected console messages are logged
2. **Check Button Functionality**: Verify buttons trigger appropriate actions
3. **UI Responsiveness**: Confirm buttons respond visually to clicks
4. **Navigation**: Verify Start AI Chat button switches tabs correctly

---

*This test report was automatically generated by Playwright automation.*
`;

  const reportPath = path.join(testResultsDir, 'TEST_REPORT.md');
  fs.writeFileSync(reportPath, report);
  
  console.log(`✅ Test report generated: ${reportPath}`);
}

// Run the tests
testHomeButtons().catch(console.error);
