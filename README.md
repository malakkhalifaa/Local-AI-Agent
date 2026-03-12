# Local AI Agent: Restaurant Q&A

> Ask questions about a pizza restaurant in plain English—answers from your own review data using a local vector DB (Chroma) and LLM (Ollama). No cloud APIs.

---

## Intro

This project is a **fully local** question-answering app for a pizza restaurant. You run it on your machine, point it at a CSV of reviews, and then ask questions in plain English (e.g. *"How are the vegan options?"*). The app uses a vector database (Chroma) to find the most relevant reviews and a local LLM (Ollama) to turn them into clear, review-based answers—no cloud APIs or API keys required. Everything runs on your computer.

Below you’ll find what it does, how it works, how to set it up, and how to run it.

![Screenshot: Q&A in action — asking about vegan options](https://github.com/user-attachments/assets/56ee28a6-a38c-4339-b77e-2a9d2bcba898)

---

## What It Does (Functionality)

When you run the app, you see:

```
Ask your question (q to quit): How are the vegan options?
```

The app then:

1. **Searches** the stored reviews for ones that best match your question (semantic search).
2. **Sends** those reviews and your question to a local LLM (e.g. Llama 3.2 via Ollama).
3. **Prints** an answer that summarizes and compares what the reviews say.

**Example (from your screenshot):**  
For *"How are the vegan options?"* the answer might say the vegan options are a *"mixed bag"*: one review (e.g. 2 stars) might complain about tasteless vegan cheese and coconut flavor, while another (5 stars) might praise the cashew cheese and fresh seasonal toppings. It can also mention things like an *"Experimental"* menu that may include vegan options. So you get a balanced, review-based summary instead of a single opinion.

You can keep asking more questions; type **`q`** to quit.

---

## How It Works

| Step | Where | What happens |
|------|--------|----------------|
| 1. Load data | `vector.py` | Reads `realistic_restaurant_reviews.csv` and embeds each review with **Ollama** (e.g. `mxbai-embed-large`). |
| 2. Vector DB | `vector.py` | Stores embeddings in **Chroma** under `./chrome_langchain_db`. On later runs, it reuses this DB instead of re-indexing. |
| 3. Retriever | `vector.py` | Exposes a **retriever** that, for any question, returns the **top 5** most relevant reviews (by semantic similarity). |
| 4. Q&A loop | `main.py` | Asks for a question, calls the retriever, then sends *question + retrieved reviews* to **Ollama** (e.g. Llama 3.2). The model is prompted to answer only from those reviews. |
| 5. Answer | `main.py` | Prints the model’s answer and loops back to the next question. |

So: **CSV → embeddings → Chroma → retriever → LLM → answer**. All of this runs on your machine.

### Chroma LangChain DB creation (and all that)

The **Chroma LangChain DB** is the persistent vector database that holds your reviews:

- **Where:** `./chrome_langchain_db` (folder created on first run).
- **When it’s created:** On first run, `vector.py` reads the CSV, turns each review into a document, embeds it with Ollama, and adds it to Chroma. The DB is saved to disk.
- **Later runs:** If `chrome_langchain_db` already exists, the script skips re-adding documents and just connects to the existing DB. No re-indexing.
- **What it stores:** A collection named `"restaurant_reviews"` with embedded text (title + review) and metadata (rating, date). The retriever uses this to find the top 5 reviews that best match each question.

So the Chroma LangChain DB is created once from your CSV, then reused for every question.

---

## Setup

1. **Python 3.x** and a virtual environment (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ollama** installed and running, with at least:
   - An embedding model, e.g. `mxbai-embed-large`
   - A chat model, e.g. `llama3.2`

   ```bash
   ollama pull mxbai-embed-large
   ollama pull llama3.2
   ```

4. **Data:** Put your restaurant reviews CSV in the project root as `realistic_restaurant_reviews.csv`, with columns such as **Title**, **Review**, **Rating**, and **Date**.

---

## Run

```bash
python main.py
```

Then type your questions at the prompt; type **`q`** to exit.

---

## Project layout

- **`main.py`** — Interactive loop: input question → retriever → LLM → print answer.
- **`vector.py`** — Loads CSV, builds/loads Chroma index, exposes the retriever.
- **`realistic_restaurant_reviews.csv`** — Source reviews (you add this).
- **`./chrome_langchain_db/`** — Chroma’s persistent vector store (created automatically).

---

## Summary

You get a **local** restaurant Q&A: ask things like *"How are the vegan options?"* and receive answers that combine and compare real reviews, with embeddings and the language model both running on your machine.

---

**GitHub repo description (short):**  
`Local Q&A over restaurant reviews using Chroma + Ollama. No cloud APIs.`
