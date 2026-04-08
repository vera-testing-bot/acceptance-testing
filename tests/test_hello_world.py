from src.hello_world import hello_world


def test_hello_world_content():
    result = hello_world()
    assert result.lower() == "hello world"


def test_hello_world_random_capitalization():
    results = {hello_world() for _ in range(50)}
    assert len(results) > 1, "Expected random capitalization to produce varied output"
