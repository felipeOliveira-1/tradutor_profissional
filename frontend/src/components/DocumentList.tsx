import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../config/axios';
import { FiFile, FiClock, FiLayers, FiAlertCircle, FiTrash2 } from 'react-icons/fi';

interface Document {
  id: number;
  filename: string;
  size: number;
  num_chapters: number;
  total_paragraphs: number;
  created_at: string;
}

const DocumentList: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const fetchDocuments = async () => {
    try {
      const response = await api.get('/api/documents');
      setDocuments(response.data);
      setLoading(false);
    } catch (error) {
      setError('Erro ao carregar documentos. Por favor, tente novamente.');
      setLoading(false);
      console.error('Error fetching documents:', error);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleDelete = async (id: number) => {
    setDeletingId(id);
    setShowConfirmation(true);
  };

  const confirmDelete = async () => {
    if (deletingId === null) return;

    try {
      await api.delete(`/api/documents/${deletingId}`);
      setDocuments(documents.filter(doc => doc.id !== deletingId));
      setShowConfirmation(false);
      setDeletingId(null);
    } catch (error) {
      console.error('Error deleting document:', error);
      setError('Erro ao deletar documento. Por favor, tente novamente.');
    }
  };

  const cancelDelete = () => {
    setShowConfirmation(false);
    setDeletingId(null);
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[200px] text-red-500">
        <FiAlertCircle className="mr-2" />
        {error}
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <FiFile className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhum documento</h3>
        <p className="mt-1 text-sm text-gray-500">Comece fazendo upload de um documento.</p>
        <div className="mt-6">
          <Link
            to="/upload"
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Upload de Documento
          </Link>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {documents.map((doc) => (
            <li key={doc.id} className="relative">
              <div className="flex justify-between items-center">
                <Link to={`/documents/${doc.id}`} className="block hover:bg-gray-50 flex-grow">
                  <div className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <FiFile className="flex-shrink-0 h-5 w-5 text-gray-400" />
                        <p className="ml-2 text-sm font-medium text-blue-600 truncate">
                          {doc.filename}
                        </p>
                      </div>
                      <div className="ml-2 flex-shrink-0 flex">
                        <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          {formatFileSize(doc.size)}
                        </p>
                      </div>
                    </div>
                    <div className="mt-2 sm:flex sm:justify-between">
                      <div className="sm:flex">
                        <p className="flex items-center text-sm text-gray-500">
                          <FiLayers className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                          {doc.num_chapters} capítulos • {doc.total_paragraphs} parágrafos
                        </p>
                      </div>
                      <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                        <FiClock className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                        <p>
                          Enviado em {formatDate(doc.created_at)}
                        </p>
                      </div>
                    </div>
                  </div>
                </Link>
                <button
                  onClick={() => handleDelete(doc.id)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 p-2 text-gray-400 hover:text-red-500"
                  title="Deletar documento"
                >
                  <FiTrash2 className="h-5 w-5" />
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* Modal de Confirmação */}
      {showConfirmation && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>

            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                    <FiAlertCircle className="h-6 w-6 text-red-600" />
                  </div>
                  <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                      Confirmar deleção
                    </h3>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500">
                        Tem certeza que deseja deletar este documento? Esta ação não pode ser desfeita.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  onClick={confirmDelete}
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Deletar
                </button>
                <button
                  type="button"
                  onClick={cancelDelete}
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DocumentList;
