"""
main.py — CLI entry point for the Blog Topic & Outline Generator.

Usage:
    python main.py
    python main.py --topic "Machine Learning" --audience "Beginners"
"""

import argparse
import json
from prompt import blog_outline_prompt
from model import call_llm
from parser import parse_output, format_output


def generate_blog_outline(topic: str, audience: str = "") -> dict:
    """
    Full pipeline: format prompt → call LLM → parse output → return structured result.

    Args:
        topic: The blog topic or niche.
        audience: (Optional) The intended audience.

    Returns:
        A dictionary with blog_title, outline_sections, target_audience, writing_goal.
    """
    # Handle missing audience gracefully
    if not audience.strip():
        audience = "General readers"

    # Format the prompt
    formatted_prompt = blog_outline_prompt.format(topic=topic, audience=audience)

    print(f"\n📝 Generating blog outline for topic: '{topic}'...")
    print(f"   Audience: {audience}\n")

    # Call LLM
    raw_output = call_llm(formatted_prompt)

    # Parse and validate output
    blog_outline = parse_output(raw_output)

    return blog_outline.model_dump()


def display_output(result: dict) -> None:
    """Pretty-print the result to the terminal."""
    print("=" * 60)
    print("✅  BLOG OUTLINE GENERATED")
    print("=" * 60)
    print(f"\n📌 Blog Title:\n   {result['blog_title']}")
    print(f"\n🎯 Target Audience:\n   {result['target_audience']}")
    print(f"\n🖊️  Writing Goal:\n   {result['writing_goal']}")
    print("\n📋 Outline Sections:")
    for i, section in enumerate(result["outline_sections"], 1):
        print(f"   {i}. {section}")
    print("\n" + "=" * 60)
    print("\n🗂️  Full JSON Output:\n")
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Blog Topic & Outline Generator using Generative AI"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="",
        help="The blog topic or niche (e.g. 'Artificial Intelligence in Healthcare')",
    )
    parser.add_argument(
        "--audience",
        type=str,
        default="",
        help="Target audience (optional, e.g. 'Beginners in technology')",
    )
    args = parser.parse_args()

    # Interactive mode if no args provided
    topic = args.topic
    audience = args.audience

    if not topic:
        print("\n🤖 Blog Topic & Outline Generator")
        print("-" * 40)
        topic = input("Enter the blog topic or niche: ").strip()
        if not topic:
            print("❌ Topic cannot be empty. Exiting.")
            return
        audience = input("Enter target audience (press Enter to skip): ").strip()

    result = generate_blog_outline(topic=topic, audience=audience)
    display_output(result)


if __name__ == "__main__":
    main()
