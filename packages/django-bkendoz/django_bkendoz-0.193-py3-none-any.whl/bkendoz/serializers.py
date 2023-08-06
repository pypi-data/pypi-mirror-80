from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import GenericUser

class GenericUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = GenericUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = GenericUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'style',
        )

        validators = [
            UniqueTogetherValidator(
                queryset=GenericUser.objects.all(),
                fields=['username', 'email']
            )
        ]
