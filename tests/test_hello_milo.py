"""Test hello_mlops"""
from introduction.hello_milo import get_response


def test_greet() -> None:
    """Test greet() function."""
    response = get_response([{"role": "user", "content": "Hello!"}], stream=False)
    message = response.choices[0]["message"]  # type: ignore[union-attr]
    assert "role" in message, "Response should have a role."
    assert message["role"] == "assistant", "Response should have assistant role."
    assert "content" in message, "Response should have content."
