"""Demo app"""
from typing import Any

import httpx
import streamlit as st


def send_question(question: str) -> Any:
    """Send the question to the chat service and get the response."""
    url = "http://localhost:8080/chat"
    response = httpx.post(url, json={"question": question}, timeout=30)
    return response.json()


def main() -> None:
    """main"""
    st.title("Milo - Your Q&A Buddy")

    # User inputs their question
    question = st.text_input("What's your question?")

    if st.button("Ask Milo"):
        if question:
            # Send the question to the chat service
            response = send_question(question)
            if response:
                # Display the answer
                st.success(response.get("answer", "No response from the service."))
            else:
                st.error("Failed to get a response.")
        else:
            st.warning("Please enter a question.")


if __name__ == "__main__":
    main()
