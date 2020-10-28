from pytest_fixtures.users_fixtures import (
    user_initial_data,
    one_test_user,
    jwt_auth_header,
)
from pytest_fixtures.misc_fixtures import (
    api_client
)

# AUTO-USE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @pytest.fixture(autouse=True)
# def this_would_be_ran_in_each_test():
#     """
#     Code here would be ran in each test (method i guess ???)
#     """
#     print('I am getting ran in each test. Please switch me off')


# Run before all tests
# def runme():
#     print('HERE!!!!!!!!!!!!!')