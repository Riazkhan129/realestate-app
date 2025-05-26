# Use Playwright's official image (based on Ubuntu + Python + all browser dependencies)
FROM mcr.microsoft.com/playwright/python:v1.44.0-focal

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit app code
COPY . .

# Expose Streamlit default port
EXPOSE 80

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=80", "--server.address=0.0.0.0"]
