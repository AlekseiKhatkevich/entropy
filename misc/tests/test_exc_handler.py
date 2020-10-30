from collections import namedtuple

from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response

from entropy.errors import messages
from entropy.exception_handlers import custom_exception_handler


class TestCustomExceptionHandlerPositive:
    """
    Positive test on project level custom exception handler.
    """
    handler = custom_exception_handler
    request_factory = namedtuple('request_factory', ('path',))
    path = r'/test/test/'
    request = request_factory(path)
    context = {'request': request}

    assert request.path == path

    def test_validation_error_standard(self):
        """
        Check that serializers ValidationError with standard
        error messages (not instances of ErrorMessage class) can be successfully placed
        inside DRF Response without modification.
        """

        drf_validation_error = serializers.ValidationError({
            'test_field': [
                ErrorDetail('test_message', 'test_code', )
                ]})

        response = custom_exception_handler(
            drf_validation_error,
            self.context,
        )

        assert response is not None
        assert isinstance(response, Response)
        assert response.data['test_field'] == ['test_message']

    def test_builtin_exc(self):
        """
        Check that built in python exception would be passed through unmodified.
        """
        exception = KeyError('test_message')

        response = custom_exception_handler(
            exception,
            self.context,
        )

        assert response is None

    def test_exc_with_ErrorMessage(self):
        """
        Check that validation error with ErrorMessage code in .code attribute would be transformed in
        the following fields
                    'type'
                    'title'
                    'status'
                    'detail'
                    'instance'
        """
        message_instance = messages.user_2
        drf_validation_error = serializers.ValidationError({
            'test_field': [
                ErrorDetail(*messages.user_2)
            ]})
        expected_error_view = {
            'type': message_instance.error_code,
            'title': message_instance.title,
            'status': drf_validation_error.status_code,
            'detail': message_instance.detail,
            'instance': self.context['request'].path,
        }

        response = custom_exception_handler(
            drf_validation_error,
            self.context,
        )

        assert response is not None
        assert isinstance(response, Response)
        assert response.data['test_field'] == [expected_error_view]
