# Simple production Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./
RUN mkdir -p /app/chroma_db

# Install Node.js for frontend build
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Copy built frontend to nginx directory
RUN cp -r /app/frontend/build/* /var/www/html/

# Copy nginx config
COPY frontend/nginx-single.conf /etc/nginx/sites-available/default
RUN rm -f /etc/nginx/sites-enabled/default && \
    ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Create startup script
WORKDIR /app
RUN echo '#!/bin/bash' > /start.sh && \
    echo 'python -m uvicorn main:app --host 0.0.0.0 --port 8000 &' >> /start.sh && \
    echo 'nginx -g "daemon off;"' >> /start.sh && \
    chmod +x /start.sh

# Expose ports
EXPOSE 80 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV CHROMA_PERSIST_DIRECTORY=/app/chroma_db

# Run the application
CMD ["/start.sh"]