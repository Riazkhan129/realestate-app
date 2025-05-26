FROM python:3.10-slim

# Install necessary system libraries for Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip \
    libglib2.0-0 libnss3 libgdk-pixbuf2.0-0 libgtk-3-0 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libxshmfence1 libxfixes3 \
    libxext6 libxrender1 libxcb1 libx11-6 libatk1.0-0 \
    libatk-bridge2.0-0 libnspr4 libxss1 libxkbcommon0 \
    libdbus-1-3 libexpat1 libatspi2.0-0 libgobject-2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
