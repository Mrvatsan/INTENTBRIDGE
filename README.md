# IntentBridge

**Modular Intent Processing Pipeline**

A web-based system that processes raw, unstructured human intent into structured, resolved representations.

## 📁 Project Structure

- `app.py`: Core Flask application with Module 1 and Module 2 engines.
- `constants.py`: Centralized application constants and configuration.
- `static/`: Frontend assets (JavaScript logic and CSS styles).
- `templates/`: HTML templates for the web interface.
- `requirements.txt`: Python package dependencies.

## 🎯 Overview

IntentBridge is a multi-stage pipeline designed to analyze human input and extract precise, machine-usable data. It currently consists of two modules:

1.  **Intent Classification Engine (Module 1)**: Converts raw input into a structured JSON representation (Intent Type, Goals, Constraints, Ambiguities, Emotions).
2.  **Ambiguity Resolution Engine (Module 2)**: Processes the output of Module 1 to resolve ambiguities through either targeted clarification questions or neutral assumptions.

### What makes IntentBridge different?
- **No conversational AI** - Pure intent extraction and refinement without suggestions or advice.
- **Structured output** - Fully valid JSON machine-readable formats.
- **Disciplined Resolution** - Follows strict logic to decide between asking questions or making assumptions.
- **Multi-dimensional analysis** - Covers intent type, goals, constraints, ambiguities, and emotional signals.

## Features

### Module 1: Classification
- **Intent Type**: Learning, Building, Planning, or Unknown
- **Goal Extraction**: Primary and secondary objectives
- **Constraint Detection**: Skill limitations, time limits, resources
- **Ambiguity Identification**: Missing or vague information
- **Emotional Signal Detection**: Confused, Motivated, Stressed, Curious, Neutral
- **Confidence Scoring**: Low, Medium, High

### Module 2: Resolution
- **Blocking Detection**: Identifies if ambiguities prevent action planning.
- **Clarification Generation**: Selects the single most critical blocking ambiguity and generates one precise question.
- **Assumption Modeling**: Generates reasonable, neutral assumptions for non-blocking ambiguities.

## API Specification

### 1. Intent Classification
- **Endpoint**: `/api/classify`
- **Method**: `POST`
- **Payload**: `{ "user_input": "string" }`

### 2. Ambiguity Resolution
- **Endpoint**: `/api/resolve`
- **Method**: `POST`
- **Payload**: Structured intent object from Module 1.

## 🧠 Philosophy

IntentBridge operates on the principle of **Decision Transparency**. Unlike standard conversational AIs that may "hallucinate" or make invisible choices, IntentBridge explicitly identifies what it knows and what it needs. Every assumption made by the system is neutral, non-binding, and reversible, ensuring the user remains the ultimate authority in the intent refinement process.

## Installation

1. **Clone or navigate to the project directory**:
```bash
cd d:\INTENTBRIDGE
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Start the Flask server**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://localhost:5000
```

## API Usage

### Classify Intent Endpoint

**URL**: `/api/classify`  
**Method**: `POST`  
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "user_input": "I want to learn machine learning but I'm a beginner"
}
```

**Response**:
```json
{
  "intent_type": "Learning",
  "primary_goal": "I want to learn machine learning but I'm a beginner",
  "secondary_goals": [],
  "constraints": ["Limited or no prior experience mentioned"],
  "ambiguities": ["Input too brief - scope unclear"],
  "emotional_signal": "Neutral",
  "confidence_level": "Medium"
}
```

### Health Check Endpoint

**URL**: `/health`  
**Method**: `GET`

**Response**:
```json
{
  "status": "healthy",
  "module": "Intent Classification Engine",
  "version": "1.0.0"
}
```

## Project Structure

```
INTENTBRIDGE/
│
├── app.py                 # Flask backend with classification engine
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/
│   └── index.html        # Frontend interface
│
└── static/
    ├── style.css         # Styling
    └── script.js         # Frontend logic
```

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **API**: RESTful JSON API

## Module Specification

This module follows a strict 8-step classification process:

1. Read input literally
2. Classify intent type
3. Extract primary goal
4. Identify secondary goals
5. Extract explicit constraints
6. Detect ambiguities
7. Detect emotional signal
8. Assign confidence level

## License

Internal module - IntentBridge System

## Version

1.0.0 - January 2026
