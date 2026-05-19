"""
app.py — Beautiful Streamlit UI for the Blog Topic & Outline Generator.
Run with: streamlit run app.py
"""

import json
import streamlit as st
from prompt import blog_outline_prompt
from model import call_llm
from parser import parse_output

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blog Outline Generator",
    page_icon="✍️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0e0e12;
    color: #f0ede6;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #1a1a2e 0%, #0e0e12 60%),
                radial-gradient(ellipse at 80% 90%, #16213e 0%, transparent 60%);
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
* { font-family: 'DM Sans', sans-serif; }

.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #f5a623, #e8832a);
    color: #0e0e12;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.3rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 900;
    line-height: 1.1;
    color: #f0ede6;
    margin: 0 0 1rem;
    letter-spacing: -0.02em;
}
.hero-title span {
    background: linear-gradient(135deg, #f5a623 0%, #e8832a 50%, #d4520a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: #8a8a9a;
    font-size: 1rem;
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}
.fancy-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
}
.fancy-divider::before, .fancy-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a3a, transparent);
}
.fancy-divider span { color: #3a3a4a; font-size: 1rem; }

.input-card {
    background: linear-gradient(145deg, #16161f, #1a1a28);
    border: 1px solid #2a2a3a;
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #0e0e12 !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 12px !important;
    color: #f0ede6 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #f5a623 !important;
    box-shadow: 0 0 0 3px rgba(245,166,35,0.1) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSlider"] label {
    color: #c0bdb6 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

[data-testid="stFormSubmitButton"] button,
.stButton button {
    background: linear-gradient(135deg, #f5a623, #d4520a) !important;
    color: #0e0e12 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(245,166,35,0.3) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFormSubmitButton"] button:hover,
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(245,166,35,0.4) !important;
}

.result-wrapper { animation: fadeUp 0.5s ease forwards; }
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.title-card {
    background: linear-gradient(135deg, #1e1a0e, #1a1a28);
    border: 1px solid #f5a62333;
    border-left: 4px solid #f5a623;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
}
.title-card .label {
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: #f5a623; margin-bottom: 0.6rem;
}
.title-card .blog-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem; font-weight: 700;
    color: #f0ede6; line-height: 1.3; margin: 0;
}
.meta-row { display: flex; gap: 1rem; margin-bottom: 1.2rem; flex-wrap: wrap; }
.meta-card {
    flex: 1; min-width: 180px;
    background: #16161f;
    border: 1px solid #2a2a3a;
    border-radius: 14px; padding: 1.2rem;
}
.meta-card .label {
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: #8a8a9a; margin-bottom: 0.5rem;
}
.meta-card .value { font-size: 0.9rem; color: #f0ede6; line-height: 1.5; }
.outline-card {
    background: #16161f;
    border: 1px solid #2a2a3a;
    border-radius: 16px; padding: 1.8rem; margin-bottom: 1.2rem;
}
.outline-card .label {
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: #8a8a9a; margin-bottom: 1.2rem;
}
.section-item {
    display: flex; align-items: flex-start; gap: 1rem;
    padding: 0.8rem 0; border-bottom: 1px solid #1e1e2a;
}
.section-item:last-child { border-bottom: none; }
.section-num {
    background: linear-gradient(135deg, #f5a623, #e8832a);
    color: #0e0e12; font-size: 0.7rem; font-weight: 800;
    width: 26px; height: 26px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
}
.section-text { font-size: 0.95rem; color: #d0cdc6; line-height: 1.5; }
.json-card {
    background: #0a0a0f; border: 1px solid #2a2a3a;
    border-radius: 14px; padding: 1.5rem; margin-bottom: 1.2rem;
}
.json-card .label {
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: #8a8a9a; margin-bottom: 1rem;
}
.json-card pre {
    color: #7ec8a0; font-size: 0.8rem; line-height: 1.6;
    overflow-x: auto; margin: 0; white-space: pre-wrap; word-break: break-word;
}
.success-banner {
    background: linear-gradient(135deg, #0d2018, #0a1a10);
    border: 1px solid #1e5c36; border-radius: 12px;
    padding: 0.8rem 1.2rem; color: #4ade80;
    font-size: 0.9rem; font-weight: 500; margin-bottom: 1.5rem;
}
.error-banner {
    background: #1a0a0a; border: 1px solid #5c1e1e;
    border-radius: 12px; padding: 0.8rem 1.2rem;
    color: #f87171; font-size: 0.9rem; margin-bottom: 1rem;
}
.footer {
    text-align: center; padding: 2rem 0 1rem;
    color: #3a3a4a; font-size: 0.78rem; letter-spacing: 0.05em;
}
[data-testid="stDownloadButton"] button {
    background: #16161f !important;
    color: #f5a623 !important;
    border: 1px solid #f5a62355 !important;
    box-shadow: none !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #1e1e2e !important;
    border-color: #f5a623 !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Content Tool</div>
    <h1 class="hero-title">Blog <span>Outline</span><br>Generator</h1>
    <p class="hero-sub">Transform any topic into a structured, compelling blog outline in seconds using generative AI.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"><span>✦</span></div>', unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
with st.form("blog_form"):
    topic = st.text_input(
        "📌 Blog Topic or Niche",
        placeholder="e.g.  Artificial Intelligence in Healthcare",
    )
    audience = st.text_input(
        "🎯 Target Audience  (optional)",
        placeholder="e.g.  General readers interested in technology",
    )
    temperature = st.slider(
        "🎨 Creativity Level",
        min_value=0.0, max_value=1.0, value=0.7, step=0.1,
        help="Higher = more creative output"
    )
    submitted = st.form_submit_button("✦  Generate My Blog Outline", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Output ────────────────────────────────────────────────────────────────────
if submitted:
    if not topic.strip():
        st.markdown('<div class="error-banner">⚠️ Please enter a blog topic before generating.</div>', unsafe_allow_html=True)
    else:
        audience_val = audience.strip() if audience.strip() else "General readers"
        with st.spinner("✦  Crafting your outline..."):
            try:
                formatted_prompt = blog_outline_prompt.format(topic=topic, audience=audience_val)
                raw_output = call_llm(formatted_prompt, temperature=temperature)
                result = parse_output(raw_output)

                st.markdown('<div class="success-banner">✓ &nbsp; Blog outline generated successfully!</div>', unsafe_allow_html=True)
                st.markdown('<div class="result-wrapper">', unsafe_allow_html=True)

                st.markdown(f"""
                <div class="title-card">
                    <div class="label">✦ Blog Title</div>
                    <p class="blog-title">{result.blog_title}</p>
                </div>""", unsafe_allow_html=True)

                st.markdown(f"""
                <div class="meta-row">
                    <div class="meta-card">
                        <div class="label">🎯 Target Audience</div>
                        <div class="value">{result.target_audience}</div>
                    </div>
                    <div class="meta-card">
                        <div class="label">🖊️ Writing Goal</div>
                        <div class="value">{result.writing_goal}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                sections_html = "".join([
                    f'<div class="section-item"><div class="section-num">{i}</div><div class="section-text">{s}</div></div>'
                    for i, s in enumerate(result.outline_sections, 1)
                ])
                st.markdown(f"""
                <div class="outline-card">
                    <div class="label">📋 Article Outline</div>
                    {sections_html}
                </div>""", unsafe_allow_html=True)

                json_str = json.dumps(result.model_dump(), indent=2)
                st.markdown(f"""
                <div class="json-card">
                    <div class="label">🗂️ JSON Output</div>
                    <pre>{json_str}</pre>
                </div>""", unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                st.download_button(
                    label="⬇️  Download as JSON",
                    data=json_str,
                    file_name="blog_outline.json",
                    mime="application/json",
                    use_container_width=True,
                )

            except EnvironmentError as e:
                st.markdown(f'<div class="error-banner">🔑 API Key Error: {e}</div>', unsafe_allow_html=True)
            except ValueError as e:
                st.markdown(f'<div class="error-banner">⚠️ Parsing Error: {e}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-banner">❌ Error: {e}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with LangChain · Groq · Streamlit &nbsp;|&nbsp; Innomatics Research Labs
</div>
""", unsafe_allow_html=True)
