#!/bin/bash
export BACKEND_URL="http://localhost:8001"
cd /app
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
