from rest_framework import generics

from entropy.errors import messages
from misc.serializers import ErrorsSerializer


class ErrorsListView(generics.ListAPIView):
    """
    Displays all possible project errors.
    """
    serializer_class = ErrorsSerializer

    def get_queryset(self):
        return [msg for msg in vars(messages).values() if isinstance(msg, messages.ErrorMessage)]
