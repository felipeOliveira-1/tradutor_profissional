import React, { useState, useEffect } from 'react';
import api from './config/axios';
import { BrowserRouter as Router, Route, Routes, Link, useParams } from 'react-router-dom';
import DocumentUpload from './components/DocumentUpload';
import DocumentList from './components/DocumentList';
import DocumentViewer from './components/DocumentViewer';
import './App.css';

interface Translation {
  id: number;
  original_text: string;
  translated_text: string;
  source_language: string;
  target_language: string;
  created_at: string;
  formality_level?: string;
  style?: string;
  context?: string;
  has_been_edited: number;
  quality_rating?: number;
  feedback_notes?: string;
}

interface TranslationRequest {
  original_text: string;
  source_language: string;
  target_language: string;
  formality_level?: string;
  style?: string;
  context?: string;
}

function App() {
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [translations, setTranslations] = useState<Translation[]>([]);
  const [formality, setFormality] = useState<string>('neutral');
  const [style, setStyle] = useState<string>('general');
  const [showHistory, setShowHistory] = useState(false);
  const [sourceLanguage, setSourceLanguage] = useState<string>('en');
  const [targetLanguage, setTargetLanguage] = useState<string>('pt');

  useEffect(() => {
    fetchTranslations();
  }, []);

  const fetchTranslations = async () => {
    try {
      const response = await api.get('/api/translations');
      setTranslations(response.data);
    } catch (error) {
      console.error('Error fetching translations:', error);
    }
  };

  const handleTranslate = async () => {
    if (!inputText.trim()) return;

    setIsLoading(true);
    try {
      const response = await api.post('/api/translations/quick', {
        text: inputText,
        source_language: sourceLanguage,
        target_language: targetLanguage,
        formality_level: formality,
        style: style
      });
      setTranslatedText(response.data.translated_text);
      await fetchTranslations(); // Atualizar o histórico
    } catch (error) {
      console.error('Error translating:', error);
      setTranslatedText('Error occurred during translation');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRateTranslation = async (id: number, rating: number) => {
    try {
      await api.put(`/api/translations/${id}`, {
        quality_rating: rating
      });
      await fetchTranslations();
    } catch (error) {
      console.error('Error rating translation:', error);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Header/Navigation */}
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <Link to="/" className="text-xl font-bold text-gray-800">
                    Tradutor Profissional
                  </Link>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link
                    to="/"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Início
                  </Link>
                  <Link
                    to="/upload"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Upload
                  </Link>
                  <Link
                    to="/documents"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Documentos
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/upload" element={
              <div className="px-4 py-6 sm:px-0">
                <div className="mb-8">
                  <h1 className="text-2xl font-semibold text-gray-900">Upload de Documentos</h1>
                  <p className="mt-2 text-sm text-gray-600">
                    Faça upload de documentos PDF, DOCX ou TXT para tradução.
                  </p>
                </div>
                <DocumentUpload />
              </div>
            } />
            <Route path="/documents" element={
              <div className="px-4 py-6 sm:px-0">
                <div className="mb-8">
                  <h1 className="text-2xl font-semibold text-gray-900">Meus Documentos</h1>
                  <p className="mt-2 text-sm text-gray-600">
                    Gerencie e traduza seus documentos.
                  </p>
                </div>
                <DocumentList />
              </div>
            } />
            <Route path="/documents/:id" element={
              <div className="px-4 py-6 sm:px-0">
                <DocumentViewerWrapper />
              </div>
            } />
            <Route path="/" element={
              <div className="px-4 py-6 sm:px-0">
                <div className="min-h-screen bg-gray-50 py-6 flex flex-col justify-start sm:py-12">
                  <div className="relative py-3 sm:max-w-4xl sm:mx-auto w-full">
                    <div className="relative px-4 py-6 bg-white shadow-lg sm:rounded-lg sm:p-10">
                      <div className="mx-auto">
                        {/* Área de tradução */}
                        <div className="flex flex-col md:flex-row gap-4">
                          {/* Coluna da esquerda - Texto original */}
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-2 bg-gray-50 p-2 rounded">
                              <select
                                className="bg-transparent border-none text-sm focus:outline-none focus:ring-0"
                                value={sourceLanguage}
                                onChange={(e) => setSourceLanguage(e.target.value)}
                              >
                                <option value="en">English</option>
                                <option value="pt">Portuguese</option>
                                <option value="es">Spanish</option>
                                <option value="fr">French</option>
                              </select>
                            </div>
                            <div className="relative">
                              <textarea
                                className="w-full h-48 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                                placeholder="Digite o texto para traduzir..."
                                value={inputText}
                                onChange={(e) => setInputText(e.target.value)}
                              />
                              <div className="absolute bottom-2 right-2 text-xs text-gray-400">
                                {inputText.length}/5,000
                              </div>
                            </div>
                          </div>

                          {/* Coluna da direita - Texto traduzido */}
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-2 bg-gray-50 p-2 rounded">
                              <select
                                className="bg-transparent border-none text-sm focus:outline-none focus:ring-0"
                                value={targetLanguage}
                                onChange={(e) => setTargetLanguage(e.target.value)}
                              >
                                <option value="pt">Portuguese</option>
                                <option value="en">English</option>
                                <option value="es">Spanish</option>
                                <option value="fr">French</option>
                              </select>
                            </div>
                            <div className="relative">
                              <textarea
                                className="w-full h-48 p-4 border rounded-lg bg-gray-50 resize-none"
                                value={translatedText}
                                readOnly
                                placeholder="Tradução aparecerá aqui..."
                              />
                              {isLoading && (
                                <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75">
                                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>

                        {/* Botão de tradução */}
                        <div className="mt-4 flex justify-center">
                          <button
                            onClick={handleTranslate}
                            disabled={isLoading || !inputText.trim()}
                            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {isLoading ? 'Traduzindo...' : 'Traduzir'}
                          </button>
                        </div>

                        {/* Configurações adicionais */}
                        <div className="mt-6 space-y-4">
                          <div className="flex gap-4">
                            <div className="flex-1">
                              <label className="block text-sm font-medium text-gray-700 mb-1">
                                Formalidade
                              </label>
                              <select
                                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                                value={formality}
                                onChange={(e) => setFormality(e.target.value)}
                              >
                                <option value="formal">Formal</option>
                                <option value="neutral">Neutro</option>
                                <option value="informal">Informal</option>
                              </select>
                            </div>
                            <div className="flex-1">
                              <label className="block text-sm font-medium text-gray-700 mb-1">
                                Estilo
                              </label>
                              <select
                                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                                value={style}
                                onChange={(e) => setStyle(e.target.value)}
                              >
                                <option value="general">Geral</option>
                                <option value="technical">Técnico</option>
                                <option value="literary">Literário</option>
                                <option value="academic">Acadêmico</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

const DocumentViewerWrapper = () => {
  const { id } = useParams<{ id: string }>();
  return <DocumentViewer documentId={Number(id)} />;
};

export default App;
