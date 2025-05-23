
#!/bin/bash

# Start FastAPI in the background
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit (bind to Railway's default port 8080)
streamlit run frontend/streamlit_app.py --server.port 8080 --server.address 0.0.0.0
