# Academic Paper Summarizer using RAG

## Description
This project summarizes academic research papers using
Retrieval Augmented Generation (RAG).  
Instead of summarizing blindly, the system retrieves relevant
sections from the paper and then generates an accurate summary.

## How It Works
1. Reads an academic paper (PDF)
2. Splits the document into chunks
3. Converts chunks into embeddings
4. Stores embeddings in FAISS vector database
5. Retrieves relevant sections
6. Generates a structured summary using an LLM

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py