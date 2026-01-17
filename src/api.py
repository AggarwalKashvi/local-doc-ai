import os
import shutil
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_DIR = "data/pdfs"
VECTOR_DB_DIR = "data/vectordb"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request Models ----------

class Question(BaseModel):
    question: str

# ---------- Load AI Components ----------

print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("Loading or creating vector database...")
if os.path.exists(VECTOR_DB_DIR) and os.listdir(VECTOR_DB_DIR):
    db = FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)
else:
    db = FAISS.from_texts([], embeddings)

print("Starting Gemma...")
llm = Ollama(model="gemma3:1b")

def get_retriever():
    return db.as_retriever(search_kwargs={"k": 4})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = PromptTemplate.from_template(
    """
    You are an assistant answering questions using only the provided context.
    If the answer is not in the context, say "I don't know."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
)

def run_chain(question: str):
    retriever = get_retriever()
    docs = retriever.get_relevant_documents(question)
    context = format_docs(docs)
    return llm.invoke(prompt.format(context=context, question=question))

# ---------- API Endpoints ----------

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    path = os.path.join(PDF_DIR, file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    loader = PyPDFLoader(path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    db.add_documents(chunks)
    db.save_local(VECTOR_DB_DIR)

    return {"status": "PDF added successfully", "chunks": len(chunks)}

@app.post("/ask")
async def ask(q: Question):
    answer = run_chain(q.question)
    return {"answer": answer}
