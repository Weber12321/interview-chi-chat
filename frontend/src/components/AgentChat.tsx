import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  CircularProgress,
  Divider,
} from '@mui/material';
import ReactMarkdown from 'react-markdown';
import { AgentChatProps } from '../types';

const AgentChat: React.FC<AgentChatProps> = ({ responses, isLoading }) => {
  const getAgentColor = (agent: string) => {
    switch (agent) {
      case 'HR Agent':
        return 'primary.main';
      case 'Interviewer Agent':
        return 'secondary.main';
      case 'Supervisor Agent':
        return 'success.main';
      default:
        return 'text.primary';
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Interview Progress
      </Typography>
      
      {isLoading ? (
        <Box display="flex" justifyContent="center" p={3}>
          <CircularProgress />
        </Box>
      ) : responses.length === 0 ? (
        <Typography color="text.secondary" align="center">
          No interview responses yet. Upload a CV and start the interview process.
        </Typography>
      ) : (
        <Grid container spacing={2}>
          {responses.map((response, index) => (
            <Grid item xs={12} key={index}>
              <Paper
                elevation={2}
                sx={{
                  p: 2,
                  borderLeft: 4,
                  borderColor: getAgentColor(response.agent),
                }}
              >
                <Typography
                  variant="subtitle1"
                  sx={{ color: getAgentColor(response.agent), mb: 1 }}
                >
                  {response.agent}
                </Typography>
                
                <Divider sx={{ my: 1 }} />
                
                <Box sx={{ mb: 2 }}>
                  <ReactMarkdown>{response.response}</ReactMarkdown>
                </Box>
                
                {response.data && (
                  <>
                    <Divider sx={{ my: 1 }} />
                    <Typography variant="body2" color="text.secondary">
                      Additional Data:
                    </Typography>
                    <pre style={{ overflowX: 'auto', fontSize: '0.875rem' }}>
                      {JSON.stringify(response.data, null, 2)}
                    </pre>
                  </>
                )}
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default AgentChat; 