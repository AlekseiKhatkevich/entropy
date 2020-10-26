from djoser import serializers as djoser_serializers


class CustomUserCreateSerializer(djoser_serializers.UserCreateSerializer):
    """
    Custom user creation serializer.user in /auth/users/:POST endpoint.
    Added possibility to specify user nickname and timezone on creation
    """
    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        fields = djoser_serializers.UserCreateSerializer.Meta.fields + (
            'nickname',
            'timezone',
        )





