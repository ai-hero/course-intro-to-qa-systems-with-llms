"""Test hello_world.hello module."""
from introduction.hello_chatgpt import get_response


def test_greet() -> None:
    """Test greet() function."""
    response = get_response([{"role": "user", "content": "Hello, my name is Rahul."}], stream=False)
    message = response.choices[0]["message"]  # type: ignore[union-attr]
    assert "role" in message, "Response should have a role."
    assert message["role"] == "assistant", "Response should have assistant role."
    assert "content" in message, "Response should have content."
