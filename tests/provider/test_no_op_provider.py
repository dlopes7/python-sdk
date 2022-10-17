from numbers import Number

from open_feature import open_feature as of
from open_feature.provider.no_op import NoOpProvider


def setup():
    provider = of.provider
    assert isinstance(provider, NoOpProvider)


def test_should_get_boolean_flag_from_no_op(no_op_provider_client):
    # Given
    # When
    flag = no_op_provider_client.get_boolean_details(key="Key", default=True)
    # Then
    assert flag is not None
    assert flag.value
    assert isinstance(flag.value, bool)


def test_should_get_number_flag_from_no_op(no_op_provider_client):
    # Given
    # When
    flag = no_op_provider_client.get_number_details(key="Key", default=100)
    # Then
    assert flag is not None
    assert flag.value == 100
    assert isinstance(flag.value, Number)


def test_should_get_string_flag_from_no_op(no_op_provider_client):
    # Given
    # When
    flag = no_op_provider_client.get_string_details(key="Key", default="String")
    # Then
    assert flag is not None
    assert flag.value == "String"
    assert isinstance(flag.value, str)


def test_should_get_dict_flag_from_no_op(no_op_provider_client):
    # Given
    return_value = {
        "String": "string",
        "Number": 2,
        "Boolean": True,
    }
    # When
    flag = no_op_provider_client.get_dict_details(
        key="Key", default=return_value
    )
    # Then
    assert flag is not None
    assert flag.value == return_value
    assert isinstance(flag.value, dict)
