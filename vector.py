# --- Imports: embeddings (Ollama), vector store (Chroma), document type, and utilities ---
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load the restaurant reviews CSV so we can turn each row into a searchable document
df = pd.read_csv("realistic_restaurant_reviews.csv")

# Create the embedding model: converts text into vectors so we can do semantic search (Ollama runs locally)
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Path where Chroma will save the vector DB; skip re-indexing if this folder already exists
db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

# Only build the document list and IDs when the database doesn't exist yet
if add_documents:
    documents = []
    ids = []

    # Turn each review row into a LangChain Document (text + metadata) for the vector store
    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={"rating": row["Rating"], "date": row["Date"]},
        )
        ids.append(str(i))  # Chroma needs string IDs for each document
        documents.append(document)

# Create or connect to the Chroma vector store: persistent on disk, uses our embedding model
vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

# If we just built the document list, add all documents to the store (only once, then reuse)
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# Retriever: given a question, fetches the top 5 most relevant reviews by semantic similarity
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)