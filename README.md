
- FAISS is used for fast similarity search over document embeddings  
- A local LLM generates responses using retrieved context only  
- FastAPI serves as the backend API  
- Tauri provides a lightweight desktop interface  

---

## Technology Stack

- Python  
- FastAPI  
- FAISS  
- Ollama  
- Gemma (local LLM)  
- Sentence-transformer embeddings  
- TypeScript  
- Tauri  

---

## How It Works

1. PDF documents are uploaded through the desktop interface  
2. Documents are split into chunks and converted into embeddings  
3. Embeddings are stored in a FAISS vector database  
4. User queries are embedded and matched semantically against stored vectors  
5. Relevant document context is retrieved  
6. The local LLM generates a response based only on retrieved content  

If relevant information is not found, the system explicitly responds that the answer is unknown.

---

## Privacy and Security

- No internet connectivity required  
- No external APIs or cloud services  
- All data remains on the local machine  
- Suitable for offline and privacy-sensitive environments  

---

## Use Cases

- Personal knowledge bases  
- Academic and research documents  
- Technical standards and policies  
- Secure or air-gapped systems  
- Offline document analysis  

---

## Status

This project is under active development and focuses on improving usability, document management, and interface polish.

## Interface

<img width="1030" height="747" alt="image" src="https://github.com/user-attachments/assets/7f0385c6-339c-4fa6-978f-3d6987cf0613" />
