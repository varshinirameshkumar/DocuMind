"""DocuMind - AI-Powered PDF Assistant (Streamlit + Google Gemini)."""
import streamlit as st

from utils import ai_helper
from utils.pdf_reader import extract_text_from_pdf

st.set_page_config(page_title="DocuMind", page_icon="📄", layout="wide")

# ---------- Session state ----------
defaults = {
    "doc_text": "",
    "doc_name": "",
    "page_count": 0,
    "chat": [],
    "cache": {},
    "uploader_key": 0,
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)


def clear_document():
    for k, v in defaults.items():
        if k != "uploader_key":
            st.session_state[k] = v if not isinstance(v, (list, dict)) else type(v)()
    st.session_state.uploader_key += 1


def run_ai(fn, *args, **kwargs):
    """Call an AI helper with friendly error handling."""
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        st.error(f"AI request failed: {e}")
        return None


# ---------- Sidebar ----------
with st.sidebar:
    st.title("📄 DocuMind")

    api_key = ai_helper.get_api_key()
    if not api_key:
        api_key = st.text_input(
            "Gemini API key", type="password",
            help="Get a free key at https://aistudio.google.com/apikey",
        )

    uploaded = st.file_uploader(
        "Upload PDF", type="pdf", key=f"uploader_{st.session_state.uploader_key}"
    )

    if uploaded and uploaded.name != st.session_state.doc_name:
        with st.spinner("Reading PDF..."):
            try:
                text, pages = extract_text_from_pdf(uploaded.getvalue())
            except Exception as e:
                st.error(f"Could not read this PDF: {e}")
                text, pages = "", 0
        if text:
            st.session_state.update(
                doc_text=text, doc_name=uploaded.name, page_count=pages,
                chat=[], cache={},
            )
        elif pages:
            st.warning("No text found. This may be a scanned (image-only) PDF.")

    if st.session_state.doc_name:
        st.success(f"**{st.session_state.doc_name}**")
        st.caption(
            f"{st.session_state.page_count} pages · "
            f"{len(st.session_state.doc_text):,} characters"
        )
        st.button("🗑️ Clear document", on_click=clear_document, use_container_width=True)

# ---------- Main screen ----------
st.title("Your Documents, Smarter with AI.")

if not st.session_state.doc_text:
    st.info("👈 Upload a PDF from the sidebar to get started.")
    st.stop()

if not api_key:
    st.warning("Enter your Gemini API key in the sidebar (or set it in a `.env` file).")
    st.stop()

text = st.session_state.doc_text
tab_sum, tab_chat, tab_keys, tab_quiz = st.tabs(
    ["📝 Summary", "💬 Chat with PDF", "🔑 Key Points", "❓ Generate Quiz"]
)

# Summary
with tab_sum:
    detailed = st.radio("Summary length", ["Short", "Detailed"], horizontal=True) == "Detailed"
    cache_key = f"summary_{detailed}"
    if st.button("Generate summary", type="primary"):
        with st.spinner("Summarizing..."):
            result = run_ai(ai_helper.summarize, text, api_key, detailed)
        if result:
            st.session_state.cache[cache_key] = result
    if cache_key in st.session_state.cache:
        st.markdown(st.session_state.cache[cache_key])

# Chat
with tab_chat:
    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    question = st.chat_input("Ask a question about your document...")
    if question:
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = run_ai(
                    ai_helper.answer_question, text, question,
                    st.session_state.chat, api_key,
                )
            if reply:
                st.markdown(reply)
        if reply:
            st.session_state.chat += [
                {"role": "user", "content": question},
                {"role": "assistant", "content": reply},
            ]

# Key points
with tab_keys:
    n = st.slider("Number of key points", 5, 20, 10)
    if st.button("Extract key points", type="primary"):
        with st.spinner("Extracting..."):
            result = run_ai(ai_helper.key_points, text, api_key, n)
        if result:
            st.session_state.cache["keys"] = result
    if "keys" in st.session_state.cache:
        st.markdown(st.session_state.cache["keys"])

# Quiz
with tab_quiz:
    q = st.slider("Number of questions", 3, 15, 5)
    if st.button("Generate quiz", type="primary"):
        with st.spinner("Writing questions..."):
            result = run_ai(ai_helper.generate_quiz, text, api_key, q)
        if result:
            st.session_state.cache["quiz"] = result
    if "quiz" in st.session_state.cache:
        st.markdown(st.session_state.cache["quiz"])
        st.download_button(
            "Download quiz (.md)", st.session_state.cache["quiz"],
            file_name="quiz.md", mime="text/markdown",
        )
