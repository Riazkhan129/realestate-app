#!/bin/bash

# Start FastAPI on port 8000 in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on port 8501 (foreground)
streamlit run streamlit_app.py --server.port 80 --server.address 0.0.0.0
