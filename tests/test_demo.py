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
