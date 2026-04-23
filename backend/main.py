import os
import uuid
import requests
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Config from Endee Documentation
ENDEE_TOKEN = os.getenv("ENDEE_TOKEN")
INDEX_NAME = "noteforge_index"
ENDEE_BASE_URL = "https://api.endee.io/api/v1"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=400, overlap=40):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # 1. Extract Text
        reader = PdfReader(file.file)
        text = "".join([page.extract_text() or "" for page in reader.pages])
        
        # 2. Chunk and Embed
        chunks = chunk_text(text)
        embeddings = model.encode(chunks).tolist()
        
        # 3. Prepare Vectors for Endee
        vectors = []
        for chunk, emb in zip(chunks, embeddings):
            vectors.append({
                "id": str(uuid.uuid4()),
                "vector": emb,
                "meta": {"text": chunk}
            })
        
        # 4. Upsert to Endee Vector DB
        upsert_url = f"{ENDEE_BASE_URL}/indexes/{INDEX_NAME}/upsert"
        requests.post(
            upsert_url, 
            headers={"Authorization": f"Bearer {ENDEE_TOKEN}"}, 
            json={"vectors": vectors}
        )

        return {"status": "success", "chunks_uploaded": len(vectors)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/search")
async def search_notes(query: str = Query(...)):
    # 1. Embed the search query
    query_embedding = model.encode([query]).tolist()[0]
    
    # 2. Query Endee Vector DB
    url = f"{ENDEE_BASE_URL}/indexes/{INDEX_NAME}/query"
    payload = {"vector": query_embedding, "topK": 3, "includeVectors": False}
    
    response = requests.post(
        url, 
        headers={"Authorization": f"Bearer {ENDEE_TOKEN}"}, 
        json=payload
    )
    return response.json()