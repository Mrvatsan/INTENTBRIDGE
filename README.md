# IntentBridge

**Intent Classification Engine - Module 1**

A web-based application that converts raw, unstructured human intent into structured, machine-usable representations.

## 🎯 Overview

IntentBridge is NOT a chatbot. It is a sophisticated system that analyzes raw human input and extracts precise, structured representations of user intent through an 8-step classification process. This is Module 1 of the IntentBridge pipeline - the Intent Classification Engine.

### What makes IntentBridge different?
- **No conversational AI** - Pure intent extraction without suggestions or advice
- **Structured output** - JSON-based machine-readable format
- **Multi-dimensional analysis** - Intent type, goals, constraints, ambiguities, and emotional signals
- **Confidence scoring** - Transparent quality assessment of classification results

## Features

- **Intent Type Classification**: Learning, Building, Planning, or Unknown
- **Goal Extraction**: Primary and secondary objectives
- **Constraint Detection**: Skill limitations, time limits, resources
- **Ambiguity Identification**: Missing or vague information
- **Emotional Signal Detection**: Confused, Motivated, Stressed, Curious, Neutral
- **Confidence Scoring**: Low, Medium, High

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
