# 🚀 Enterprise Multi-Source RAG Knowledge Assistant (Phase 1)

A Retrieval-Augmented Generation (RAG) application that allows users to query PDF documents using natural language. The system retrieves relevant document chunks using semantic search and generates accurate answers using Google's Gemini API.

---

## 📌 Project Overview

This project is the first phase of an Enterprise Knowledge Base Assistant.

The application:

- Loads PDF documents
- Splits documents into semantic chunks
- Converts chunks into embeddings
- Stores embeddings in a FAISS vector database
- Retrieves the most relevant chunks for a query
- Uses Gemini 2.5 Flash to generate grounded answers
- Provides source citations for transparency

---

## 🏗️ Architecture

```text
PDF Document
      │
      ▼
PDF Loader
      │
      ▼
Document Chunking
      │
      ▼
BGE Embeddings
      │
      ▼
FAISS Vector Store
      │
      ▼
Retriever
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
Answer + Citations
```

---

## ✨ Features

### ✅ PDF Ingestion

Upload and process PDF documents.

### ✅ Intelligent Chunking

Documents are split into manageable chunks using RecursiveCharacterTextSplitter.

### ✅ Semantic Search

Uses vector similarity search instead of keyword matching.

### ✅ Local Embeddings

Generates embeddings using:

```text
BAAI/bge-small-en-v1.5
```

### ✅ FAISS Vector Database

Stores document embeddings for efficient retrieval.

### ✅ Gemini Integration

Uses Gemini 2.5 Flash to generate context-aware answers.

### ✅ Source Citations

Displays document pages used to generate answers.

---

## 🛠️ Tech Stack

| Component       | Technology                 |
| --------------- | -------------------------- |
| Language        | Python                     |
| LLM             | Gemini 2.5 Flash           |
| Embeddings      | BAAI/bge-small-en-v1.5     |
| Vector Database | FAISS                      |
| Framework       | LangChain                  |
| PDF Processing  | PyPDF                      |
| Environment     | Python Virtual Environment |

---

## 📂 Project Structure

```text
enterprise-rag/
│
├── data/
│   └── sample.pdf
│
├── src/
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── gemini_client.py
│
├── .env
│
├── main.py
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd enterprise-rag
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Gemini API Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Get your API key from Google AI Studio.

---

## ▶️ Running the Project

```bash
python main.py
```

Example:

```text
Ask a question:
What are the company's revenue figures?
```

Output:

```text
Answer:
The company reported revenue growth of ...

Sources:
Page 5
Page 8
Page 10
```

---

## 🔍 How Retrieval Works

### Step 1: PDF Loading

The PDF is converted into LangChain Documents.

### Step 2: Chunking

Documents are split into chunks using:

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

### Step 3: Embeddings

Each chunk is converted into a vector representation using:

```text
BAAI/bge-small-en-v1.5
```

### Step 4: Vector Storage

Embeddings are stored in a FAISS index.

### Step 5: Retrieval

For every user query:

```text
User Question
      ↓
Embedding
      ↓
Similarity Search
      ↓
Top-K Relevant Chunks
```

### Step 6: Gemini Generation

Retrieved chunks are provided as context to Gemini, which generates the final answer.

---

## 📊 Current Limitations

- Supports PDF documents only
- Single-user environment
- No Streamlit UI yet
- No chat history
- No re-ranking
- No multi-source ingestion

---

## 🚧 Upcoming Features (Phase 2)

- Website ingestion
- CSV ingestion
- Streamlit chat interface
- Persistent vector database
- Multi-document support
- Chat history
- Metadata management

---

## 📈 Future Enhancements

- Sentence Window Retrieval
- Hybrid Search
- Re-ranking using BGE Reranker
- Graph RAG
- AWS Deployment
- Enterprise Authentication
- Knowledge Base Management Dashboard

---

## 🎯 Learning Outcomes

Through this project, I gained hands-on experience with:

- Retrieval-Augmented Generation (RAG)
- Embedding Models
- Vector Databases
- Semantic Search
- LangChain
- FAISS
- Gemini API Integration
- Prompt Engineering
- LLM Application Development

---

## 👨‍💻 Author

Akshay

Mathematics & Computing Student

Building AI, ML, and Data-Driven Applications.
