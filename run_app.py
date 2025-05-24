import threading
import uvicorn
from main import app
import streamlit.web.cli as stcli
import sys

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8001)  # ← not 8000, try 8001

def run_streamlit():
    sys.argv = ["streamlit", "run", "streamlit_app.py", "--server.port=80"]
    stcli.main()

if __name__ == "__main__":
    threading.Thread(target=run_fastapi, daemon=True).start()
    run_streamlit()
