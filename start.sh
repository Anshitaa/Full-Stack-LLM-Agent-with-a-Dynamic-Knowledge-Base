#!/bin/bash

# Full-Stack LLM Agent Startup Script

echo "🚀 Starting Full-Stack LLM Agent with Dynamic Knowledge Base"
echo "=============================================================="

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Environment file not found. Creating from template..."
    cp backend/env_example.txt backend/.env
    echo "📝 Please edit backend/.env and add your OpenAI API key"
    echo "   OPENAI_API_KEY=your_openai_api_key_here"
    echo ""
    read -p "Press Enter after adding your API key..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build

echo "✅ Application started successfully!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the application"
