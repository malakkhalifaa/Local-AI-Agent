from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

#These framwork that makes it easy to use ollama with langchain
#Ollama should be running in the background for this to work
#This will all run locally on your machine, no data is sent to the cloud

model = OllamaLLM(model="llama3.2")

#What we want to ask the model
template="""
You are an exeprt in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""
while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break
    
    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    print(result)