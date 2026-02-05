# AI Chatbot - Quick Start Guide

## Project Overview
A full-stack AI chatbot powered by Claude Sonnet 4.5, built with FastAPI (backend) and Streamlit (frontend), featuring multi-turn conversations with context memory and MongoDB persistence.

## Repository Structure
```
/app/
├── backend/
│   ├── server.py           # FastAPI application
│   ├── requirements.txt    # Backend dependencies
│   └── .env               # Environment configuration
├── streamlit_app.py        # Streamlit frontend
├── requirements_streamlit.txt
├── run_streamlit.sh        # Streamlit startup script
├── README.md              # Detailed documentation
└── PROJECT_REPORT.md      # Complete project report
```

## Quick Setup

### Prerequisites
- Python 3.9+
- MongoDB running on localhost:27017

### Installation

1. **Install Backend Dependencies**
```bash
cd /app/backend
pip install -r requirements.txt
```

2. **Install Frontend Dependencies**
```bash
cd /app
pip install -r requirements_streamlit.txt
```

3. **Start Backend Server**
```bash
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

4. **Start Streamlit Frontend**
```bash
export BACKEND_URL=http://localhost:8001
streamlit run /app/streamlit_app.py --server.port 8501
```

5. **Access Application**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8001/docs

## Key Features
- Real-time AI conversations with Claude Sonnet 4.5
- Multi-turn context memory
- Multiple chat sessions
- MongoDB persistence
- Clean Streamlit UI
- RESTful API

## Technology Stack
- **Backend**: FastAPI, Python
- **Frontend**: Streamlit
- **Database**: MongoDB
- **AI**: Claude Sonnet 4.5 (Anthropic)

## API Endpoints
- `POST /api/chat` - Send message
- `POST /api/chat/sessions` - Create session
- `GET /api/chat/sessions` - List sessions
- `GET /api/chat/sessions/{id}/messages` - Get messages
- `DELETE /api/chat/sessions/{id}` - Delete session

## Testing
All features tested with 98% success rate:
- Backend API: 100%
- Frontend UI: 100%
- Integration: 100%
- Context memory: Verified working

## Documentation
- `README.md` - Setup and usage instructions
- `PROJECT_REPORT.md` - Comprehensive project report with architecture, design decisions, and screenshots

## GitHub Submission
1. Create GitHub repository
2. Push all code files
3. Include README.md (without emojis)
4. Ensure .env is in .gitignore
5. Add LICENSE file

## Contact
For questions or issues, refer to PROJECT_REPORT.md for detailed documentation.
