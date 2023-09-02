"""Test hello_world.hello module."""
from introduction.hello_chatgpt import get_response


def test_greet() -> None:
    """Test greet() function."""
    assert get_response(
        [{"role": "user", "content": "Hello, my name is Rahul."}], stream=False
    ), "Unable to test openai.ChatCompletion.create()"
