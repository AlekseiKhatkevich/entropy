import pytest


@pytest.fixture(scope='function')
def user_initial_data() -> dict:
    """
    Creates positive initial data for user instance creation.
    :return: dict with user's data
    """
    initial_data = dict(
        email='test@email.com',
        password='1q2w3e',
        nickname='testuser',
        timezone='Iceland',
    )
    return initial_data
