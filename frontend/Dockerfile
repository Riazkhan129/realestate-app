FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy shared requirements from root
COPY ../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install

# Copy frontend code
COPY . .

# Expose port and run Streamlit
EXPOSE 80
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=80", "--server.address=0.0.0.0"]
