import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Chip,
  Paper,
  Alert,
  CircularProgress,
  Collapse,
  Divider
} from '@mui/material';
import { 
  Support as SupportIcon, 
  Speed as SpeedIcon, 
  Security as SecurityIcon,
  Payment as PaymentIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon
} from '@mui/icons-material';

const exampleQueries = [
  {
    title: "Payment Issues",
    description: "Help with subscription renewal and billing problems",
    icon: <PaymentIcon />,
    examples: [
      "My payment was declined when trying to renew my subscription",
      "I haven't received an invoice for last month",
      "How do I update my payment method?"
    ]
  },
  {
    title: "Account Access",
    description: "Login problems and account security",
    icon: <SecurityIcon />,
    examples: [
      "I can't log into my account after changing my password",
      "How to enable two-factor authentication?",
      "Suspicious login attempt detected"
    ]
  },
  {
    title: "Technical Support",
    description: "App crashes and performance issues",
    icon: <SpeedIcon />,
    examples: [
      "App crashes when opening settings page",
      "Slow performance on dashboard",
      "Mobile app not working properly"
    ]
  },
  {
    title: "General Support",
    description: "Product features and general questions",
    icon: <SupportIcon />,
    examples: [
      "How to use the new dashboard features?",
      "Feature request: Dark mode theme",
      "Where can I find user documentation?"
    ]
  }
];

interface AiResponse {
  query: string;
  response: string;
  loading: boolean;
  error: string | null;
  expanded: boolean;
}

const HomeTab: React.FC = () => {
  const [aiResponses, setAiResponses] = useState<AiResponse[]>([]);

  const handleExampleClick = async (example: string) => {
    console.log('🚀 === STARTING AI SUPPORT REQUEST ===');
    console.log('📝 Query:', example);
    console.log('⏰ Timestamp:', new Date().toISOString());
    
    // Check if we already have a response for this query
    const existingResponse = aiResponses.find(r => r.query === example);
    if (existingResponse) {
      console.log('🔄 Found existing response, toggling expansion');
      // Toggle expansion if already exists
      setAiResponses(prev => prev.map(r => 
        r.query === example ? { ...r, expanded: !r.expanded } : r
      ));
      return;
    }

    console.log('🆕 Creating new AI response entry...');
    // Add new response entry
    const newResponse: AiResponse = {
      query: example,
      response: '',
      loading: true,
      error: null,
      expanded: true
    };
    
    setAiResponses(prev => [...prev, newResponse]);
    console.log('✅ UI state updated - Loading indicator shown');

    try {
      console.log('🌐 Making API call to Agno FastAPI...');
      console.log('📍 Endpoint: http://localhost:7777/runs?workflow_id=rag-customer-support-resolution-pipeline');
      console.log('📤 Request payload:', { workflow_input: example });
      
      // Make API call to Agno FastAPI
      const response = await fetch('http://localhost:7777/runs?workflow_id=rag-customer-support-resolution-pipeline', {
        method: 'POST',
        body: (() => {
          const formData = new FormData();
          formData.append('workflow_input', example);
          return formData;
        })(),
      });

      console.log('📥 Response received:', {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok
      });

      if (response.ok) {
        console.log('✅ API call successful, parsing response...');
        const result = await response.json();
        console.log('🔍 Raw API response:', result);
        
        const aiResponse = result.content || result.output || 'AI response received but no content available.';
        console.log('📋 Extracted AI response:', aiResponse);
        console.log('📏 Response length:', aiResponse.length, 'characters');
        
        // Update the response
        setAiResponses(prev => prev.map(r => 
          r.query === example 
            ? { ...r, response: aiResponse, loading: false, error: null }
            : r
        ));
        
        console.log('🎉 === AI SUPPORT REQUEST COMPLETED SUCCESSFULLY ===');
        console.log('📊 Final response summary:', {
          query: example,
          responseLength: aiResponse.length,
          hasContent: aiResponse !== 'AI response received but no content available.',
          timestamp: new Date().toISOString()
        });
      } else {
        const errorText = await response.text();
        console.error('❌ API Error Response:', errorText);
        console.error('🔍 Error details:', {
          status: response.status,
          statusText: response.statusText,
          errorText: errorText
        });
        
        setAiResponses(prev => prev.map(r => 
          r.query === example 
            ? { ...r, loading: false, error: `Failed to get AI response: ${response.status} - ${errorText}` }
            : r
        ));
        
        console.log('💥 === AI SUPPORT REQUEST FAILED ===');
      }
    } catch (err) {
      const error = err as Error;
      console.error('💥 Network/Connection Error:', error);
      console.error('🔍 Error details:', {
        name: error.name,
        message: error.message,
        stack: error.stack
      });
      
      setAiResponses(prev => prev.map(r => 
        r.query === example 
          ? { ...r, loading: false, error: 'Failed to connect to AI system' }
          : r
      ));
      
      console.log('💥 === AI SUPPORT REQUEST FAILED DUE TO NETWORK ERROR ===');
    }
  };

  const toggleResponse = (query: string) => {
    setAiResponses(prev => prev.map(r => 
      r.query === query ? { ...r, expanded: !r.expanded } : r
    ));
  };

  return (
    <Box>
      <Box textAlign="center" mb={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          Welcome to AI Customer Support
        </Typography>
        <Typography variant="h6" color="text.secondary" paragraph>
          Get instant help with our AI-powered support system
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Choose from common issues below or start a chat for personalized assistance
        </Typography>
      </Box>

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
        {exampleQueries.map((category, index) => (
          <Card key={index} elevation={2} sx={{ height: '100%' }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Box color="primary.main" mr={1}>
                  {category.icon}
                </Box>
                <Typography variant="h6" component="h2">
                  {category.title}
                </Typography>
              </Box>
              
              <Typography variant="body2" color="text.secondary" mb={2}>
                {category.description}
              </Typography>

              <Box mb={2}>
                {category.examples.map((example, idx) => (
                  <Chip
                    key={idx}
                    label={example}
                    variant="outlined"
                    size="small"
                    sx={{ mr: 1, mb: 1 }}
                  />
                ))}
              </Box>

              <Button 
                variant="contained" 
                color="primary"
                fullWidth
                onClick={() => handleExampleClick(category.examples[0])}
              >
                Get Help with {category.title}
              </Button>
            </CardContent>
          </Card>
        ))}
      </Box>

      {/* AI Responses Section */}
      {aiResponses.length > 0 && (
        <Box mt={4}>
          <Typography variant="h5" gutterBottom>
            AI Responses
          </Typography>
          <Divider sx={{ mb: 3 }} />
          
          {aiResponses.map((aiResponse, index) => (
            <Card key={index} elevation={2} sx={{ mb: 2 }}>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="h6" color="primary">
                    {aiResponse.query}
                  </Typography>
                  <Button
                    size="small"
                    onClick={() => toggleResponse(aiResponse.query)}
                    endIcon={aiResponse.expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                  >
                    {aiResponse.expanded ? 'Hide' : 'Show'} Response
                  </Button>
                </Box>
                
                <Collapse in={aiResponse.expanded}>
                  {aiResponse.loading && (
                    <Box display="flex" alignItems="center" gap={2} mb={2}>
                      <CircularProgress size={20} />
                      <Typography>Getting AI response from knowledge base...</Typography>
                    </Box>
                  )}
                  
                  {aiResponse.error && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                      {aiResponse.error}
                    </Alert>
                  )}
                  
                  {aiResponse.response && !aiResponse.loading && !aiResponse.error && (
                    <Paper elevation={1} sx={{ p: 2, backgroundColor: '#f8f9fa' }}>
                      <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                        {aiResponse.response}
                      </Typography>
                    </Paper>
                  )}
                </Collapse>
              </CardContent>
            </Card>
          ))}
        </Box>
      )}

      <Paper elevation={1} sx={{ p: 3, mt: 4, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Ready to get started?
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          Click any button above to get instant AI-powered help, or switch to the AI Chat tab for a conversation
        </Typography>
        <Button variant="outlined" color="primary" size="large">
          Start AI Chat
        </Button>
      </Paper>
    </Box>
  );
};

export default HomeTab;
