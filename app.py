"""
CampusGPT Sipna - beginner version.

Run this app with:
    streamlit run app.py
"""

import os

import streamlit as st

from campus_gpt import answer_question, load_documents, make_chunks


DOCUMENTS_FOLDER = os.path.join(os.path.dirname(__file__), "documents")


st.set_page_config(
    page_title="CampusGPT Sipna",
    layout="centered",
)


@st.cache_data
def get_chunks():
    """
    Load college documents once and reuse them.
    """
    documents = load_documents(DOCUMENTS_FOLDER)
    chunks = make_chunks(documents)
    return documents, chunks


documents, chunks = get_chunks()


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.title("CampusGPT Sipna")
st.write("Ask simple questions about the college documents.")


with st.sidebar:
    st.header("Documents")

    for document in documents:
        st.write("- " + document["name"])

    st.divider()
    st.header("Gemini")

    api_key = st.text_input("Gemini API key", type="password")

    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.success("API key added for this session.")
    elif os.getenv("GEMINI_API_KEY"):
        st.success("API key loaded from environment.")
    else:
        st.warning("Add a Gemini API key to get AI answers.")

    st.divider()

    if st.button("Clear chat"):
        st.session_state.chat_history = []
        st.rerun()


sample_questions = [
    "What departments are available at Sipna?",
    "Tell me about Sipna library facilities",
    "What placement training is available?",
]

st.subheader("Try a question")

columns = st.columns(3)

for index, question in enumerate(sample_questions):
    if columns[index].button(question):
        result = answer_question(question, chunks)
        st.session_state.chat_history.append({
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
        })
        st.rerun()


for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

        if chat["sources"]:
            with st.expander("Sources"):
                for source in chat["sources"]:
                    st.write(source["source"] + ": " + source["text"])


user_question = st.chat_input("Ask CampusGPT...")

if user_question:
    result = answer_question(user_question, chunks)

    st.session_state.chat_history.append({
        "question": user_question,
        "answer": result["answer"],
        "sources": result["sources"],
    })

    st.rerun()
