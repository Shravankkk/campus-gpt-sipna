# CampusGPT Sipna

This is a super basic RAG-style CampusGPT project for students.

It uses:

- Streamlit for the app
- Simple keyword search for retrieval
- Gemini for generating the final answer

It does not use embeddings or vector databases.

## What Students Learn

- How to read college documents from a folder
- How to split text into small chunks
- How to retrieve useful chunks using keywords
- How to send retrieved context to Gemini
- How to show answers in a Streamlit chat app

## Folder Structure

```text
campus-gpt-sipna/
├── app.py
├── campus_gpt.py
├── documents/
│   ├── attendance_rules.txt
│   ├── departments.txt
│   ├── events.txt
│   ├── facilities.txt
│   ├── library_info.txt
│   └── placements.txt
├── .devcontainer/
│   └── devcontainer.json
├── .env
├── requirements.txt
├── setup.sh
└── run.sh
```

## Setup With GitHub Codespaces

Open this project in GitHub Codespaces. Dependencies are installed automatically.

After Codespaces opens, run:

```bash
./run.sh
```

## Gemini API Key

Option 1: Paste your Gemini API key in the app sidebar.

Option 2: Open `.env` and add your key:

```text
GEMINI_API_KEY=your_real_key_here
```

## Run

In Codespaces:

```bash
./run.sh
```

On your own laptop, first run local setup:

```bash
chmod +x setup.sh run.sh
./setup.sh
```

Then run:

```bash
source .venv/bin/activate
./run.sh
```

## Main Files

- `app.py` has the Streamlit user interface.
- `campus_gpt.py` has the RAG logic.
- `documents/` has the college information.

## How The RAG Flow Works

1. `load_documents()` reads text files.
2. `make_chunks()` splits documents into small lines.
3. `search_documents()` finds useful lines for the question.
4. `ask_gemini()` sends the question and useful lines to Gemini.
5. Gemini writes the final answer.

## Easy Student Tasks

Students can try these changes:

1. Add more lines inside the files in `documents/`.
2. Add one new text file in `documents/`.
3. Change the sample questions in `app.py`.
4. Improve the `COMMON_WORDS` list in `campus_gpt.py`.
5. Change how many results are returned in `search_documents()`.
