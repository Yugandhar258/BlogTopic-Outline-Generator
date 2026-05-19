from langchain_core.prompts import PromptTemplate

blog_outline_prompt = PromptTemplate(
    input_variables=["topic", "audience"],
    template="""
You are an expert content strategist and blog writer.

Given the following topic and audience, generate a compelling blog title, 
a well-structured outline with 5-7 sections, the target audience, 
and the writing goal of the blog.

TOPIC: {topic}
AUDIENCE: {audience}

Respond ONLY with a valid JSON object. Do not include any explanation, 
markdown, or extra text. Use this exact schema:

{{
  "blog_title": "string",
  "outline_sections": ["string", "string", ...],
  "target_audience": "string",
  "writing_goal": "string"
}}

Guidelines:
- blog_title: Make it engaging, clear, and SEO-friendly.
- outline_sections: List 5-7 logical sections that flow naturally.
- target_audience: Be specific about who will benefit from the blog.
- writing_goal: One sentence describing the blog's purpose.
- If audience is not provided, infer a suitable audience from the topic.
"""
)