# Recommendation Letter Assistant

Developing a Context-Aware Recommendation Letter Writing Assistant: Leveraging LLM and RAG for Enhanced Text Generation.

## Features

- Upload and parse resumes
- Named Entity Recognition and selection
- Research selected entities with external context
- Generate recommendation letters
- Export letters as Word documents
- Visual resume and letter preview
- Full-text vector search by ChromaDB

## Tech Stack

- **Frontend**: React, Tailwind CSS, Vite
- **Backend**: FastAPI, SQLModel, PostgreSQL, LangChain, ChromaDB, Docker
- **LLMs**: OpenAI + BAML

## Project Structure

```
├── backend/
│   ├── src/                    # Backend source code
│   │   ├── models/             # SQLModel database models
│   │   ├── services/           # Core business logic
│   │   ├── repositories/       # DB query layer
│   │   ├── transport/          # FastAPI route handlers
│   │   ├── integrations/       # Vector store, LLM client, DB
│   │   ├── settings.py         # Configuration
│   │   └── main.py             # FastAPI app entrypoint
│   ├── .env                    # Backend environment config
│   ├── pyproject.toml          # Python dependencies
│   └── Dockerfile              # Backend Docker setup
│
├── frontend/
│   ├── src/                    # React app source code
│   │   ├── pages/              # Application views
│   │   ├── components/         # Reusable UI components
│   │   ├── main.jsx            # Frontend entrypoint
│   │   └── index.css           # Tailwind CSS styles
│   ├── .env                    # Frontend environment config
│   ├── public/
│   ├── index.html              # HTML base
│   ├── vite.config.js          # Vite configuration
│   └── Dockerfile              # Frontend Docker setup
│
├── docker-compose.yaml         # Orchestration for backend/frontend/DB
└── README.md
```

## Getting Started

### Prerequisites

- Docker
- OpenAI key

### 1. Clone the repository

```bash
git clone https://github.com/mnv/text-generation-assistant
cd recommendation-letter-assistant
```

### 2. Environment configuration

In `backend/.env`:

```
OPENAI_API_KEY=your-api-key
```

In `frontend/.env`:

```
VITE_API_BASE_URL=http://0.0.0.0:8010/api/v1
```

### 3. Add few shot examples of recommendation letters

Examples should be placed in `./data/few_shot_letters/{recommendation_type}` as `.txt` files.
`recommendation_type` can be one of: `enrollment`, `job`, `visa`.

### 4. Start Docker containers

```bash
docker compose up --build
```

- Backend: [http://0.0.0.0:8010/api/v1](http://0.0.0.0:8010/api/v1)
- Frontend: [http://127.0.0.1:8080](http://127.0.0.1:8080)

## Usage

1. Upload a resume on the **Upload** page.
2. Go to **Research**, parse the resume, and select entities.
3. Click "Start Research" to fetch additional context.
4. Navigate to **Generate** and fill in letter requirements.
5. Review or download generated letters under **Letters**.
