"""A simple chatbot using the OpenAI API."""
import os
from typing import Any, Dict, Generator, List, Union

import openai
import streamlit as st
from dotenv import load_dotenv

MODEL_NAME = "gpt-3.5-turbo"
ResponseType = Union[Generator[Any, None, None], Any, List, Dict]

# Load the .env file
load_dotenv()

# Set up the OpenAI API key
assert os.getenv("OPENAI_API_KEY"), "Please set your OPENAI_API_KEY environment variable."
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_response(messages: List[Dict[str, Any]], stream: bool = True) -> ResponseType:
    """Get response from OpenAI API."""
    return openai.ChatCompletion.create(model=MODEL_NAME, messages=messages, stream=stream)


def main() -> None:
    """Run the chatbot."""
    st.title("Chat with the MLOps.Community 👋")

    if "messages" not in st.session_state:
        # Priming the model with a message
        # To create a custom chatbot.
        # Feel free to change the message to whatever you want.
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    # Identity
                    "Your name is Milo. You are a chatbot representing the MLOps Community. "
                    # Purpose
                    "Your purpose is to answer questions about the MLOps Community. "
                    # Introduce yourself
                    "Introduce yourself to the user. "
                    # Scoping
                    "Please answer the user's questions based on what you known about the commmumnity. "
                    "If the question is outside scope of AI, Machine Learning, or MLOps, please politely decline. "
                    "Answer questions in the scope of what you know about the community. "
                    "If you don't know the answer, please politely decline. "
                ),
            }
        ]

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

        message = get_response(st.session_state.messages)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in get_response(st.session_state.messages, stream=True):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
