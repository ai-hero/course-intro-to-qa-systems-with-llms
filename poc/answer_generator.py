"""
    Helper functions to generate an answer given a question, relevant context.
"""
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

# Load the .env file
load_dotenv()

# Set up the OpenAI API key
assert os.getenv("OPENAI_API_KEY"), "Please set your OPENAI_API_KEY environment variable."

client = OpenAI()


def answer_question(question: str, context: str) -> Any:
    """Answer a question given a context."""
    if not question.endswith("?"):
        question = question + "?"

    # Combine the summaries into a prompt and use SotA GPT-4 to answer.
    prompt = (
        "Use the following summaries of conversations on the MLOps.community slack channel"
        "to generate an answer for the user question. "
        "If the answer is not in the context, reply 'I don't know'. "
        "If the answer contains some personal information, remove it before answering. "
        "But if it cannot be removed, please politely decline to answer."
        "\nContext:```\n"
        f"{context}"
        "```"
        f"\nQuestion: {question}"
    )
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    content = completion.choices[0].message.content
    return content
