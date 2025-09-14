# 📊 RAG Financials Q&A

This project is a **Retrieval-Augmented Generation (RAG) system** that lets you ask financial questions (revenues, margins, R&D, etc.) about Microsoft, Google, and NVIDIA using their **10-K HTML filings**.

It uses:
- **BeautifulSoup** → to extract text from HTML filings  
- **Chunking** → to split documents into smaller pieces  
- **FAISS** → to store and search embeddings  
- **OpenAI / Cohere embeddings** → with automatic fallback  
- **Query decomposition agent** → breaks down complex questions into smaller sub-queries


## ✨ Features
- Ask **financial questions** across Microsoft, Google, and NVIDIA’s 10-K filings.  
- Uses **query decomposition + metric normalization** to break down complex queries.  
- Supports **semantic search with FAISS** and **OpenAI/Cohere embeddings (with fallback)**.  
- Returns **structured answers with excerpts** for transparency.  


---

## Setup

1. Clone the repository:
```bash
git clone git@github.com:cgmonali/RAG-financial-Q-A.git
cd RAG-financial-Q-A
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Add filings into files/

5. Create a `.env` file in the root:
```bash
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key
```

7. Run the project
```bash
python3 main.py
```

