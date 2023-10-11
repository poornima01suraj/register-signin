from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'web_terms', 'dataprocessing', 'subscription']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)
        return user

class UserSignInSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        try:
            user = CustomUser.objects.filter(
                Q(username__iexact=identifier) |
                Q(email__iexact=identifier) |
                Q(phone_number__iexact=identifier)
            ).first()
        
        

            if user and user.is_active and user.check_password(password):
                return user
            else:
                raise serializers.ValidationError("Invalid credentials")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")
