"""
app.py — Streamlit Web UI for the Blog Topic & Outline Generator.

Run with:
    streamlit run app.py
"""

import json
import streamlit as st
from prompt import blog_outline_prompt
from model import call_llm
from parser import parse_output

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blog Outline Generator",
    page_icon="✍️",
    layout="centered",
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("✍️ Blog Topic & Outline Generator")
st.markdown(
    "Generate a compelling blog title and a structured article outline "
    "powered by **Generative AI**."
)
st.divider()

# ── Input Form ────────────────────────────────────────────────────────────────
with st.form("blog_form"):
    topic = st.text_input(
        "📌 Blog Topic or Niche *",
        placeholder="e.g. Artificial Intelligence in Healthcare",
    )
    audience = st.text_input(
        "🎯 Target Audience (optional)",
        placeholder="e.g. General readers interested in technology",
    )
    temperature = st.slider(
        "🎨 Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative titles; Lower = more predictable output",
    )
    submitted = st.form_submit_button("🚀 Generate Outline", use_container_width=True)

# ── Generation Logic ──────────────────────────────────────────────────────────
if submitted:
    if not topic.strip():
        st.error("⚠️ Please enter a blog topic before generating.")
    else:
        audience_val = audience.strip() if audience.strip() else "General readers"

        with st.spinner("🤖 AI is crafting your blog outline..."):
            try:
                formatted_prompt = blog_outline_prompt.format(
                    topic=topic, audience=audience_val
                )
                raw_output = call_llm(formatted_prompt, temperature=temperature)
                result = parse_output(raw_output)

                # ── Results ──────────────────────────────────────────────────
                st.success("✅ Blog outline generated successfully!")
                st.divider()

                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader("📝 Blog Title")
                    st.markdown(f"### {result.blog_title}")

                with col2:
                    st.subheader("🎯 Audience")
                    st.info(result.target_audience)

                st.subheader("🖊️ Writing Goal")
                st.markdown(f"> {result.writing_goal}")

                st.subheader("📋 Article Outline")
                for i, section in enumerate(result.outline_sections, 1):
                    st.markdown(f"**{i}.** {section}")

                st.divider()
                st.subheader("🗂️ JSON Output")
                st.json(result.model_dump())

                # ── Download Button ───────────────────────────────────────────
                json_str = json.dumps(result.model_dump(), indent=2)
                st.download_button(
                    label="⬇️ Download as JSON",
                    data=json_str,
                    file_name="blog_outline.json",
                    mime="application/json",
                    use_container_width=True,
                )

            except EnvironmentError as e:
                st.error(f"🔑 API Key Error: {e}")
            except ValueError as e:
                st.error(f"⚠️ Output Parsing Error: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected Error: {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center><small>Built with LangChain · OpenAI · Streamlit | "
    "Innomatics Research Labs</small></center>",
    unsafe_allow_html=True,
)
