from rest_framework import serializers


class ErrorsSerializer(serializers.Serializer):
    """
    Serializer for project errors.
    """
    error_code = serializers.CharField(
        read_only=True,
    )
    title = serializers.CharField(
        read_only=True,
    )
    detail = serializers.CharField(
        read_only=True,
    )
