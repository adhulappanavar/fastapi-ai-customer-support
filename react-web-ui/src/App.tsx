import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Tabs,
  Tab,
  Paper,
  ThemeProvider,
  createTheme,
  CssBaseline
} from '@mui/material';
import { Chat as ChatIcon, Home as HomeIcon, ConfirmationNumber as TicketIcon, Storage as StorageIcon } from '@mui/icons-material';
import HomeTab from './components/HomeTab';
import ChatTab from './components/ChatTab';
import TicketsTab from './components/TicketsTab';
import KnowledgeBaseTab from './components/KnowledgeBaseTab';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              AI Customer Support System
            </Typography>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Paper elevation={3}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs 
                value={tabValue} 
                onChange={handleTabChange} 
                aria-label="customer support tabs"
                centered
              >
                <Tab icon={<HomeIcon />} label="Home" />
                <Tab icon={<ChatIcon />} label="AI Chat" />
                <Tab icon={<TicketIcon />} label="Tickets" />
                <Tab icon={<StorageIcon />} label="Knowledge Base" />
              </Tabs>
            </Box>
            
            <TabPanel value={tabValue} index={0}>
              <HomeTab />
            </TabPanel>
            
            <TabPanel value={tabValue} index={1}>
              <ChatTab />
            </TabPanel>
            
            <TabPanel value={tabValue} index={2}>
              <TicketsTab />
            </TabPanel>
            
            <TabPanel value={tabValue} index={3}>
              <KnowledgeBaseTab />
            </TabPanel>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
