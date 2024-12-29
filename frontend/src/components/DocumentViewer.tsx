import React, { useState, useEffect } from 'react';
import api from '../config/axios';

interface Chapter {
  title: string;
  paragraphs: string[];
}

interface Document {
  id: number;
  filename: string;
  chapters: Chapter[];
  metadata: {
    num_pages?: number;
    author?: string;
    title?: string;
  };
}

interface DocumentViewerProps {
  documentId: number;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentId }) => {
  const [document, setDocument] = useState<Document | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedChapter, setSelectedChapter] = useState<number>(0);
  const [selectedParagraphs, setSelectedParagraphs] = useState<Set<number>>(new Set());
  const [translatedParagraphs, setTranslatedParagraphs] = useState<{ [key: number]: string }>({});
  const [translating, setTranslating] = useState(false);
  const [sourceLanguage, setSourceLanguage] = useState('en');
  const [targetLanguage, setTargetLanguage] = useState('pt');

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'it', name: 'Italian' },
    { code: 'nl', name: 'Dutch' },
    { code: 'ru', name: 'Russian' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'zh', name: 'Chinese' },
  ];

  useEffect(() => {
    const fetchDocument = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await api.get(`/api/documents/${documentId}`);
        setDocument(response.data);
      } catch (error) {
        console.error('Error fetching document:', error);
        setError('Erro ao carregar o documento. Por favor, tente novamente.');
      } finally {
        setLoading(false);
      }
    };

    if (documentId) {
      fetchDocument();
    }
  }, [documentId]);

  const toggleParagraphSelection = (index: number) => {
    const newSelection = new Set(selectedParagraphs);
    if (newSelection.has(index)) {
      newSelection.delete(index);
    } else {
      newSelection.add(index);
    }
    setSelectedParagraphs(newSelection);
  };

  const translateSelectedParagraphs = async () => {
    if (selectedParagraphs.size === 0) return;

    try {
      setTranslating(true);
      const currentChapter = document?.chapters[selectedChapter];
      if (!currentChapter) return;

      const paragraphsToTranslate = Array.from(selectedParagraphs).map(index => ({
        index,
        text: currentChapter.paragraphs[index]
      }));

      for (const { index, text } of paragraphsToTranslate) {
        try {
          const response = await api.post('/api/translations/quick', {
            text,
            source_language: sourceLanguage,
            target_language: targetLanguage
          });

          setTranslatedParagraphs(prev => ({
            ...prev,
            [index]: response.data.translated_text
          }));
        } catch (error) {
          console.error(`Error translating paragraph ${index}:`, error);
        }
      }
    } catch (error) {
      console.error('Translation error:', error);
    } finally {
      setTranslating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-red-600 bg-red-100 rounded-lg">
        {error}
      </div>
    );
  }

  if (!document) {
    return (
      <div className="p-4 text-gray-600">
        Nenhum documento encontrado.
      </div>
    );
  }

  const chapters = document.chapters || [];
  const currentChapter = chapters[selectedChapter] || { title: 'Sem título', paragraphs: [] };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">{document.filename}</h1>
        {document.metadata && (
          <div className="text-sm text-gray-600">
            {document.metadata.author && <p>Autor: {document.metadata.author}</p>}
            {document.metadata.num_pages && <p>Páginas: {document.metadata.num_pages}</p>}
          </div>
        )}
      </div>

      {/* Controles de Tradução */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex flex-wrap gap-4 items-center">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Idioma de Origem
            </label>
            <select
              value={sourceLanguage}
              onChange={(e) => setSourceLanguage(e.target.value)}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              {languages.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>
          </div>
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Idioma de Destino
            </label>
            <select
              value={targetLanguage}
              onChange={(e) => setTargetLanguage(e.target.value)}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              {languages.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>
          </div>
          <div className="flex-none">
            <button
              onClick={translateSelectedParagraphs}
              disabled={selectedParagraphs.size === 0 || translating}
              className={`px-4 py-2 rounded-md text-white font-medium ${
                selectedParagraphs.size === 0 || translating
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-indigo-600 hover:bg-indigo-700'
              }`}
            >
              {translating ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Traduzindo...
                </span>
              ) : (
                'Traduzir Selecionados'
              )}
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-6">
        {/* Sidebar com lista de capítulos */}
        <div className="col-span-1 bg-gray-50 p-4 rounded-lg">
          <h2 className="font-semibold text-gray-700 mb-4">Capítulos</h2>
          <nav>
            {chapters.map((chapter, index) => (
              <button
                key={index}
                onClick={() => {
                  setSelectedChapter(index);
                  setSelectedParagraphs(new Set());
                  setTranslatedParagraphs({});
                }}
                className={`w-full text-left px-3 py-2 rounded-md mb-2 transition-colors ${
                  selectedChapter === index
                    ? 'bg-indigo-100 text-indigo-700'
                    : 'hover:bg-gray-100 text-gray-700'
                }`}
              >
                {chapter.title || `Capítulo ${index + 1}`}
              </button>
            ))}
          </nav>
        </div>

        {/* Área de conteúdo */}
        <div className="col-span-3">
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              {currentChapter.title || `Capítulo ${selectedChapter + 1}`}
            </h2>
            <div className="space-y-4">
              {currentChapter.paragraphs.map((paragraph, index) => (
                <div key={index} className="relative">
                  <div
                    className={`p-4 rounded-lg transition-colors ${
                      selectedParagraphs.has(index)
                        ? 'bg-indigo-50 border border-indigo-200'
                        : 'hover:bg-gray-50 border border-transparent'
                    }`}
                    onClick={() => toggleParagraphSelection(index)}
                  >
                    <p className="text-gray-700 leading-relaxed cursor-pointer">
                      {paragraph}
                    </p>
                    {translatedParagraphs[index] && (
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <p className="text-gray-600 italic">
                          {translatedParagraphs[index]}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentViewer;
