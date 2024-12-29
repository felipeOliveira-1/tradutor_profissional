# Tradutor Profissional

Uma aplicação de tradução profissional que utiliza modelos de linguagem avançados para auxiliar tradutores, oferecendo traduções precisas e personalizáveis.

## Tecnologias Utilizadas

### Backend
- FastAPI (Framework web assíncrono)
- OpenAI GPT-4o Optimized (Motor de tradução principal)
- Python 3.12+
- PostgreSQL (Sistema de banco de dados implementado)
- Alembic (Sistema de migração)

### Frontend
- React 18 com TypeScript
- Tailwind CSS
- Sistema de upload com drag-and-drop
- Visualizador de documentos integrado
- Interface responsiva

## Estrutura do Projeto

```
tradutor_profissional/
├── backend/               
│   ├── main.py           # API endpoints
│   ├── models.py         # Modelos do banco de dados
│   ├── schemas.py        # Schemas Pydantic
│   ├── database.py       # Configuração PostgreSQL
│   ├── document_processor.py # Processamento de documentos
│   ├── alembic/          # Sistema de migração
│   ├── requirements.txt  # Dependências Python
│   └── .env             # Variáveis de ambiente
├── frontend/            
│   ├── src/             # Código fonte React
│   ├── package.json     # Dependências Node.js
│   └── tailwind.config.js
└── docs/                # Documentação do projeto
```

## Recursos Implementados
- ✓ Upload e processamento de documentos (PDF, DOCX, TXT)
- ✓ Tradução assíncrona de textos
- ✓ Navegação por capítulos
- ✓ Interface de visualização de documentos
- ✓ Seleção de idiomas de origem e destino
- ✓ Sistema de gerenciamento de capítulos
- ✓ Processamento otimizado de documentos

## Configuração e Instalação

### Backend

1. **Configurar ambiente virtual**:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac
```

2. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

3. **Configurar variáveis de ambiente**:
Crie um arquivo `.env` na pasta backend com:
```env
OPENAI_API_KEY=sua_chave_api_aqui
```

4. **Iniciar o servidor**:
```bash
python -m uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

### Frontend

1. **Instalar dependências**:
```bash
cd frontend
npm install
```

2. **Iniciar o servidor de desenvolvimento**:
```bash
npm start
```

O frontend estará disponível em `http://localhost:3000`

## API Endpoints

### Tradução
- `POST /api/translate`
  - Traduz um texto
  - Corpo da requisição:
    ```json
    {
      "text": "Text to translate",
      "source_lang": "en",
      "target_lang": "pt"
    }
    ```
  - Resposta:
    ```json
    {
      "translated_text": "Texto traduzido"
    }
    ```

## Deploy

### Backend (Render)

1. Faça login no [Render](https://render.com)
2. Conecte seu repositório GitHub
3. Clique em "New +" e selecione "Blueprint"
4. Selecione o repositório do projeto
5. O Render irá automaticamente:
   - Criar o banco de dados PostgreSQL
   - Configurar as variáveis de ambiente
   - Fazer deploy da API

### Frontend (Vercel)

1. Faça login no [Vercel](https://vercel.com)
2. Importe o projeto do GitHub
3. Configure a variável de ambiente:
   - `REACT_APP_API_URL`: URL do backend no Render
4. Clique em "Deploy"

### Variáveis de Ambiente Necessárias

#### Backend (Render)
- `DATABASE_URL`: Configurado automaticamente
- `OPENAI_API_KEY`: Sua chave da API OpenAI
- `PORT`: Configurado automaticamente

#### Frontend (Vercel)
- `REACT_APP_API_URL`: URL do backend

## Funcionalidades Planejadas

- [ ] Sistema de histórico de traduções
- [ ] Personalização de estilo de tradução
- [ ] Interface de revisão avançada
- [ ] Suporte a múltiplos formatos de arquivo
- [ ] Sistema de feedback e aprendizado contínuo

## Contribuição

Contribuições são bem-vindas! Por favor, leia nosso guia de contribuição antes de submeter um Pull Request.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.
