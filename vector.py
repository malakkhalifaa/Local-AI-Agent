#logic for vector database, uses chromadb, which is a local vector database
#that can be used to store and retrieve vectors
#take entire csv file and convert it to a vector database, 
# then use that vector database to answer questions
from langchain_ollM import OllamaLLM
from langchain_chromadb import ChromaDB
from langchain_core.documents import Document
import os
import pandas as pd

#load csv file
df=pd.read_csv("realife_reviews.csv")
#bring embeddings for each review
embeddings=OllamaEmbeddings(model="mxbai-embeddings-large")
#store our vectors in chromadb


db_location="./chrome_landchain_db"
add_documents=not os.path.exists(db_location) #check if the database already exists, if it does we don't need to add documents again
#if exists means vectors are already stored, if not we need to add them


if add_documents:
    documents=[]
    ids=[]

    #iterate through each review and create a document for it
    for i, row in df.iterrows():
        document=Document(page_content=row["Title"]+ " " + row["Review"] #page content is what we re vectorizing, we can use the title and review text for this
        metadata={"rating": row["Rating"], "date": row["Date"]} 
        #metadata is additional information we want to store about the document, we can use the rating and date for this but wont be used for retrieval in this example
       id=str(i) #id is a unique identifier for the document, we can just use the index of the review in the dataframe for this
        )
        ids.append(str(i)) #need to convert to string because chromadb expects string ids
        documents.append(document) #add the document to our list of documents
        
vector_store = Chroma(collection_name="restaurant_reviews", 
                      persist_directory=db_location, 
                      embedding_function=embeddings
                      ) #store persistently in the specified directory, rather than in memory

if add_documents