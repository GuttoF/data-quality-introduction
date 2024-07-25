from app.hello_function import hello_world


def test_hello_world():
    function_result = hello_world()
    expected_result = "Hello, World!"
    assert function_result == expected_result
