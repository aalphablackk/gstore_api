from rest_framework import serializers
from .models import CustomUser


def send_otp_email(user):
    otp = user.generate_otp()
    subject = "Your OTP for email verification"
    message = f"Your OTP for email verification is: {otp}"
    user.email_user(subject, message)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Password do not match')
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email is already in use')

        
        return data

    class Meta:
        model = CustomUser
        fields = ['email','first_name', 'last_name', 'password', 'confirm_password']


    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)



        #email otp
        send_otp_email(user)
        
        # print(otp)

        return user

class GetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
