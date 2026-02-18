# IntentBridge Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)

> Bridge the gap between vague ideas and structured, actionable execution plans.

IntentBridge is a production-grade AI system that transforms conceptual ideas into comprehensive technical roadmaps and project scaffolding using a multi-module AI pipeline powered by Google Gemini.

---

## Product Overview

The platform consists of a multi-module AI pipeline:

| Module | Purpose |
|---|---|
| **Intent Classifier** | Parses raw text to detect core goals and constraints |
| **Ambiguity Resolver** | Identifies missing info and generates clarifying questions |
| **Execution Planner** | Produces comprehensive technical roadmaps and requirement specs |
| **Build Engine** | Generates boilerplate code and project scaffolding |

## Architecture

- **Frontend**: React 18 + Tailwind CSS
- **Backend**: FastAPI (Python 3.9+)
- **AI Core**: Google Gemini LLM (with mock mode for offline dev)
- **Orchestrator**: Modular Python layer for pipeline management
- **Database**: PostgreSQL via SQLAlchemy ORM

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose (optional)

### Local Setup (Backend)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env  # Edit with your API key
python main.py
```

### Local Setup (Frontend)
```bash
cd frontend
npm install
npm start
```

### Docker Setup
```bash
docker-compose up --build
```

This launches the full stack: backend (port 8000), frontend (port 3000), and PostgreSQL (port 5432).

## API Reference

### POST `/api/v1/process`

Process a user's idea through the AI pipeline.

**Request Body:**
```json
{
  "session_id": "unique-session-id",
  "user_input": "I want to build a todo app",
  "history": []
}
```

**Response (clarification needed):**
```json
{
  "status": "clarification_needed",
  "intent": { ... },
  "questions": ["What platform?", "What tech stack?"],
  "analysis": "..."
}
```

**Response (plan generated):**
```json
{
  "status": "plan_generated",
  "intent": { ... },
  "plan": { "product_definition": { ... }, "technical_architecture": { ... } }
}
```

## Testing Strategy

- **Unit Tests**: Test individual AI modules with mock LLM responses
- **Integration Tests**: Verify the workflow from input to plan generation
- **E2E**: Use Playwright/Cypress for frontend-to-backend validation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.