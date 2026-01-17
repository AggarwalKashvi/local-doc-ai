import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

PDF_DIR = "data/pdfs"
VECTOR_DB_DIR = "data/vectordb"

def main():
    print("Loading PDFs...")
    
    documents = []
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(PDF_DIR, file)
            loader = PyPDFLoader(path)
            documents.extend(loader.load())
            print(f"Loaded {file}")

    if not documents:
        print("No PDFs found!")
        return

    print("Splitting text...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    print("Creating embeddings with nomic embed text...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    

    print("Building FAISS index...")
    db = None
    batch_size = 8
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        print(f"Embedding batch {i//batch_size + 1} / {(len(chunks) // batch_size) + 1}")
        
        if db is None:
            db = FAISS.from_documents(batch, embeddings)

        else:
            db.add_documents(batch)


    print("Saving vector database...")
    db.save_local(VECTOR_DB_DIR)

    print("Vector database created successfully!")

if __name__ == "__main__":
    main()
