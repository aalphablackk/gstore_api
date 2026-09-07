from django.contrib.admin import action
from django.shortcuts import render
from rest_framework.views import APIView

from productApp.serializers import UserSerializer
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, send_otp_email,VerifyOTPSerializer, GetOTPSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        data = request.data

        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message":"Registration Successful", 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        otp = data.get('otp')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # user.verify_otp(otp)
        if user.verify_otp(otp):
            user.is_verified = True
            user.save()
            return Response({"message":"OTP verified successfully"}, status=status.HTTP_200_OK)
        return Response ({"message", "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

class GetOTPView(APIView):
    def post(self, request):
        serializer = GetOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            send_otp_email(user)
        return Response({"message":"OTP generated successfully"}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        password = serializer.validated_data['password']
        

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # create a signed token for the user

            if user.is_verified:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            else:
                send_otp_email(user)
                return Response({"message":"Email not verified. Please verify your account"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message":"Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



# class UserViewset(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer

#     @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
#     def me(self, request):
#         user = request.user
#         serializer = UserSerializer(user,many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def all_users(self, request):
#         users = CustomUser.objects.all()
#         paginator_users = self.paginator.paginate_queryset(users, request)
#         serializer = UserSerializer(users, many=True)
#         # return Response(serializer.data, status=status.HTTP_200_OK)
#         return self.paginator.get_paginated_response(serializer.data)
#     # lookup_field = 'id'  #to change the pk to id
