import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUserModelPositive:
    """
    Positive test on User model
    """
    initial_data = dict(
        email='test@email.com',
        password='argon2id$argon2i$v=19$m=512,t=2,p=2$SDV5RzU4eG5OcWU0$o1+GMGzgCYNOi8fBTqgmYQ',
        nickname='testuser',
        timezone='Iceland',
    )

    def test_model_creation(self):
        """
        Check that if correct data is provided, then User model instance can be created.
        """
        get_user_model().objects.create(**self.initial_data)

        assert get_user_model().objects.filter(**self.initial_data).exists()

