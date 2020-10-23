from entropy.errors.schema import ErrorMessage


class TestErrorsSchema:
    """
    Positive tests on error dataclass
    """
    example_error = ErrorMessage(
        section='test',
        error_code_number=1,
        title='Test message',
        detail='This is a test message',
    )
    example_error_2 = ErrorMessage(
        section='test',
        error_code_number=1,
        title='Unique message',
        detail='This is a unique message',
    )
    example_error_3 = ErrorMessage(
        section='py-test',
        error_code_number=228,
        title='Py-test, really???',
        detail='Please consider it...',
    )

    def test_iter(self):
        """
        Check that __iter__ method would return a generator object (self, self.error_code)
        """
        # noinspection PyTupleAssignmentBalance
        error, code = self.example_error

        assert isinstance(error, ErrorMessage)
        assert code == self.example_error.error_code

    def test_new(self):
        """
        Check that there are can be one and only one instance with unique error_code
        """
        assert id(self.example_error) == id(self.example_error_2) != id(self.example_error_3)
