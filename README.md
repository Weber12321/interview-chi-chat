# AI Interview System

A multi-agent workflow system for conducting technical interviews using OpenAI's agent framework.

## Features

- Three specialized AI agents:
  - HR Agent: Analyzes CVs and job descriptions to create interview agendas
  - Interviewer Agent: Conducts technical interviews with dynamic question generation
  - Supervisor Agent: Evaluates interview performance and provides feedback
- PDF and web page parsing capabilities
- Vector search for related candidate information
- Web-based interface for configuration and interaction

## Project Structure

```
interview-chi-chat/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── services/
│   ├── tests/
│   └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
└── requirements.txt
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Initialize the database:
```bash
python backend/app/db/init_db.py
```

4. Run the backend:
```bash
uvicorn backend.main:app --reload
```

## Frontend Options

The frontend can be built using either:
1. React with Material-UI
2. Vue.js with Vuetify
3. Svelte with SvelteKit

## License

MIT License
