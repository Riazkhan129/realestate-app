#!/bin/bash

# Start FastAPI in the background on port 8000
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on the Railway public port
streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port 8501

