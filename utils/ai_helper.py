"""Gemini API helpers: summary, Q&A, key points and quiz generation."""
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_CHARS = 600_000  # safety limit on document size sent to the model

SYSTEM_PROMPT = (
    "You are DocuMind, an AI assistant that works strictly with the document "
    "provided by the user. Base every answer on the document content. If the "
    "answer is not in the document, say so clearly instead of guessing."
)


def get_api_key() -> str | None:
    """Look for the key in environment/.env, then Streamlit secrets."""
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


def _generate(prompt: str, api_key: str, temperature: float = 0.3) -> str:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )
    return (response.text or "").strip() or "The model returned an empty response."


def _doc_block(text: str) -> str:
    return f"<document>\n{text[:MAX_CHARS]}\n</document>"


def summarize(text: str, api_key: str, detailed: bool = False) -> str:
    style = (
        "a detailed, well-structured summary with headings and bullet points "
        "covering all major sections"
        if detailed
        else "a short summary of at most 150 words"
    )
    prompt = f"{_doc_block(text)}\n\nWrite {style} of the document above."
    return _generate(prompt, api_key)


def answer_question(text: str, question: str, history: list[dict], api_key: str) -> str:
    convo = "\n".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in history[-6:]
    )
    prompt = (
        f"{_doc_block(text)}\n\n"
        f"Previous conversation:\n{convo or '(none)'}\n\n"
        f"User question: {question}\n\n"
        "Answer clearly using only the document. Mention page numbers when helpful."
    )
    return _generate(prompt, api_key)


def key_points(text: str, api_key: str, count: int = 10) -> str:
    prompt = (
        f"{_doc_block(text)}\n\n"
        f"Extract the {count} most important points and key concepts from the "
        "document. Return a numbered list; give each item a bold title followed "
        "by a one-sentence explanation."
    )
    return _generate(prompt, api_key)


def generate_quiz(text: str, api_key: str, count: int = 5) -> str:
    prompt = (
        f"{_doc_block(text)}\n\n"
        f"Create {count} multiple-choice questions based on the document. "
        "Format each as:\n\n"
        "**Q1. question text**\n"
        "- A) option\n- B) option\n- C) option\n- D) option\n\n"
        "After all questions, add a section titled '## Answer Key' with the "
        "correct option and a one-line explanation for each question."
    )
    return _generate(prompt, api_key, temperature=0.6)
