import pytest

from dsa.stack import Stack, is_balanced


def test_last_in_first_out():
    s = Stack()
    for v in [1, 2, 3]:
        s.push(v)
    assert s.peek() == 3
    assert len(s) == 3
    assert [s.pop(), s.pop(), s.pop()] == [3, 2, 1]
    assert s.is_empty()


def test_empty_stack_errors():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()


@pytest.mark.parametrize(
    "text",
    ["", "()", "([]{})", "{[()()]}", "a(b)c[d]", "no brackets"],
)
def test_balanced(text):
    assert is_balanced(text)


@pytest.mark.parametrize(
    "text",
    ["(", ")", "(]", "([)]", "(()", "())", "}{"],
)
def test_not_balanced(text):
    assert not is_balanced(text)
