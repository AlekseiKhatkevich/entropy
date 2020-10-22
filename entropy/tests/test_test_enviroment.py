import os


def test__test_environment():
    """
    Check that during test run Dynaconf environment is set to 'test'
    """
    environment = os.getenv('ENV_FOR_DYNACONF')

    assert environment == 'test'