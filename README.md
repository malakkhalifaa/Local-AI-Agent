# Local AI Agent: Restaurant Q&A

> Ask questions about a pizza restaurant in plain English—answers from your own review data using a **local** vector DB (Chroma) and LLM (Ollama). **No cloud APIs.**!!!!!!!!!!

---

## Intro

This project is a **fully local** question-answering app for a pizza restaurant. You run it on your machine, point it at a CSV of reviews, and ask questions in plain English—*"How are the vegan options?"*, *"Is the crust good?"*, etc. The app uses **Chroma** to find the most relevant reviews and **Ollama** to turn them into clear, review-based answers. No API keys, no cloud—everything runs on your computer.

**In this README:** what it does, how it works, setup, and how to run it.

---

### Screenshot

![Q&A in action — asking about vegan options](https://github.com/user-attachments/assets/56ee28a6-a38c-4339-b77e-2a9d2bcba898)

---

## What It Does

When you run the app you see:

```
Ask your question (q to quit): How are the vegan options?
```

The app then:

1. **Searches** the vector DB for reviews that best match your question (semantic search).
2. **Sends** those reviews + your question to the local LLM (e.g. Llama 3.2).
3. **Prints** an answer that summarizes and compares what the reviews say.

**Example:** For *"How are the vegan options?"* you might get a *"mixed bag"* summary—e.g. one review (2 stars) complaining about tasteless vegan cheese and coconut flavor, another (5 stars) praising the cashew cheese and fresh seasonal toppings, plus a note about an *"Experimental"* menu that may include vegan options. You get a balanced, review-based answer, not a single opinion.

Keep asking questions; type **`q`** to quit.

---

## How It Works

| Step | Where | What happens |
|------|--------|----------------|
| 1 | `vector.py` | Load CSV, embed each review with Ollama (`mxbai-embed-large`). |
| 2 | `vector.py` | Store embeddings in **Chroma** under `./chrome_langchain_db` (reused on later runs). |
| 3 | `vector.py` | Expose a **retriever** that returns the **top 5** most relevant reviews per question. |
| 4 | `main.py` | Prompt: ask a question → retriever fetches reviews → LLM answers from those reviews only. |

**Flow:** `CSV → embeddings → Chroma → retriever → LLM → answer` — all on your machine.

### Chroma LangChain DB (the details)

- **Where:** `./chrome_langchain_db` (created on first run).
- **When:** First run: CSV → documents → embed → add to Chroma → save to disk. Later runs: connect to existing DB, no re-indexing.
- **What’s stored:** Collection `"restaurant_reviews"` with embedded text (title + review) and metadata (rating, date). The retriever uses this to find the top 5 matches for each question.

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

3. **Ollama** installed and running. Pull the models:

   ```bash
   ollama pull mxbai-embed-large
   ollama pull llama3.2
   ```

4. **Data:** Place your restaurant reviews CSV in the project root as `realistic_restaurant_reviews.csv`, with columns **Title**, **Review**, **Rating**, and **Date**.

---

## Run

```bash
python main.py
```

Type your questions at the prompt; type **`q`** to exit.

---

## Project Layout

| File / folder | Purpose |
|---------------|---------|
| `main.py` | Interactive loop: question → retriever → LLM → answer |
| `vector.py` | Load CSV, build/load Chroma index, expose retriever |
| `realistic_restaurant_reviews.csv` | Source reviews (you provide) |
| `./chrome_langchain_db/` | Chroma’s persistent vector store (auto-created) |

---

## Summary

**Local** restaurant Q&A: ask things like *"How are the vegan options?"* and get answers that combine and compare real reviews—embeddings and LLM both run on your machine.

---

<sub>**GitHub repo description:** `Local Q&A over restaurant reviews using Chroma + Ollama. No cloud APIs.`</sub>
