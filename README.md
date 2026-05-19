# ✍️ Blog Topic & Outline Generator

A Generative AI application that takes a **topic** and **audience** as input and produces a **structured blog outline** with a compelling title, logical sections, target audience, and writing goal.

Built with **LangChain · OpenAI GPT-4o-mini · Pydantic · Streamlit**

---

## 📁 Project Structure

```
blog_outline_generator/
│
├── prompt.py          # LangChain PromptTemplate
├── model.py           # LLM initialization & API call
├── parser.py          # Pydantic model + JSON output parser
├── main.py            # CLI entry point
├── app.py             # Streamlit web UI
├── requirements.txt   # Python dependencies
├── .env.example       # API key template
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone / Download the project

```bash
cd blog_outline_generator
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

```bash
cp .env.example .env
# Open .env and set your OpenAI API key:
# OPENAI_API_KEY=sk-...
```

---

## 🚀 Running the Application

### Option A — Streamlit Web UI (Recommended)

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

### Option B — CLI (Interactive Mode)

```bash
python main.py
```

### Option C — CLI (With Arguments)

```bash
python main.py --topic "Machine Learning in Finance" --audience "Finance professionals"
```

---

## 📤 Output Schema

```json
{
  "blog_title": "string",
  "outline_sections": ["string"],
  "target_audience": "string",
  "writing_goal": "string"
}
```

---

## 🧪 Test Cases

| Scenario | Input | Expected Behaviour |
|---|---|---|
| Broad topic | "Technology" | General-purpose 5–7 section outline |
| Narrow topic | "CRISPR Gene Editing in Cancer Treatment" | Focused, technical sections |
| Missing audience | Topic only, no audience | Infers a suitable audience |

---

## 🏗️ Architecture

```
User Input (Topic + Audience)
        │
        ▼
  PromptTemplate (prompt.py)
        │  Formats structured prompt
        ▼
    LLM Call (model.py)
        │  GPT-4o-mini via LangChain
        ▼
  Output Parser (parser.py)
        │  JSON → Pydantic BlogOutline
        ▼
  Structured Output → CLI / Streamlit UI
```

---

## ☁️ Deployment

### Streamlit Cloud

1. Push code to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) → New App.
3. Select your repo and set `app.py` as the entry point.
4. Add `OPENAI_API_KEY` in **Secrets** (Settings → Secrets).

### Hugging Face Spaces

1. Create a new Space with **Streamlit** SDK.
2. Upload all files.
3. Add `OPENAI_API_KEY` to **Space Secrets**.

---

## 🔐 Security Notes

- Never hardcode API keys in source code.
- `.env` is listed in `.gitignore` — only `.env.example` is committed.
- Always use environment variables for secrets in production.

---

*Innomatics Research Labs — Generative AI Project*
