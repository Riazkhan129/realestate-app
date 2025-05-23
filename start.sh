#!/bin/bash

# Run FastAPI in the background (port 8000)
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Run Streamlit in foreground (main app on port 80)
streamlit run streamlit_app.py --server.port 80 --server.enableCORS false
