from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# serializer for user registration 
from django.db import transaction
from rest_framework.exceptions import ValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    def validate(self, data):
        
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        
        if data.get('phone_number') and CustomUser.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "A user with this phone number already exists."})

        return data

    @transaction.atomic
    def create(self, validated_data):
        try:
            
            password = validated_data.pop('password1')
            validated_data.pop('password2')

            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                phone_number=validated_data.get('phone_number', ''),
                password=password
            )
            return user
        except Exception as e:
            
            raise ValidationError({"detail": f"An error occurred while creating the user: {str(e)}"})






class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        
        token = super().get_token(user)

       

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }

        return data
    
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)