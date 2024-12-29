# Tradutor Profissional

Uma aplicação de tradução profissional que utiliza modelos de linguagem avançados para auxiliar tradutores, oferecendo traduções precisas e personalizáveis.

## Status do Projeto

- **Backend**: ✓ Deployed em https://tradutor-profissional-api.onrender.com
- **Frontend**: ✓ Deployed em https://frontend-pi-woad.vercel.app

## Tecnologias Utilizadas

### Backend
- FastAPI (Framework web assíncrono)
- OpenAI GPT-4o (Motor de tradução principal)
- Python 3.12+
- PostgreSQL (Sistema de banco de dados)
- Alembic (Sistema de migração)
- Render (Plataforma de deploy)

### Frontend
- React 18 com TypeScript
- Tailwind CSS
- Sistema de upload com drag-and-drop
- Visualizador de documentos integrado
- Interface responsiva
- Vercel (Plataforma de deploy)

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
- ✓ Deploy automático no Vercel e Render
- ✓ Integração frontend-backend via CORS

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
DATABASE_URL=sua_url_postgres_aqui
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

2. **Configurar variáveis de ambiente**:
Crie um arquivo `.env` na pasta frontend com:
```env
REACT_APP_API_URL=http://localhost:8000
```

3. **Iniciar o servidor de desenvolvimento**:
```bash
npm start
```

O frontend estará disponível em `http://localhost:3000`

## Deploy

### Backend (Render)

O backend está atualmente deployed em: https://tradutor-profissional-api.onrender.com

Para fazer deploy de alterações:
1. Faça commit das mudanças
2. Push para o GitHub
3. O Render fará o deploy automaticamente

### Frontend (Vercel)

O frontend está atualmente deployed em: https://frontend-pi-woad.vercel.app

Para fazer deploy de alterações:
1. Faça commit das mudanças
2. Push para o GitHub
3. O Vercel fará o deploy automaticamente

## Limitações Conhecidas

1. Tempo de cold start no Render (plano gratuito)
2. Limite de requisições da API OpenAI
3. Sem sistema de autenticação
4. Suporte apenas para tradução inglês-português

## Próximas Funcionalidades

- [ ] Sistema de histórico de traduções
- [ ] Personalização de estilo de tradução
- [ ] Interface de revisão avançada
- [ ] Suporte a múltiplos formatos de arquivo
- [ ] Sistema de feedback e aprendizado contínuo
- [ ] Sistema de autenticação
- [ ] Suporte a mais pares de idiomas

## Contribuição

Contribuições são bem-vindas! Por favor, leia nosso guia de contribuição antes de submeter um Pull Request.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.
