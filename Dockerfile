# Use Python base image
FROM python:3.9-slim

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend

# Copy frontend files (to be served by Flask or directly as static files)
COPY frontend/ ./frontend

# Expose the Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "backend/app.py"]
