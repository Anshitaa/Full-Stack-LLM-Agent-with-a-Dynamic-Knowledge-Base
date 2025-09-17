from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import json
import asyncio
from typing import List, Optional
import logging

from rag_pipeline import RAGPipeline
from document_processor import DocumentProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLM Agent with Dynamic Knowledge Base",
    description="A RAG-powered LLM agent that can answer questions and learn from uploaded documents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline and document processor
rag_pipeline = None
document_processor = None

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG pipeline and document processor on startup"""
    global rag_pipeline, document_processor
    try:
        rag_pipeline = RAGPipeline()
        document_processor = DocumentProcessor()
        await document_processor.initialize_rag_pipeline(rag_pipeline)
        logger.info("RAG pipeline and document processor initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG pipeline: {e}")
        raise

# Pydantic models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[str]

class UploadResponse(BaseModel):
    status: str
    filename: str
    message: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "LLM Agent with Dynamic Knowledge Base API is running!"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "rag_pipeline": rag_pipeline is not None,
        "document_processor": document_processor is not None
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat with the RAG agent"""
    if not rag_pipeline:
        raise HTTPException(status_code=500, detail="RAG pipeline not initialized")
    
    try:
        response, sources = await rag_pipeline.query(message.message)
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/chat/stream")
async def chat_stream(message: ChatMessage):
    """Stream chat response from the RAG agent"""
    if not rag_pipeline:
        raise HTTPException(status_code=500, detail="RAG pipeline not initialized")
    
    async def generate():
        try:
            async for chunk in rag_pipeline.query_stream(message.message):
                yield f"data: {json.dumps(chunk)}\n\n"
        except Exception as e:
            logger.error(f"Error in streaming chat: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a new document to add to the knowledge base"""
    if not document_processor:
        raise HTTPException(status_code=500, detail="Document processor not initialized")
    
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        content = await file.read()
        
        # Process the document
        result = await document_processor.process_document(content, file.filename)
        
        return UploadResponse(
            status="success",
            filename=file.filename,
            message=f"Document '{file.filename}' has been successfully added to the knowledge base"
        )
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.get("/documents")
async def list_documents():
    """List all documents in the knowledge base"""
    if not document_processor:
        raise HTTPException(status_code=500, detail="Document processor not initialized")
    
    try:
        documents = await document_processor.list_documents()
        return {"documents": documents}
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
