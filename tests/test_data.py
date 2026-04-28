"""Test data on output and exceptions."""

import pytest

from animal_shelter import data


def test_convert_camel_case() -> None:
    """Test output of convert camel case function."""
    assert data.convert_camel_case("CamelCase") == "camel_case"
    assert data.convert_camel_case("CamelCASE") == "camel_case"
    assert data.convert_camel_case("camel-case") != "camel_case"
    assert data.convert_camel_case("camel_case") == "camel_case"
    assert data.convert_camel_case("camel case") != "camel_case"


def test_for_exceptions() -> None:
    """Test exception of convert camel case function."""
    with pytest.raises(TypeError) as exception:
        data.convert_camel_case(10)
    assert "str" in str(exception.value)


def test_for_exceptions_2() -> None:  # Is the same as the previous one
    """Test exception of convert camel case funciton in another way."""
    with pytest.raises(TypeError, match="str"):
        data.convert_camel_case(10)
