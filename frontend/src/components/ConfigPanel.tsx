import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Grid,
} from '@mui/material';
import { ConfigPanelProps } from '../types';

const ConfigPanel: React.FC<ConfigPanelProps> = ({ onSubmit }) => {
  const [apiKey, setApiKey] = useState('');
  const [baseUrl, setBaseUrl] = useState('http://localhost:8000');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ apiKey, baseUrl });
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Typography variant="h6" gutterBottom>
        Configuration
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="OpenAI API Key"
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            required
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="API Base URL"
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
            required
          />
        </Grid>
        <Grid item xs={12}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
          >
            Save Configuration
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ConfigPanel; 