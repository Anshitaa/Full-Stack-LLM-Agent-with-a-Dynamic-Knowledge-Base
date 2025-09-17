import os
import logging
from typing import List, Dict, Any
import asyncio
from io import BytesIO
import PyPDF2
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        """Initialize the document processor"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.rag_pipeline = None
        self.processed_documents = []
        
    async def initialize_rag_pipeline(self, rag_pipeline: RAGPipeline):
        """Initialize the RAG pipeline reference"""
        self.rag_pipeline = rag_pipeline

    async def process_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process a document and add it to the knowledge base"""
        try:
            # Extract text from PDF
            text = await self._extract_text_from_pdf(file_content)
            
            if not text.strip():
                raise ValueError("No text content found in the document")
            
            # Create document object
            document = Document(
                page_content=text,
                metadata={
                    "source": filename,
                    "type": "pdf",
                    "processed_at": str(asyncio.get_event_loop().time())
                }
            )
            
            # Add to RAG pipeline
            if self.rag_pipeline:
                await self.rag_pipeline.add_documents([document], {"filename": filename})
            
            # Track processed document
            self.processed_documents.append({
                "filename": filename,
                "text_length": len(text),
                "chunks": len(self.text_splitter.split_documents([document]))
            })
            
            logger.info(f"Successfully processed document: {filename}")
            
            return {
                "filename": filename,
                "text_length": len(text),
                "chunks_created": len(self.text_splitter.split_documents([document])),
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing document {filename}: {e}")
            raise

    async def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text content from PDF bytes"""
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all processed documents"""
        return self.processed_documents.copy()

    async def get_document_info(self, filename: str) -> Dict[str, Any]:
        """Get information about a specific document"""
        for doc in self.processed_documents:
            if doc["filename"] == filename:
                return doc
        return {"error": "Document not found"}

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        total_docs = len(self.processed_documents)
        total_text_length = sum(doc["text_length"] for doc in self.processed_documents)
        total_chunks = sum(doc["chunks"] for doc in self.processed_documents)
        
        return {
            "total_documents": total_docs,
            "total_text_length": total_text_length,
            "total_chunks": total_chunks,
            "average_text_length": total_text_length / total_docs if total_docs > 0 else 0,
            "average_chunks_per_doc": total_chunks / total_docs if total_docs > 0 else 0
        }
