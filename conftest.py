import pytest


# AUTO-USE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @pytest.fixture(autouse=True)
# def this_would_be_ran_in_each_test():
#     """
#     Code here would be ran in each test (method i guess ???)
#     """
#     print('I am run in each test. Please switch me off')


# USERS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
