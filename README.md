# IntentBridge Platform

IntentBridge is a production-grade AI system designed to bridge the gap between vague conceptual ideas and structured, actionable execution plans and builds.

## 📌 Product Overview
The platform consists of a multi-module AI pipeline:
1. **Intent Classifier**: Parses raw text to detect core goals and constraints.
2. **Ambiguity Resolver**: Identifies missing critical information and generates clarifying questions.
3. **Execution Planner**: Produces comprehensive technical roadmaps and requirement specs.
4. **Build Engine**: Generates boilerplate code and project scaffolding automatically.

## 🏗 Architecture Design
- **Frontend**: React + Tailwind CSS
- **Backend**: FastAPI (Python)
- **AI Core**: Google Gemini LLM
- **Orchestrator**: Modular Python layer for pipeline management
- **Database**: PostgreSQL (planned)

## 🚀 Deployment Guide

### Local Setup (Backend)
1. Navigate to `/backend`
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Set `GOOGLE_API_KEY` in `.env`
5. Run server: `python main.py`

### Local Setup (Frontend)
1. Navigate to `/frontend`
2. Install dependencies: `npm install`
3. Run dev server: `npm start`

### Docker setup
Run `docker-compose up --build` to launch the whole stack.

## 🧪 Testing Strategy
- **Unit Tests**: Test individual AI modules with mock LLM responses.
- **Integration Tests**: Verify the workflow from input to plan generation.
- **E2E**: Use Playwright/Cypress for frontend-to-backend validation.
