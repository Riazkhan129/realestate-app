import subprocess
import threading

def run_fastapi():
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

def run_streamlit():
    subprocess.run(["streamlit", "run", "streamlit_app.py", "--server.port=8000", "--server.enableCORS=false"])

# Run Streamlit on the exposed port (8000), FastAPI on background (choose different port like 9000)
threading.Thread(target=run_fastapi).start()
run_streamlit()
