from django.contrib.auth.hashers import Argon2PasswordHasher


class CustomArgon2PasswordHasher(Argon2PasswordHasher):
    """
    Customized Argon2 password hasher.
    """
    algorithm = 'argon2id'
    library = 'argon2'

