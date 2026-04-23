# NoteForge AI: RAG-based Semantic PDF Search

NoteForge is an AI-powered document intelligence system built for the **Endee.io Internship Challenge**. It allows users to upload PDFs, convert them into high-dimensional vector embeddings, and perform semantic search using a Retrieval-Augmented Generation (RAG) pipeline.

## 🚀 Features
- **PDF Extraction**: Efficient text extraction using `pypdf`.
- **Semantic Chunking**: Context-aware text splitting for better retrieval.
- **Vector Embeddings**: Powered by `sentence-transformers (all-MiniLM-L6-v2)`.
- **Vector Database**: Utilizing **Endee.io** for high-performance vector storage and similarity search.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **Vector DB**: Endee.io
- **ML Models**: HuggingFace Sentence Transformers
- **Frontend**: HTML5, Tailwind CSS, JavaScript

## Project Structure

NoteForge/
│
├── backend/
│ └── main.py
│
├── frontend/
│ ├── index.html
│ ├── styles.css
│ └── script.js
│
├── screenshots/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

## 🏗️ System Design
1. **Ingestion**: PDF text is extracted and split into overlapping chunks.
2. **Embedding**: Chunks are converted into 384-dimensional vectors.
3. **Storage**: Vectors and metadata are upserted into the Endee Vector Index.
4. **Retrieval**: User queries are embedded in real-time and matched against the index using Cosine Similarity via the Endee Query API.

## ⚡ Setup
1. Clone the forked repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `ENDEE_TOKEN` to a `.env` file.
4. Run backend: `uvicorn backend.main:app --reload`