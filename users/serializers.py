from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'telegram_chat_id',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Создание пользователя с хешированным паролем.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            telegram_chat_id=validated_data.get('telegram_chat_id', None)
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя (без пароля).
    """

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'telegram_chat_id',
            'first_name',
            'last_name',
        ]
        read_only_fields = ['email']
        