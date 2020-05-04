import pytest

from beethon.management.decorators import register


@pytest.mark.unit
def test_register_wrong_class():
    with pytest.raises(TypeError):

        @register()
        class SomeClass:
            pass


@pytest.mark.unit
def test_register_with_wrong_handler():
    with pytest.raises(TypeError):

        class SomeHandler:
            pass

        @register(with_handler=SomeHandler)
        class SomeClass:
            pass
