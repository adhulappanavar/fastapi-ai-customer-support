import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Chip,
  Paper
} from '@mui/material';
import { 
  Support as SupportIcon, 
  Speed as SpeedIcon, 
  Security as SecurityIcon,
  Payment as PaymentIcon 
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

const HomeTab: React.FC = () => {
  const handleExampleClick = (example: string) => {
    console.log('Switch to chat with example:', example);
    // In a real application, you would update the chat tab state or pre-fill the chat input
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

      <Paper elevation={1} sx={{ p: 3, mt: 4, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Ready to get started?
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          Switch to the AI Chat tab to start a conversation with our intelligent support agent
        </Typography>
        <Button variant="outlined" color="primary" size="large">
          Start AI Chat
        </Button>
      </Paper>
    </Box>
  );
};

export default HomeTab;
