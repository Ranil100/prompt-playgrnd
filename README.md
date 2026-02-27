# 🧪 Prompt Playground

A mini LLM experimentation application that runs the same task through three prompting strategies and compares their outputs:

- Zero-shot prompting
- Few-shot prompting
- Structured prompting

The project uses Gemini through Google's `google-genai` SDK, FastAPI for the backend, and vanilla HTML/CSS/JavaScript for the frontend.

## Features

- Run one task through three prompt strategies
- Side-by-side output comparison
- Response latency measurement
- Simple deterministic quality scoring
- Automatic winner selection
- Generated-prompt inspection
- Temperature control
- Responsive dark UI
- No framework required for the frontend

## Project structure

```text
prompt-playground/
├── backend/
│   ├── main.py
│   ├── prompts.py
│   ├── evaluator.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── experiments/
├── .env.example
├── .gitignore
└── README.md
```

## Setup

### 1. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env`:

```text
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Never commit `.env`.

### 4. Start the API

From the project root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 5. Open the UI

Open `frontend/index.html` in your browser.

If your browser blocks local requests, serve the frontend with Python:

```bash
python -m http.server 5500 --directory frontend
```

Then visit:

```text
http://127.0.0.1:5500
```

## How the evaluation works

This starter project intentionally uses a lightweight deterministic heuristic rather than asking the model to reveal hidden chain-of-thought.

The score considers:

- non-empty output
- useful list/number structure
- reasonable response length
- avoidance of unnecessary AI meta-commentary

For a production-grade evaluator, replace `backend/evaluator.py` with a benchmark-specific rubric or a separately configured judge model.

## Suggested experiments

Try the playground with:

1. Email summarization
2. Customer-support response generation
3. Text classification
4. Meeting-note extraction
5. Project-plan generation
6. Technical explanation
7. Resume bullet improvement

## Portfolio description

> Built a Prompt Evaluation Playground using FastAPI and Gemini that compares zero-shot, few-shot, and structured prompting strategies on identical tasks, measuring latency and output quality to identify the strongest prompting approach.

## Important note

The project uses "structured prompting" instead of requesting or displaying private chain-of-thought. The UI compares the final outputs and observable evaluation metrics.
