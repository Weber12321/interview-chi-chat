import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Button,
  TextField,
  Typography,
  CircularProgress,
  Paper,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { FileUploadProps } from '../types';

const FileUpload: React.FC<FileUploadProps> = ({ onUpload, isLoading }) => {
  const [jobDescriptionUrl, setJobDescriptionUrl] = useState('');
  const [companyWebsiteUrl, setCompanyWebsiteUrl] = useState('');
  const [file, setFile] = useState<File | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0]);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (file && jobDescriptionUrl && companyWebsiteUrl) {
      onUpload(file, jobDescriptionUrl, companyWebsiteUrl);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Typography variant="h6" gutterBottom>
        Upload CV and Job Information
      </Typography>
      
      <Paper
        {...getRootProps()}
        sx={{
          p: 3,
          mb: 2,
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
          backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
          cursor: 'pointer',
          textAlign: 'center',
        }}
      >
        <input {...getInputProps()} />
        <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
        <Typography>
          {isDragActive
            ? 'Drop the PDF file here'
            : 'Drag and drop a PDF CV here, or click to select'}
        </Typography>
        {file && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Selected file: {file.name}
          </Typography>
        )}
      </Paper>

      <TextField
        fullWidth
        label="Job Description URL"
        value={jobDescriptionUrl}
        onChange={(e) => setJobDescriptionUrl(e.target.value)}
        required
        sx={{ mb: 2 }}
      />

      <TextField
        fullWidth
        label="Company Website URL"
        value={companyWebsiteUrl}
        onChange={(e) => setCompanyWebsiteUrl(e.target.value)}
        required
        sx={{ mb: 2 }}
      />

      <Button
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
        disabled={!file || !jobDescriptionUrl || !companyWebsiteUrl || isLoading}
      >
        {isLoading ? (
          <CircularProgress size={24} color="inherit" />
        ) : (
          'Start Interview'
        )}
      </Button>
    </Box>
  );
};

export default FileUpload; 