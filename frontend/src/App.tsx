import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Container, Paper } from '@mui/material';
import ConfigPanel from './components/ConfigPanel';
import FileUpload from './components/FileUpload';
import AgentChat from './components/AgentChat';
import { AgentResponse } from './types';

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

function App() {
  const [apiKey, setApiKey] = useState<string>('');
  const [baseUrl, setBaseUrl] = useState<string>('http://localhost:8000');
  const [responses, setResponses] = useState<AgentResponse[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleConfigSubmit = (config: { apiKey: string; baseUrl: string }) => {
    setApiKey(config.apiKey);
    setBaseUrl(config.baseUrl);
  };

  const handleFileUpload = async (file: File, jobDescriptionUrl: string, companyWebsiteUrl: string) => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('job_description_url', jobDescriptionUrl);
      formData.append('company_website_url', companyWebsiteUrl);

      const response = await fetch(`${baseUrl}/api/v1/start-interview`, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${apiKey}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to start interview');
      }

      const data = await response.json();
      setResponses(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <ConfigPanel onSubmit={handleConfigSubmit} />
          </Paper>
          
          <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <FileUpload onUpload={handleFileUpload} isLoading={isLoading} />
          </Paper>
          
          <Paper elevation={3} sx={{ p: 3 }}>
            <AgentChat responses={responses} isLoading={isLoading} />
          </Paper>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 