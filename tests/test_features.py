"""Test add feature functions."""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

from animal_shelter import features


def test_add_features() -> None:
    """Test general add feature function."""
    s = pd.DataFrame(
        data={
            "animal_type": ["Dog", "Cat", "Dog"],
            "name": ["Ivo", "Henk", "unknown"],
            "sex_upon_outcome": ["Intact Female", "Neutered Male", "Spayed Female"],
            "breed": ["unknown", "shorthair", "unknown"],
            "age_upon_outcome": ["10 months", "2 years", "4 months"],
            "is_dog": [True, False, True],
            "has_name": [True, True, False],
            "sex": ["female", "male", "female"],
            "neutered": ["intact", "fixed", "fixed"],
            "hair_type": [
                "Labrador Retriever Mix",
                "Domestic Shorthair Mix",
                "Collie Smooth Mix",
            ],
            "days_upon_outcome": [300.0, 730.0, 120.0],
        }
    )
    result = features.add_features(s)
    assert_frame_equal(result, s)


def test_exceptions_add_features() -> None:
    """Test general add feature function for exceptions."""
    with pytest.raises(BaseException):
        features.add_features()


def test_check_is_dog() -> None:
    """Test is dog function."""
    s = pd.Series(["Dog", "Cat", "Dog"])
    result = features._check_is_dog(s)
    expected = pd.Series([True, False, True])
    assert_series_equal(result, expected)


def test_exceptions_check_is_dog() -> None:
    """Test is dog function on exceptions."""
    with pytest.raises(BaseException):
        features._check_is_dog()


def test_check_has_name() -> None:
    """Test has name function."""
    s = pd.Series(["Ivo", "Henk", "unknown"])
    result = features._check_has_name(s)
    expected = pd.Series([True, True, False])
    assert_series_equal(result, expected)


def test_exceptions_get_sex() -> None:
    """Test get sex function on exceptions."""
    with pytest.raises(BaseException):
        features._get_sex()


@pytest.fixture  # type: ignore[misc]
def list_of_sex() -> pd.Series:
    """Create input for get sex and neutered function."""
    return pd.Series(["Intact Female", "Neutered Male", "Spayed Female"])


def test_get_sex(list_of_sex: pd.Series) -> None:
    """Test get sex function."""
    result = features._get_sex(list_of_sex)
    expected = pd.Series(["female", "male", "female"])
    assert_series_equal(result, expected)


def test_get_neutered(list_of_sex: pd.Series) -> None:
    """Test get neutered function."""
    result = features._get_neutered(list_of_sex)
    expected = pd.Series(["intact", "fixed", "fixed"])
    assert_series_equal(result, expected)


def test_get_hair_type() -> None:
    """Test get hair type function."""
    s = pd.Series(
        ["Labrador Retriever Mix", "Domestic Shorthair Mix", "Collie Smooth Mix"]
    )
    result = features._get_hair_type(s)
    expected = pd.Series(["unknown", "shorthair", "unknown"])
    assert_series_equal(result, expected)


def test_compute_days_upon_outcome() -> None:
    """Test compute days upon outcome function."""
    s = pd.Series(["10 months", "2 years", "4 months"])
    result = features._compute_days_upon_outcome(s)
    expected = pd.Series([300.0, 730.0, 120.0])
    assert_series_equal(result, expected)
