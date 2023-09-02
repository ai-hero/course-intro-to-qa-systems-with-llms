"""Test hello_world.hello module."""
from hello_world.hello import greet


def test_greet() -> None:
    """Test greet() function."""
    assert greet("World") == "Hello, World!"
