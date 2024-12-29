import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import api from '../config/axios';
import axios from 'axios';
import { FiUpload, FiFile, FiCheck, FiAlertCircle } from 'react-icons/fi';

interface DocumentUploadProps {
  onUploadSuccess?: () => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setError(null);
    setProgress(0);
    
    if (acceptedFiles.length === 0) {
      setError('Por favor, selecione um arquivo para upload.');
      return;
    }

    const file = acceptedFiles[0];
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ];

    if (!allowedTypes.includes(file.type)) {
      setError('Tipo de arquivo não suportado. Use PDF, DOCX ou TXT.');
      return;
    }

    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setError('O arquivo é muito grande. Tamanho máximo: 10MB');
      return;
    }

    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/api/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setProgress(progress);
          }
        },
      });

      console.log('Upload successful:', response.data);
      setProgress(100);
      if (onUploadSuccess) {
        onUploadSuccess();
      }
    } catch (error) {
      console.error('Upload error:', error);
      if (axios.isAxiosError(error) && error.response) {
        setError(error.response.data.detail || 'Erro ao fazer upload do arquivo.');
      } else {
        setError('Erro ao fazer upload do arquivo. Tente novamente.');
      }
    } finally {
      setUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false
  });

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-indigo-400'}
          ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input {...getInputProps()} disabled={uploading} />
        
        {uploading ? (
          <div className="space-y-4">
            <div className="text-gray-600">Fazendo upload... {progress}%</div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-indigo-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        ) : isDragActive ? (
          <p className="text-indigo-600">Solte o arquivo aqui...</p>
        ) : (
          <div className="space-y-2">
            <p className="text-gray-600">
              Arraste e solte um arquivo aqui, ou clique para selecionar
            </p>
            <p className="text-sm text-gray-500">
              PDF, DOCX ou TXT (max. 10MB)
            </p>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {progress === 100 && !error && (
        <div className="mt-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
          Upload concluído com sucesso!
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
