# Use Playwright's official image (with all browser dependencies)
FROM mcr.microsoft.com/playwright/python:v1.44.0-focal

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend (Streamlit) code
COPY . .

# ✅ Add this line to include backend folder
COPY ../backend ./backend

# Expose Streamlit default port
EXPOSE 80

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=80", "--server.address=0.0.0.0"]
