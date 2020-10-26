from djoser import serializers as djoser_serializers


class CustomUserSerializer(djoser_serializers.UserSerializer):
    """
    Custom serializer for /users/ endpoint.
    Adds possibility to create extra fields in user model during user registration.
    """

    class Meta(djoser_serializers.UserSerializer.Meta):
         pass

    def to_representation(self, instance):

        # rep = super().to_representation(instance)
        # rep['test'] = True
        # return rep
        pass