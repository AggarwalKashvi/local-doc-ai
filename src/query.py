from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

VECTOR_DB_DIR = "vectordb"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def main():
    print("Loading vector database...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)

    retriever = db.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke("test")
    print("\nDEBUG: Retrieved documents:")
    for d in docs:
        print(d.page_content[:200], "\n---\n")

    print("Starting Gemma...")
    llm = Ollama(model="gemma3:1b")

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

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    print("Ask questions about your PDFs (type 'exit' to quit)\n")

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        answer = chain.invoke(query)
        print("\nGemma:", answer)
        print("\n" + "-" * 50)

if __name__ == "__main__":
    main()
