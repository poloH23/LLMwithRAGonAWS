import sys


def test_python_version():
    assert sys.version_info >= (3, 9), "Python 3.9 or above is required."


def test_math_basics():
    assert 1 + 1 == 2
    assert isinstance(3.14, float)


def test_list_append():
    data = []
    data.append("item")
    assert len(data) == 1
    assert data[0] == "item"


def test_token():
    from lib.token_utils import get_line_access
    from lib.token_utils import get_line_secret

    token = get_line_access()
    secret = get_line_secret()
    assert token != "", print(token)
    assert secret != "", print(secret)
