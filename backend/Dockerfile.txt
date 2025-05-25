FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy shared requirements from root
COPY ../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install

# Copy backend code
COPY . .

# Expose port and run FastAPI
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

