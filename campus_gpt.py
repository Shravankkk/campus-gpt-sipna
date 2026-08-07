"""
Very simple CampusGPT RAG logic.

RAG means:
1. Read documents
2. Find useful document lines
3. Send those lines to Gemini
4. Show Gemini's answer
"""

import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_MODEL = "gemini-3.5-flash-lite"


COMMON_WORDS = {
    "what", "is", "the", "a", "an", "of", "for", "to", "in", "on",
    "and", "or", "with", "about", "tell", "me", "please", "can", "you",
    "when", "where", "how", "do", "does", "are", "any", "my", "i",
}


def load_documents(folder_path):
    """
    Read all .txt files from the documents folder.
    """
    documents = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        documents.append({
            "name": file_name,
            "text": text,
        })

    return documents


def make_chunks(documents):
    """
    Split documents into small searchable lines.
    """
    chunks = []

    for document in documents:
        lines = document["text"].splitlines()

        for line in lines:
            line = line.strip()

            if line:
                chunks.append({
                    "source": document["name"],
                    "text": line,
                })

    return chunks


def clean_text(text):
    """
    Convert text to lowercase and remove simple punctuation.
    """
    text = text.lower()

    for symbol in ".,?!:;()[]":
        text = text.replace(symbol, " ")

    return text


def search_documents(question, chunks, limit=3):
    """
    Find the best matching document lines for a question.
    """
    cleaned_question = clean_text(question)
    words = cleaned_question.split()

    keywords = []

    for word in words:
        if word not in COMMON_WORDS:
            keywords.append(word)

    results = []

    for chunk in chunks:
        cleaned_chunk = clean_text(chunk["text"])
        score = 0

        for keyword in keywords:
            if keyword in cleaned_chunk:
                score = score + 1

        if score > 0:
            results.append({
                "source": chunk["source"],
                "text": chunk["text"],
                "score": score,
            })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]


def answer_question(question, chunks):
    """
    Find useful chunks and ask Gemini to answer using only those chunks.
    """
    results = search_documents(question, chunks)

    if not results:
        return {
            "answer": "Sorry, I could not find this information in the college documents.",
            "sources": [],
        }

    answer = ask_gemini(question, results)

    return {
        "answer": answer,
        "sources": results,
    }


def ask_gemini(question, results):
    """
    Send the question and retrieved document lines to Gemini.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    context = ""

    for result in results:
        context = context + result["source"] + ": " + result["text"] + "\n"

    prompt = f"""You are CampusGPT, a helpful assistant for college students. Answer the question using only the context below.
Context:
{context}

Question:
{question}

Answer:
"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        return response.text
    except Exception as error:
        return "Gemini error: " + str(error)
