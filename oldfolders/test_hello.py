from hello1 import hello


def test_default():
    assert hello() == "hello, world"
    
def test_argument():
    for name in ["Herione", "Harry", "Ron"]:
        assert hello(name) == f"hello, {name}"
    if 