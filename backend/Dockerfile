# Use slim Python image
FROM python:3.10-slim

# Install system dependencies for Playwright and Chromium
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip \
    libglib2.0-0 libnss3 libgdk-pixbuf2.0-0 libgtk-3-0 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libxshmfence1 libxfixes3 \
    libxext6 libxrender1 libxcb1 libx11-6 libatk1.0-0 \
    libatk-bridge2.0-0 libnspr4 libxss1 libxkbcommon0 \
    libdbus-1-3 libexpat1 libatspi2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browser dependencies
RUN python -m playwright install

# Copy app code
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
