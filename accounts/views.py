import random
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.contrib.auth.hashers import make_password

from .serializers import *
from users.serializers import UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        self.token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': RegisterSerializer(user).data
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = self.token_data
        return response


class EmailRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = EmailRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        self.token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': RegisterSerializer(user).data
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = self.token_data
        return response



class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        user = authenticate(request, phone_number=phone_number, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'شماره تلفن یا رمز عبور اشتباه است'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.data.get("refresh")
            if not token:
                return Response({"error": "توکن اجباری است"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken(token)

            if hasattr(refresh, 'blacklist'):
                refresh.blacklist()

            return Response({"message": "خروج موفقیت‌آمیز بود"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class EmailLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailLoginSerializer  

    @extend_schema(
        request=EmailLoginSerializer,
        responses={
            200: UserSerializer,
            401: {
                "type": "object",
                "properties": {"detail": {"type": "string"}}
            }
        },
        examples=[
            OpenApiExample(
                "نمونه لاگین ایمیل",
                value={"email": "user@example.com", "password": "password123"},
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "full_name": user.get_full_name(),
                    "email": user.email,
                    "phone_number": user.phone_number
                }
            })
        return Response({"detail": "ایمیل یا رمز عبور اشتباه است."}, status=status.HTTP_401_UNAUTHORIZED)