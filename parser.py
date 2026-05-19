import json
from pydantic import BaseModel, Field
from typing import List


class BlogOutline(BaseModel):
    """Pydantic model representing the structured blog outline output."""

    blog_title: str = Field(..., description="The engaging title of the blog post")
    outline_sections: List[str] = Field(
        ..., description="List of logical sections/headings for the blog"
    )
    target_audience: str = Field(..., description="The intended audience for the blog")
    writing_goal: str = Field(..., description="The primary goal or purpose of the blog")


def parse_output(raw_text: str) -> BlogOutline:
    """
    Parse the raw LLM output (JSON string) into a BlogOutline Pydantic model.
    Raises ValueError if parsing fails.
    """
    # Strip markdown code fences if present
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM did not return valid JSON.\nRaw output:\n{raw_text}\nError: {e}")

    # Validate with Pydantic
    blog_outline = BlogOutline(**data)
    return blog_outline


def format_output(blog_outline: BlogOutline) -> str:
    """Return a pretty-printed JSON string of the blog outline."""
    return blog_outline.model_dump_json(indent=2)
