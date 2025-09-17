import os
import logging
from typing import List, Tuple, AsyncGenerator, Dict, Any
import asyncio
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import openai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        """Initialize the RAG pipeline with ChromaDB and OpenAI"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key or self.openai_api_key == "your_openai_api_key_here":
            logger.warning("OPENAI_API_KEY not properly set. RAG functionality will be limited.")
            self.openai_api_key = None
        
        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.chroma_persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        self.client = chromadb.PersistentClient(
            path=self.chroma_persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        logger.info("RAG pipeline initialized successfully")

    async def add_documents(self, documents: List[Document], metadata: Dict[str, Any] = None):
        """Add documents to the vector store"""
        try:
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            if not chunks:
                logger.warning("No chunks created from documents")
                return
            
            # Prepare data for ChromaDB
            texts = [chunk.page_content for chunk in chunks]
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    "source": chunk.metadata.get("source", "unknown"),
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                if metadata:
                    chunk_metadata.update(metadata)
                
                metadatas.append(chunk_metadata)
                ids.append(f"{chunk_metadata['source']}_{i}")
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(texts).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(chunks)} chunks to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise

    async def query(self, question: str, n_results: int = 5) -> Tuple[str, List[str]]:
        """Query the RAG pipeline and return response with sources"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([question]).tolist()[0]
            
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # Extract relevant documents
            relevant_docs = results["documents"][0] if results["documents"] else []
            sources = []
            
            if results["metadatas"] and results["metadatas"][0]:
                sources = [meta.get("source", "unknown") for meta in results["metadatas"][0]]
            
            # Create context from retrieved documents
            context = "\n\n".join(relevant_docs) if relevant_docs else "No relevant context found."
            
            # Generate response using OpenAI
            response = await self._generate_response(question, context)
            
            return response, sources
            
        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            raise

    async def query_stream(self, question: str, n_results: int = 5) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream query response from the RAG pipeline"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([question]).tolist()[0]
            
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # Extract relevant documents
            relevant_docs = results["documents"][0] if results["documents"] else []
            sources = []
            
            if results["metadatas"] and results["metadatas"][0]:
                sources = [meta.get("source", "unknown") for meta in results["metadatas"][0]]
            
            # Create context from retrieved documents
            context = "\n\n".join(relevant_docs) if relevant_docs else "No relevant context found."
            
            # Stream response using OpenAI
            async for chunk in self._generate_response_stream(question, context):
                yield chunk
                
        except Exception as e:
            logger.error(f"Error in streaming RAG query: {e}")
            yield {"error": str(e)}

    async def _generate_response(self, question: str, context: str) -> str:
        """Generate response using OpenAI API"""
        if not self.openai_api_key:
            return f"""I can see you asked: "{question}"

However, I need to be configured with a valid OpenAI API key to provide intelligent responses. 

The context I found from the knowledge base is:
{context}

To enable full AI functionality, please:
1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Update the OPENAI_API_KEY in the environment configuration
3. Restart the application

For now, I can only show you the relevant context from uploaded documents."""

        try:
            prompt = f"""You are a helpful AI assistant with access to a knowledge base. 
            Use the following context to answer the user's question. If the context doesn't contain 
            relevant information, say so and provide a helpful response based on your general knowledge.

            Context:
            {context}

            Question: {question}

            Answer:"""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error while generating a response: {str(e)}"

    async def _generate_response_stream(self, question: str, context: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream response using OpenAI API"""
        try:
            prompt = f"""You are a helpful AI assistant with access to a knowledge base. 
            Use the following context to answer the user's question. If the context doesn't contain 
            relevant information, say so and provide a helpful response based on your general knowledge.

            Context:
            {context}

            Question: {question}

            Answer:"""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield {
                        "type": "content",
                        "content": chunk.choices[0].delta.content
                    }
            
            yield {"type": "done"}
            
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            yield {"type": "error", "content": str(e)}

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store collection"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}
