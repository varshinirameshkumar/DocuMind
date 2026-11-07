# 📄 DocuMind – AI-Powered PDF Assistant

**Your Documents, Smarter with AI.**

DocuMind lets you upload a PDF and then summarize it, chat with it, pull out its key points and generate a practice quiz, all powered by Google's Gemini API. It is built entirely in Python with Streamlit.

🔗 **Live demo:** https://documind-jr6na2hrjjcvalkyb4cdzc.streamlit.app
💻 **Source code:** https://github.com/varshinirameshkumar/DocuMind

> Free-tier hosting: the demo may take a minute to wake up if nobody has used it recently. Please use public or sample PDFs only, because document text is sent to Google's Gemini API.

---

## ✨ Features

| Feature | What it does |
|---|---|
| 📄 **PDF upload** | Upload any text-based PDF and see its page and character count |
| 📝 **Summary** | A short (about 150 words) or detailed, structured summary |
| 💬 **Chat with PDF** | Ask questions in plain English; follow-up questions work because recent messages are remembered. Answers come only from the document |
| 🔑 **Key points** | Extract the 5 to 20 most important points and concepts |
| ❓ **Generate quiz** | 3 to 15 multiple-choice questions with an answer key, downloadable as Markdown |
| 🗑️ **Clear document** | Reset everything and start with a new file |

---

## 🧰 Tech stack

| Component | Technology | Why |
|---|---|---|
| Language | Python 3.10+ | Standard for AI work, rich libraries |
| Interface | [Streamlit](https://streamlit.io) | Full web UI in pure Python, free hosting |
| LLM | [Google Gemini API](https://ai.google.dev) (`google-genai` SDK) | Free tier, large context window, simple API |
| PDF reading | [PyMuPDF](https://pymupdf.readthedocs.io) | Fast, reads PDFs straight from memory |
| Configuration | python-dotenv | Keeps the API key out of the code |
| Deployment | Streamlit Community Cloud | Free, deploys directly from GitHub |

No database, vector store or model training is needed: the whole document fits in the model's context window, so each request simply sends the document text together with a task-specific prompt.

---

## 🔄 How it works

```text
Upload PDF → PyMuPDF extracts text → text kept in session state
          → button click / question → prompt = <document> + task
          → Gemini API → response shown (and cached)
```

1. The PDF is read from memory and converted to text, with `[Page N]` markers so answers can mention pages.
2. The text is stored in Streamlit's `session_state`, so it survives reruns.
3. Each feature has its own prompt in `utils/ai_helper.py`. A system instruction tells the model to use only the document and to say so when the answer is not there.
4. The Gemini response is rendered as Markdown. Summaries, key points and quizzes are cached so they stay on screen.

---

## 📁 Project structure

```text
DocuMind/
├── app.py               # Streamlit interface and app logic
├── requirements.txt     # Python dependencies
├── .env.example         # Template for your local settings
├── .gitignore           # Keeps .env and venv out of Git
├── README.md            # This file
└── utils/
    ├── __init__.py
    ├── pdf_reader.py    # PDF text extraction (PyMuPDF)
    └── ai_helper.py     # Prompts and Gemini API calls
```

---

## 🚀 Getting started

### Prerequisites

- Python 3.10 or newer
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/varshinirameshkumar/DocuMind.git
cd DocuMind
```

### 2. Create and activate a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Copy the template and edit it:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and set your values (no quotes, no spaces around `=`):

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

If you skip this step, the app will ask for the key in the sidebar instead.

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at http://localhost:8501.

---

## ⚙️ Configuration

| Setting | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Your Gemini API key (`GOOGLE_API_KEY` also works) |
| `GEMINI_MODEL` | No | Model name. Defaults to `gemini-3.5-flash-lite` |

**About model names:** providers retire old models over time. If you see a `404 NOT_FOUND` error mentioning the model, list the models your key can use and set one in `GEMINI_MODEL`:

```bash
python -c "import os; from dotenv import load_dotenv; from google import genai; load_dotenv(); c=genai.Client(api_key=os.getenv('GEMINI_API_KEY')); [print(m.name) for m in c.models.list() if 'generateContent' in (m.supported_actions or [])]"
```

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this project to your own GitHub repository (`.env` is git-ignored, so your key is never uploaded).
2. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub and click **Create app**.
3. Choose your repository, the `main` branch and `app.py` as the main file.
4. Under **Advanced settings → Secrets**, add:

   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   GEMINI_MODEL = "gemini-3.5-flash-lite"
   ```

5. Click **Deploy**. Every `git push` afterwards updates the live app automatically.

---

## 🔒 Security and privacy

- Never commit your API key. Keep it in `.env` locally and in Streamlit Secrets in the cloud.
- Run `git status` before each push and make sure `.env` is not listed.
- If a key is ever exposed, delete it in Google AI Studio and create a new one.
- Uploaded text is sent to the Gemini API. Check Google's current data terms and avoid confidential documents.
- Everyone using a shared demo link uses the owner's API quota.

---

## ⚠️ Limitations

- **Scanned (image-only) PDFs** are not supported because there is no OCR.
- The whole document is sent with each request, and text beyond 600,000 characters is cut off.
- Like any LLM, the model can make mistakes. Check important answers against the PDF.
- One document at a time, with no login and no saved history.

---

## 🛣️ Roadmap

- [ ] OCR support for scanned PDFs
- [ ] Retrieval-augmented generation (RAG) for very large documents and multiple files
- [ ] Page citations in answers
- [ ] Streaming responses
- [ ] Interactive quiz with scoring
- [ ] Saved chat history and user accounts
- [ ] Automated tests and pinned dependency versions

---

## 🙌 Acknowledgements

Built with [Streamlit](https://streamlit.io), [PyMuPDF](https://pymupdf.readthedocs.io) and the [Google Gemini API](https://ai.google.dev).
