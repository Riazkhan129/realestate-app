
import subprocess
import threading
import uvicorn
from main import app
import streamlit.web.cli as stcli
import sys

# Install Playwright browsers
subprocess.run(["playwright", "install", "--with-deps"])

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Use port 8001 for FastAPI

def run_streamlit():
    sys.argv = ["streamlit", "run", "streamlit_app.py", "--server.port=80"]
    stcli.main()

if __name__ == "__main__":
    threading.Thread(target=run_fastapi, daemon=True).start()
    run_streamlit()
