import os
import groq
from sentence_transformers import SentenceTransformer
import numpy as np

from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Groq(api_key=GROQ_API_KEY)

# Initialize Sentence Transformer model for embeddings
# using a small, fast model
try:
    print("Loading embedding model (this may take a moment)...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Embedding model loaded successfully.")
except Exception as e:
    print(f"Warning: Could not load embedding model: {e}")
    embedding_model = None

# Store resume chunks and their embeddings
knowledge_base = {
    "chunks": [],
    "embeddings": None
}

def initialize_knowledge_base(resume_text):
    """
    Initializes the knowledge base by chunking the resume text and creating embeddings.
    """
    global knowledge_base
    if not resume_text:
        return

    # Simple chunking by paragraphs or newlines for now
    chunks = [chunk.strip() for chunk in resume_text.split('\n\n') if chunk.strip()]
    
    # If chunks are too small, maybe group them? 
    # For now, let's keep it simple.
    
    knowledge_base["chunks"] = chunks
    
    if embedding_model:
        embeddings = embedding_model.encode(chunks)
        knowledge_base["embeddings"] = embeddings
    else:
        print("Embedding model not loaded, RAG will be disabled (or basic keyword search).")

def find_relevant_context(query, top_k=3):
    """
    Finds relevant chunks from the knowledge base using semantic search.
    """
    if not knowledge_base["embeddings"] is not None or not knowledge_base["chunks"]:
        return ""

    if embedding_model:
        query_embedding = embedding_model.encode([query])
        
        # Calculate cosine similarity
        similarities = np.dot(knowledge_base["embeddings"], query_embedding.T).flatten()
        
        # Get top k indices
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        relevant_chunks = [knowledge_base["chunks"][i] for i in top_indices]
        return "\n\n".join(relevant_chunks)
    
    return ""

def get_ai_response(user_query, context=""):
    """
    Generates a response from Groq API using the provided context.
    """
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not found."

    system_prompt = f"""
    You are a professional AI assistant for Asish Kumar Behera's portfolio website.
    Your goal is to answer questions about Asish's skills, experience, projects, and background based ONLY on the provided context.
    
    Context from Resume:
    {context}
    
    Instructions:
    1. Answer politely and professionally.
    2. Keep answers concise (under 3-4 sentences is best, unless detailed info is asked).
    3. If the answer is found in the context, provide it clearly.
    4. If the user asks something NOT related to Asish's portfolio, skills, experience, or the provided context, politely refuse.
       Refusal Example: "I’m designed to answer questions only about Asish Kumar Behera’s portfolio, skills, and experience. Please ask something related to that."
    5. Do not hallucinate information not in the context.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_query,
                }
            ],
            model="llama-3.1-8b-instant", # Using a fast model
            temperature=0.5,
            max_tokens=200,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error communicating with AI service: {str(e)}"
