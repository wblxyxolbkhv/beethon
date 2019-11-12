import pytest

from beethon.messages.base import Request


def test_register_wrong_class():
    with pytest.raises(ValueError):
        Request.parse("{}")
