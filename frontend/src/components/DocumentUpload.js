import React, { useState, useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import axios from 'axios';

const DocumentUpload = ({ onUploadSuccess }) => {
  const [uploadStatus, setUploadStatus] = useState('idle'); // idle, uploading, success, error
  const [uploadMessage, setUploadMessage] = useState('');
  const [documents, setDocuments] = useState([]);
  const [isLoadingDocuments, setIsLoadingDocuments] = useState(false);

  // Load documents on component mount
  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    setIsLoadingDocuments(true);
    try {
      const response = await axios.get('/documents');
      setDocuments(response.data.documents || []);
    } catch (error) {
      console.error('Error loading documents:', error);
    } finally {
      setIsLoadingDocuments(false);
    }
  };

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Validate file type
    if (!file.type.includes('pdf')) {
      setUploadStatus('error');
      setUploadMessage('Please upload a PDF file.');
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setUploadStatus('error');
      setUploadMessage('File size must be less than 10MB.');
      return;
    }

    setUploadStatus('uploading');
    setUploadMessage('Processing document...');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadStatus('success');
      setUploadMessage(response.data.message);
      
      // Reload documents list
      await loadDocuments();
      
      // Notify parent component
      if (onUploadSuccess) {
        onUploadSuccess();
      }

      // Clear success message after 5 seconds
      setTimeout(() => {
        setUploadStatus('idle');
        setUploadMessage('');
      }, 5000);

    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('error');
      setUploadMessage(
        error.response?.data?.detail || 'Failed to upload document. Please try again.'
      );
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false,
    disabled: uploadStatus === 'uploading'
  });

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      onDrop([file]);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-card">
        <h2>Upload Documents to Knowledge Base</h2>
        <p>Upload PDF documents to expand the AI agent's knowledge base. The agent will be able to answer questions based on the content of uploaded documents.</p>
        
        <div
          {...getRootProps()}
          className={`upload-area ${isDragActive ? 'dragover' : ''}`}
        >
          <input {...getInputProps()} />
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="file-input"
            disabled={uploadStatus === 'uploading'}
          />
          
          <Upload className="upload-icon" />
          <div className="upload-text">
            {isDragActive
              ? 'Drop the PDF file here...'
              : 'Drag & drop a PDF file here, or click to select'
            }
          </div>
          <div className="upload-subtext">
            Only PDF files are supported. Maximum file size: 10MB
          </div>
        </div>

        {uploadStatus === 'uploading' && (
          <div className="upload-progress">
            <Loader className="loading-spinner" />
            {uploadMessage}
          </div>
        )}

        {uploadStatus === 'success' && (
          <div className="upload-success">
            <CheckCircle size={20} />
            {uploadMessage}
          </div>
        )}

        {uploadStatus === 'error' && (
          <div className="upload-error">
            <AlertCircle size={20} />
            {uploadMessage}
          </div>
        )}

        <div className="documents-list">
          <h3>Uploaded Documents</h3>
          {isLoadingDocuments ? (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
              <Loader className="loading-spinner" />
              Loading documents...
            </div>
          ) : documents.length === 0 ? (
            <p style={{ color: '#64748b', fontStyle: 'italic' }}>
              No documents uploaded yet. Upload a PDF to get started!
            </p>
          ) : (
            <div>
              {documents.map((doc, index) => (
                <div key={index} className="document-item">
                  <div>
                    <div className="document-name">
                      <FileText size={16} style={{ marginRight: '0.5rem' }} />
                      {doc.filename}
                    </div>
                    <div className="document-info">
                      {doc.text_length} characters, {doc.chunks} chunks
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
