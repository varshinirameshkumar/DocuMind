# 📄 DocuMind – AI-Powered PDF Assistant

Upload a PDF, then summarize it, chat with it, extract key points, or generate a quiz.
Built with **Python, Streamlit, PyMuPDF and the Google Gemini API**.

## Quick start

```bash
# 1. (optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt

# 3. add your API key (free: https://aistudio.google.com/apikey)
cp .env.example .env            # Windows: copy .env.example .env
#    then edit .env and paste your key

# 4. run
streamlit run app.py
```

If you skip step 3, the app will ask for the key in the sidebar.

## Features
- PDF upload and text extraction (PyMuPDF)
- Short / detailed summary
- Chat with your PDF (context-aware Q&A with history)
- Key point extraction
- Multiple-choice quiz with answer key (downloadable)

## Project structure
```
DocuMind/
├── app.py              # Streamlit UI
├── requirements.txt
├── .env.example        # copy to .env
├── utils/
│   ├── pdf_reader.py   # PDF text extraction
│   └── ai_helper.py    # Gemini prompts & API calls
└── README.md
```

## Deploy on Streamlit Community Cloud
1. Push to GitHub (`.env` is git-ignored – never upload your key).
2. Create the app at https://share.streamlit.io, main file `app.py`.
3. In **Settings → Secrets** add: `GEMINI_API_KEY = "your_key"`

## Notes
- Change the model with `GEMINI_MODEL` in `.env` (default `gemini-2.5-flash`).
- Scanned/image-only PDFs have no extractable text and need OCR first.
