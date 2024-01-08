"""A simple chatbot using the OpenAI API."""
import os
from typing import Any, Dict, List

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

MODEL_NAME = "gpt-3.5-turbo"

# Load the .env file
load_dotenv()

# Set up the OpenAI API key
assert os.getenv("OPENAI_API_KEY"), "Please set your OPENAI_API_KEY environment variable."
client = OpenAI()


def get_response(messages: List[Dict[str, Any]], stream: bool = True) -> Any:
    """Get response from OpenAI API."""
    response = client.chat.completions.create(model=MODEL_NAME, messages=messages, stream=stream)
    if stream:
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    else:
        return response.choices[0].message.content


SCOPE = False


def main() -> None:
    """Run the chatbot."""
    st.title("Chat with Milo, from MLOps.Community 👋")

    if "messages" not in st.session_state:
        # Priming the model with a message
        # To create a custom chatbot.
        system_prompt = (
            # Identity
            "Your name is Milo. You are a chatbot representing the MLOps Community. "
            # Purpose
            "Your purpose is to answer questions about the MLOps Community. "
            # Introduce yourself
            "If the user says hi, introduce yourself to the user."
        )
        if SCOPE:
            system_prompt += (
                # Scoping
                "Please answer the user's questions based on what you known about the commmumnity. "
                "If the question is outside scope of AI, Machine Learning, or MLOps, please politely decline. "
                "Answer questions in the scope of what you know about the community. "
                "If you don't know the answer, please politely decline. "
            )
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] not in ["user", "assistant"]:
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input and get response from OpenAI API
    if prompt := st.chat_input():
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for token in get_response(st.session_state.messages, stream=True):
                full_response += token
                message_placeholder.markdown(full_response + " ")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
