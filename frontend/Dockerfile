FROM python:3.10-slim

# Install system dependencies needed by Playwright browsers
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libnss3-dev \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libnspr4 \
    libdbus-1-3 \
    libexpat1 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2 \
    libxcb1 \
    libatspi2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY ../requirements.txt .

# Install Python dependencies and Playwright
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install

# Copy Streamlit code
COPY . .

# Expose port and run Streamlit
EXPOSE 80
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=80", "--server.address=0.0.0.0"]
