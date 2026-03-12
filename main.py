# --- Imports: local LLM (Ollama), prompt builder, and the vector retriever from vector.py ---
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

# Use Llama 3.2 via Ollama for generating answers (runs fully on your machine)
model = OllamaLLM(model="llama3.2")

# Prompt tells the model to act as a restaurant expert and use only the provided reviews to answer
template = """
You are an expert in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
# Chain: prompt -> model (user question + retrieved reviews go in, answer comes out)
chain = prompt | model

# Interactive loop: ask a question, get an answer, repeat until user types "q"
while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    # Fetch the 5 most relevant reviews for this question from the vector database
    reviews = retriever.invoke(question)
    # Send those reviews + the question to the LLM and print the answer
    result = chain.invoke({"reviews": reviews, "question": question})
    print(result)