import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Button,
  Chip,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  CircularProgress,
  Alert
} from '@mui/material';
import { 
  Search as SearchIcon, 
  Refresh as RefreshIcon,
  Visibility as ViewIcon,
  SmartToy as AiIcon
} from '@mui/icons-material';

interface Ticket {
  id: number;
  ticket_number: string;
  title: string;
  description: string;
  user_full_name: string;
  category_name: string;
  priority_name: string;
  status_name: string;
  created_at: string;
  tags?: string;
}

interface AiResolution {
  ticketId: number;
  response: string;
  loading: boolean;
  error: string | null;
}

const TicketsTab: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [filteredTickets, setFilteredTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [aiResolutions, setAiResolutions] = useState<AiResolution[]>([]);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [priorityFilter, setPriorityFilter] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<string>('');

  useEffect(() => {
    fetchTickets();
  }, []);

  useEffect(() => {
    filterTickets();
  }, [tickets, searchTerm, statusFilter, priorityFilter, categoryFilter]);

  const fetchTickets = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/tickets');
      if (response.ok) {
        const data = await response.json();
        setTickets(data);
        setError(null);
      } else {
        throw new Error('Failed to fetch tickets');
      }
    } catch (err) {
      setError('Failed to load tickets. Please check if the ticketing API is running.');
      console.error('Error fetching tickets:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterTickets = () => {
    let filtered = [...tickets];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(ticket =>
        ticket.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        ticket.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (ticket.tags && ticket.tags.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Status filter
    if (statusFilter) {
      filtered = filtered.filter(ticket => ticket.status_name === statusFilter);
    }

    // Priority filter
    if (priorityFilter) {
      filtered = filtered.filter(ticket => ticket.priority_name === priorityFilter);
    }

    // Category filter
    if (categoryFilter) {
      filtered = filtered.filter(ticket => ticket.category_name === categoryFilter);
    }

    setFilteredTickets(filtered);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'open': return 'success';
      case 'in progress': return 'warning';
      case 'resolved': return 'info';
      case 'closed': return 'default';
      default: return 'default';
    }
  };

  const handleViewTicket = (ticket: Ticket) => {
    console.log('Viewing ticket:', ticket);
    // This could open a modal or navigate to ticket details
  };

  const handleAiResolution = async (ticket: Ticket) => {
    // Check if we already have a resolution for this ticket
    const existingResolution = aiResolutions.find(r => r.ticketId === ticket.id);
    if (existingResolution) {
      return; // Already resolved
    }

    // Add loading state for this ticket
    setAiResolutions(prev => [...prev, {
      ticketId: ticket.id,
      response: '',
      loading: true,
      error: null
    }]);

    try {
      // Prepare the query for AI analysis
      const query = `Ticket: ${ticket.title}\n\nDescription: ${ticket.description}\n\nCategory: ${ticket.category_name}\nPriority: ${ticket.priority_name}\n\nPlease provide a comprehensive solution for this support ticket.`;

      const response = await fetch('http://localhost:7777/runs?workflow_id=customer-support-resolution-pipeline', {
        method: 'POST',
        body: (() => {
          const formData = new FormData();
          formData.append('workflow_input', query);
          return formData;
        })(),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('AI Response received:', result);
        const aiResponse = result.content || result.output || 'AI response received but no content available.';
        
        // Update the resolution with the response
        setAiResolutions(prev => prev.map(r => 
          r.ticketId === ticket.id 
            ? { ...r, response: aiResponse, loading: false, error: null }
            : r
        ));
      } else {
        const errorText = await response.text();
        console.error('API Error Response:', errorText);
        throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
      }
    } catch (err) {
      console.error('Error getting AI resolution:', err);
      setAiResolutions(prev => prev.map(r => 
        r.ticketId === ticket.id 
          ? { ...r, loading: false, error: 'Failed to get AI resolution' }
          : r
      ));
    }
  };

  const getAiResolution = (ticketId: number) => {
    return aiResolutions.find(r => r.ticketId === ticketId);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5">
          Ticket Management
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={fetchTickets}
        >
          Refresh
        </Button>
      </Box>

      {/* Filters */}
      <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
        <Box display="flex" gap={2} flexWrap="wrap" alignItems="center">
          <TextField
            label="Search tickets"
            variant="outlined"
            size="small"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{ minWidth: 200 }}
            InputProps={{
              startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />
            }}
          />
          
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={statusFilter}
              label="Status"
              onChange={(e: SelectChangeEvent) => setStatusFilter(e.target.value)}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="Open">Open</MenuItem>
              <MenuItem value="In Progress">In Progress</MenuItem>
              <MenuItem value="Resolved">Resolved</MenuItem>
              <MenuItem value="Closed">Closed</MenuItem>
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Priority</InputLabel>
            <Select
              value={priorityFilter}
              label="Priority"
              onChange={(e: SelectChangeEvent) => setPriorityFilter(e.target.value)}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="Critical">Critical</MenuItem>
              <MenuItem value="High">High</MenuItem>
              <MenuItem value="Medium">Medium</MenuItem>
              <MenuItem value="Low">Low</MenuItem>
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Category</InputLabel>
            <Select
              value={categoryFilter}
              label="Category"
              onChange={(e: SelectChangeEvent) => setCategoryFilter(e.target.value)}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="Account Access">Account Access</MenuItem>
              <MenuItem value="Billing & Payments">Billing & Payments</MenuItem>
              <MenuItem value="Technical Support">Technical Support</MenuItem>
              <MenuItem value="Product Features">Product Features</MenuItem>
              <MenuItem value="Security Issues">Security Issues</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Paper>

      {/* Results count */}
      <Typography variant="body2" color="text.secondary" mb={2}>
        Showing {filteredTickets.length} of {tickets.length} tickets
      </Typography>

      {/* Tickets Table */}
      <TableContainer component={Paper} elevation={2}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Ticket #</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>User</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Priority</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredTickets.map((ticket) => (
              <React.Fragment key={ticket.id}>
                <TableRow hover>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {ticket.ticket_number}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Box>
                      <Typography variant="body2" fontWeight="medium">
                        {ticket.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" sx={{ 
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden'
                      }}>
                        {ticket.description}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{ticket.user_full_name}</TableCell>
                  <TableCell>{ticket.category_name}</TableCell>
                  <TableCell>
                    <Chip 
                      label={ticket.priority_name} 
                      color={getPriorityColor(ticket.priority_name) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={ticket.status_name} 
                      color={getStatusColor(ticket.status_name) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="caption">
                      {new Date(ticket.created_at).toLocaleDateString()}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Box display="flex" gap={1}>
                      <IconButton 
                        size="small" 
                        onClick={() => handleViewTicket(ticket)}
                        color="primary"
                        title="View Ticket Details"
                      >
                        <ViewIcon />
                      </IconButton>
                      <IconButton 
                        size="small" 
                        onClick={() => handleAiResolution(ticket)}
                        color="secondary"
                        title="Get AI Resolution"
                        disabled={getAiResolution(ticket.id)?.loading || !!getAiResolution(ticket.id)?.response}
                      >
                        {getAiResolution(ticket.id)?.loading ? (
                          <CircularProgress size={16} />
                        ) : (
                          <AiIcon />
                        )}
                      </IconButton>
                    </Box>
                  </TableCell>
                </TableRow>
                
                {/* AI Resolution Row */}
                {getAiResolution(ticket.id) && (
                  <TableRow>
                    <TableCell colSpan={8} sx={{ p: 0 }}>
                      <Box sx={{ p: 2, bgcolor: 'grey.50', borderTop: '1px solid', borderColor: 'grey.200' }}>
                        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                          <Typography variant="subtitle2" color="primary" display="flex" alignItems="center" gap={1}>
                            <AiIcon fontSize="small" />
                            AI Resolution
                          </Typography>
                          {getAiResolution(ticket.id)?.error && (
                            <Chip 
                              label="Error" 
                              color="error" 
                              size="small" 
                              variant="outlined"
                            />
                          )}
                        </Box>
                        
                        {getAiResolution(ticket.id)?.loading && (
                          <Box display="flex" alignItems="center" gap={1}>
                            <CircularProgress size={16} />
                            <Typography variant="body2" color="text.secondary">
                              Getting AI resolution...
                            </Typography>
                          </Box>
                        )}
                        
                        {getAiResolution(ticket.id)?.error && (
                          <Alert severity="error" sx={{ mb: 1 }}>
                            {getAiResolution(ticket.id)?.error}
                          </Alert>
                        )}
                        
                        {getAiResolution(ticket.id)?.response && (
                          <Box>
                            <Typography variant="body2" component="div" sx={{ 
                              whiteSpace: 'pre-wrap',
                              fontFamily: 'monospace',
                              fontSize: '0.875rem',
                              lineHeight: 1.5
                            }}>
                              {getAiResolution(ticket.id)?.response}
                            </Typography>
                          </Box>
                        )}
                      </Box>
                    </TableCell>
                  </TableRow>
                )}
              </React.Fragment>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {filteredTickets.length === 0 && (
        <Paper elevation={1} sx={{ p: 4, textAlign: 'center', mt: 2 }}>
          <Typography variant="h6" color="text.secondary">
            No tickets found
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Try adjusting your search criteria or filters
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default TicketsTab;
