# Full-Stack LLM Agent with Dynamic Knowledge Base

A production-ready web application that showcases an end-to-end AI product development pipeline. This application allows users to chat with a RAG-powered LLM agent and dynamically update its knowledge base by uploading new documents.

## 🎯 Project Overview

This project demonstrates:
- **Backend API**: FastAPI with RAG pipeline using LangChain, ChromaDB, and OpenAI
- **Frontend**: Modern React application with chat interface and document upload
- **Deployment**: Docker containerization with docker-compose for local development
- **AI Integration**: Retrieval-Augmented Generation (RAG) with dynamic knowledge base updates

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │   ChromaDB      │
│                 │    │                 │    │   Vector Store  │
│  - Chat Interface│◄──►│  - RAG Pipeline │◄──►│                 │
│  - File Upload  │    │  - Document Proc│    │  - Embeddings   │
│  - Real-time UI │    │  - OpenAI API   │    │  - Persistence  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Features

### Chat Interface
- Real-time conversation with the AI agent
- Source attribution showing which documents were used
- Responsive design with modern UI/UX
- Streaming responses (optional)

### Document Upload
- Drag-and-drop PDF upload interface
- Automatic text extraction and chunking
- Vector embedding generation
- Dynamic knowledge base updates

### Backend API
- RESTful API with FastAPI
- Automatic API documentation
- Error handling and validation
- Health check endpoints

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- Docker and Docker Compose
- OpenAI API key

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd full-stack-llm-agent
```

### 2. Environment Setup
Create a `.env` file in the backend directory:
```bash
cp backend/env_example.txt backend/.env
```

Edit `backend/.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### 3. Local Development

#### Option A: Using Docker Compose (Recommended)
```bash
# Start all services
docker-compose up --build

# The application will be available at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### Option B: Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## 📚 API Endpoints

### Chat Endpoints
- `POST /chat` - Send a message to the AI agent
- `POST /chat/stream` - Stream chat response (Server-Sent Events)

### Document Management
- `POST /upload` - Upload a new document to the knowledge base
- `GET /documents` - List all uploaded documents

### Health & Status
- `GET /` - Basic health check
- `GET /health` - Detailed health status

## 🧪 Usage

1. **Start the application** using Docker Compose or manual setup
2. **Open the frontend** at http://localhost:3000
3. **Upload documents** using the Upload tab to add knowledge to the agent
4. **Chat with the agent** using the Chat tab to ask questions about uploaded documents

### Example Workflow
1. Upload a PDF document about machine learning
2. Ask: "What is machine learning?"
3. The agent will answer based on the uploaded document content
4. Upload more documents to expand the knowledge base
5. Ask follow-up questions that may require information from multiple documents

## 🏗️ Project Structure

```
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── rag_pipeline.py         # RAG implementation
│   ├── document_processor.py   # Document processing logic
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Backend container
│   └── chroma_db/             # Vector database storage
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Header.js
│   │   │   ├── ChatInterface.js
│   │   │   └── DocumentUpload.js
│   │   ├── App.js             # Main app component
│   │   └── index.js           # App entry point
│   ├── package.json           # Node.js dependencies
│   ├── Dockerfile            # Frontend container
│   └── nginx.conf            # Nginx configuration
├── docker-compose.yml         # Multi-container setup
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `CHROMA_PERSIST_DIRECTORY`: Path for ChromaDB storage (default: ./chroma_db)

### Customization
- **Chunk Size**: Modify `chunk_size` in `rag_pipeline.py` and `document_processor.py`
- **Embedding Model**: Change the model in `rag_pipeline.py`
- **UI Theme**: Customize colors and styles in `App.css`

## 🚀 Deployment

### AWS Deployment (Recommended)
1. **Build and push Docker images** to AWS ECR
2. **Deploy using AWS App Runner** or **Elastic Beanstalk**
3. **Set environment variables** in the deployment configuration
4. **Configure domain and SSL** if needed

### Other Cloud Providers
- **Google Cloud Run**: Deploy containers directly
- **Azure Container Instances**: Similar to AWS App Runner
- **Heroku**: Use container deployment

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### API Testing
Use the interactive API documentation at http://localhost:8000/docs

## 📈 Performance Considerations

- **Chunk Size**: Optimize for your document types (default: 1000 characters)
- **Embedding Model**: Consider using more powerful models for better accuracy
- **Caching**: Implement Redis for frequently accessed embeddings
- **Scaling**: Use load balancers and multiple backend instances

## 🔒 Security Considerations

- **API Keys**: Store securely using environment variables
- **File Upload**: Validate file types and sizes
- **Rate Limiting**: Implement rate limiting for API endpoints
- **CORS**: Configure CORS properly for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is correctly set in the `.env` file
   - Check that you have sufficient API credits

2. **ChromaDB Connection Issues**
   - Ensure the `chroma_db` directory has proper permissions
   - Try deleting the directory to reset the database

3. **Frontend Not Loading**
   - Check that the backend is running on port 8000
   - Verify CORS settings in the backend

4. **Document Upload Fails**
   - Ensure the file is a valid PDF
   - Check file size limits (10MB default)

### Getting Help
- Check the logs: `docker-compose logs backend` or `docker-compose logs frontend`
- Review the API documentation at http://localhost:8000/docs
- Open an issue on GitHub for bugs or feature requests

## 🎉 Success Criteria

✅ **Deployed Application**: Accessible via public URL  
✅ **Interactive Chat**: Users can engage with the RAG agent  
✅ **Dynamic Upload**: Users can upload documents and expand knowledge  
✅ **Containerized**: Full Docker setup with docker-compose  
✅ **Production Ready**: Error handling, logging, and monitoring  

This project successfully demonstrates modern AI product development with a complete full-stack implementation!
