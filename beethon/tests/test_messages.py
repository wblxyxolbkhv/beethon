import pytest

from beethon.messages.base import Request


@pytest.mark.unit
def test_register_wrong_class():
    with pytest.raises(ValueError):
        Request.parse("{}")
