import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Alert,
  CircularProgress,
  Divider,
  Chip
} from '@mui/material';
import {
  Description as PdfIcon,
  Upload as UploadIcon,
  Build as BuildIcon,
  Storage as StorageIcon
} from '@mui/icons-material';

interface PdfFile {
  name: string;
  size: string;
  uploadedAt: string;
}

interface VectorDbStats {
  totalDocuments: number;
  totalChunks: number;
  indexSize: string;
  lastUpdated: string;
}

const KnowledgeBaseTab: React.FC = () => {
  const [pdfFiles, setPdfFiles] = useState<PdfFile[]>([]);
  const [vectorDbStats, setVectorDbStats] = useState<VectorDbStats | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info', text: string } | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // Mock data - replace with actual API calls
  useEffect(() => {
    loadPdfFiles();
    loadVectorDbStats();
  }, []);

  const loadPdfFiles = async () => {
    try {
      // Mock API call - replace with actual endpoint
      const mockFiles: PdfFile[] = [
        { name: 'customer_support_guide.pdf', size: '2.3 MB', uploadedAt: '2024-01-15' },
        { name: 'technical_troubleshooting_guide.pdf', size: '1.8 MB', uploadedAt: '2024-01-10' },
        { name: 'billing_subscription_guide.pdf', size: '1.5 MB', uploadedAt: '2024-01-05' }
      ];
      setPdfFiles(mockFiles);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load PDF files' });
    }
  };

  const loadVectorDbStats = async () => {
    try {
      // Mock API call - replace with actual endpoint
      const mockStats: VectorDbStats = {
        totalDocuments: 3,
        totalChunks: 156,
        indexSize: '45.2 MB',
        lastUpdated: '2024-01-15 14:30:00'
      };
      setVectorDbStats(mockStats);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load vector database statistics' });
    }
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setMessage(null);
    } else if (file) {
      setMessage({ type: 'error', text: 'Please select a PDF file' });
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    try {
      // Mock upload - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const newFile: PdfFile = {
        name: selectedFile.name,
        size: `${(selectedFile.size / (1024 * 1024)).toFixed(1)} MB`,
        uploadedAt: new Date().toISOString().split('T')[0]
      };
      
      setPdfFiles(prev => [newFile, ...prev]);
      setSelectedFile(null);
      setMessage({ type: 'success', text: 'PDF uploaded successfully' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to upload PDF' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleBuildKnowledgeBase = async () => {
    setIsLoading(true);
    try {
      // Mock build process - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Reload stats after build
      await loadVectorDbStats();
      setMessage({ type: 'success', text: 'Knowledge base built successfully' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to build knowledge base' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Knowledge Base Management
      </Typography>
      
      {message && (
        <Alert severity={message.type} sx={{ mb: 3 }}>
          {message.text}
        </Alert>
      )}

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
        {/* PDF Upload Section */}
        <Card elevation={2}>
          <CardContent>
            <Typography variant="h6" gutterBottom display="flex" alignItems="center">
              <UploadIcon sx={{ mr: 1 }} />
              Upload PDF
            </Typography>
            
            <Box sx={{ mb: 2 }}>
              <input
                accept=".pdf"
                style={{ display: 'none' }}
                id="pdf-file-input"
                type="file"
                onChange={handleFileSelect}
              />
              <label htmlFor="pdf-file-input">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<UploadIcon />}
                  fullWidth
                >
                  Select PDF File
                </Button>
              </label>
            </Box>
            
            {selectedFile && (
              <Box sx={{ mb: 2 }}>
                <Chip
                  icon={<PdfIcon />}
                  label={selectedFile.name}
                  onDelete={() => setSelectedFile(null)}
                  color="primary"
                />
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  Size: {(selectedFile.size / (1024 * 1024)).toFixed(1)} MB
                </Typography>
              </Box>
            )}
            
            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={!selectedFile || isLoading}
              fullWidth
              startIcon={isLoading ? <CircularProgress size={20} /> : <UploadIcon />}
            >
              {isLoading ? 'Uploading...' : 'Upload PDF'}
            </Button>
          </CardContent>
        </Card>

        {/* Build Knowledge Base Section */}
        <Card elevation={2}>
          <CardContent>
            <Typography variant="h6" gutterBottom display="flex" alignItems="center">
              <BuildIcon sx={{ mr: 1 }} />
              Build Knowledge Base
            </Typography>
            
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Process all uploaded PDFs and build the vector database for AI search
            </Typography>
            
            <Button
              variant="contained"
              color="secondary"
              onClick={handleBuildKnowledgeBase}
              disabled={isLoading || pdfFiles.length === 0}
              fullWidth
              startIcon={isLoading ? <CircularProgress size={20} /> : <BuildIcon />}
            >
              {isLoading ? 'Building...' : 'Build Knowledge Base'}
            </Button>
          </CardContent>
        </Card>

        {/* PDF Files List */}
        <Card elevation={2}>
          <CardContent>
            <Typography variant="h6" gutterBottom display="flex" alignItems="center">
              <PdfIcon sx={{ mr: 1 }} />
              PDF Files ({pdfFiles.length})
            </Typography>
            
            {pdfFiles.length === 0 ? (
              <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
                No PDF files uploaded yet
              </Typography>
            ) : (
              <List dense>
                {pdfFiles.map((file, index) => (
                  <React.Fragment key={index}>
                    <ListItem>
                      <ListItemIcon>
                        <PdfIcon color="error" />
                      </ListItemIcon>
                      <ListItemText
                        primary={file.name}
                        secondary={`${file.size} • Uploaded: ${file.uploadedAt}`}
                      />
                    </ListItem>
                    {index < pdfFiles.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            )}
          </CardContent>
        </Card>

        {/* Vector Database Statistics */}
        <Card elevation={2}>
          <CardContent>
            <Typography variant="h6" gutterBottom display="flex" alignItems="center">
              <StorageIcon sx={{ mr: 1 }} />
              Vector Database Statistics
            </Typography>
            
            {vectorDbStats ? (
              <Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Total Documents:</Typography>
                  <Typography variant="body2" fontWeight="bold">{vectorDbStats.totalDocuments}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Total Chunks:</Typography>
                  <Typography variant="body2" fontWeight="bold">{vectorDbStats.totalChunks}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Index Size:</Typography>
                  <Typography variant="body2" fontWeight="bold">{vectorDbStats.indexSize}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Last Updated:</Typography>
                  <Typography variant="body2" fontWeight="bold">{vectorDbStats.lastUpdated}</Typography>
                </Box>
              </Box>
            ) : (
              <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
                Loading statistics...
              </Typography>
            )}
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default KnowledgeBaseTab;
