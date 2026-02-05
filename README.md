# AI Chatbot Application

A full-stack AI chatbot application powered by Claude Sonnet 4.5, built with FastAPI, Streamlit, and MongoDB.

## Features

- Real-time AI conversations using Claude Sonnet 4.5
- Multi-turn conversation with context memory
- Chat history persistence in MongoDB
- Multiple chat sessions management
- Clean and intuitive Streamlit UI
- RESTful API with FastAPI

## System Architecture

### Backend (FastAPI)
- RESTful API endpoints for chat operations
- MongoDB integration for data persistence
- Claude Sonnet 4.5 integration via Emergent LLM Key
- Async operations for better performance

### Frontend (Streamlit)
- Interactive chat interface
- Session management sidebar
- Real-time message display
- Chat history navigation

### Database (MongoDB)
- Collections:
  - `chat_sessions`: Stores chat session metadata
  - `chat_messages`: Stores all messages with session references

## Technology Stack

- **Backend**: FastAPI, Python 3.9+
- **Frontend**: Streamlit
- **Database**: MongoDB
- **AI Model**: Claude Sonnet 4.5 (Anthropic)
- **Integration**: emergentintegrations library

## Installation & Setup

### Prerequisites
- Python 3.9 or higher
- MongoDB running on localhost:27017
- Internet connection for API calls

### Backend Setup

1. Navigate to backend directory:
```bash
cd /app/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Environment variables are configured in `/app/backend/.env`:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
CORS_ORIGINS=*
EMERGENT_LLM_KEY=sk-emergent-7F539F03e27F977149
```

4. Start the FastAPI server:
```bash
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

The backend API will be available at `http://localhost:8001`

### Streamlit Frontend Setup

1. Install Streamlit dependencies:
```bash
pip install -r /app/requirements_streamlit.txt
```

2. Set the backend URL environment variable:
```bash
export BACKEND_URL=http://localhost:8001
```

3. Run the Streamlit app:
```bash
streamlit run /app/streamlit_app.py --server.port 8501
```

The Streamlit UI will be available at `http://localhost:8501`

## API Endpoints

### Chat Endpoints

- `POST /api/chat/sessions` - Create a new chat session
- `GET /api/chat/sessions` - Get all chat sessions
- `GET /api/chat/sessions/{session_id}/messages` - Get messages for a session
- `POST /api/chat` - Send a message and get AI response
- `DELETE /api/chat/sessions/{session_id}` - Delete a session

### Example API Usage

```bash
# Create a new session
curl -X POST http://localhost:8001/api/chat/sessions

# Send a message
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?", "session_id": "your-session-id"}'
```

## Usage

1. Start the backend server (FastAPI)
2. Start the Streamlit frontend
3. Open browser to `http://localhost:8501`
4. Click "New Chat" to start a conversation
5. Type your message and press Enter
6. The AI will respond using Claude Sonnet 4.5
7. Switch between chats using the sidebar

## Project Structure

```
/app/
├── backend/
│   ├── server.py           # FastAPI application
│   ├── requirements.txt    # Backend dependencies
│   └── .env               # Environment variables
├── streamlit_app.py       # Streamlit frontend
├── requirements_streamlit.txt  # Streamlit dependencies
└── README.md              # This file
```

## Design Decisions

1. **FastAPI for Backend**: Chosen for its async support, automatic API documentation, and excellent performance.

2. **Streamlit for Frontend**: Provides rapid development of interactive UIs with minimal code, perfect for AI applications.

3. **MongoDB for Persistence**: NoSQL database allows flexible schema for chat messages and sessions.

4. **Claude Sonnet 4.5**: Latest AI model from Anthropic, providing high-quality conversational responses.

5. **Session-based Architecture**: Each chat session maintains its own context, allowing multiple independent conversations.

6. **Emergent LLM Key**: Universal API key simplifying integration with multiple LLM providers.

## Testing

Test the backend API:
```bash
# Check if server is running
curl http://localhost:8001/api/

# Create a test session and send a message
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

## Troubleshooting

- **MongoDB Connection Error**: Ensure MongoDB is running on localhost:27017
- **API Key Error**: Verify EMERGENT_LLM_KEY is set in backend/.env
- **CORS Issues**: Backend allows all origins by default (CORS_ORIGINS=*)
- **Port Already in Use**: Change ports in startup commands if 8001 or 8501 are occupied

## License

MIT License