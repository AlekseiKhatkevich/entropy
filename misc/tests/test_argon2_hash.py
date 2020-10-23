from entropy import password_hashers


class TestArgon2Hasher:
    """
    Positive test on argon2 password hasher.
    """

    def test_created_user_hash_type(self, django_user_model, user_initial_data):
        """
        Check that 'argon2' hasher is used by default
        """
        user = django_user_model(**user_initial_data)
        user.set_password(user.password)
        algorithm_name = password_hashers.CustomArgon2PasswordHasher.algorithm

        assert user.password.startswith(algorithm_name)
