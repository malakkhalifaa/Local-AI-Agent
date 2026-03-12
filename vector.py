# Vector DB logic: load CSV reviews -> create Chroma LangChain DB (embeddings + persistent store)
# -> expose a retriever so main.py can fetch relevant reviews for each question. All local (Ollama + Chroma).
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

# Chroma LangChain DB: path where the vector database is stored on disk (created on first run)
# If this folder exists, we assume the DB is already built and skip re-adding all documents
db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

# Only build the document list and IDs when the Chroma LangChain DB doesn't exist yet
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

# Create or connect to the Chroma LangChain DB (vector store):
# - collection_name: logical name for this set of vectors (e.g. "restaurant_reviews")
# - persist_directory: where Chroma saves the DB so it survives restarts (chrome_langchain_db folder)
# - embedding_function: Ollama model used to turn text into vectors for similarity search
# First run: folder is created and we add documents below. Later runs: we just connect and reuse.
vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

# Only on first run: add all CSV reviews into the Chroma LangChain DB (embedding + storing each one)
# After this, the DB is ready; next runs will skip this and use the existing DB
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# Retriever: given a question, fetches the top 5 most relevant reviews from the Chroma DB by semantic similarity
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)