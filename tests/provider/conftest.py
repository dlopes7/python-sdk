import pytest

from open_feature import open_feature as of


@pytest.fixture()
def no_op_provider_client():
    return of.client()
