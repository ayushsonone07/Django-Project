from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from . import serializers
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from . import models
from .permissions import CustomPermission
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.encoding import force_bytes
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

# Create your views here.

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCsrfTokenView( APIView ):

     def get(self, request):
         return Response({'message': 'csrf token set successfully'}, status=status.HTTP_200_OK)

class HomeView( APIView ):

    permission_classes = [AllowAny]

    def get(self, request):
        text = [
            'api/users/register/',
            'api/users/login/',
            'api/users/logout/',
            'api/users/forgot_password/',
        ]
        return Response(text, status=status.HTTP_200_OK)


# ======== Register views ===========   

@method_decorator(csrf_protect, name='dispatch')
class RegisterView( APIView ):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User register successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StaffRegisterView( APIView ):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_staff=True)
            return Response({'message': 'Staff register successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======== Login views =========== 

@method_decorator(csrf_protect, name='dispatch')
class LoginView( APIView ):

    permission_classes  = [AllowAny]

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid()
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        print(email, password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token = get_tokens_for_user(user)
            return Response({
                'token': token,
                'message': 'User login Successfully'
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getUserView( APIView ):

    def get(self, request):
        user = request.user
        obj = User.objects.filter(id=user.id)
        serializer = serializers.UserSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LeaveView( APIView ):

    def get(self, request):
        user = request.user
        leave_obj = models.LeaveModel.objects.filter(user=user.id)
        serializer = serializers.LeaveSerializer(leave_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Leave applied succesfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView( APIView ):

    def get(self, request):
        user = request.user
        user_obj = models.ProfileModel.objects.filter(user=user.id)
        leave_obj = models.LeaveModel.objects.filter(user=user.id)
        serializer = serializers.ProfileSerializer([user_obj, leave_obj], many=True)
        return Response(serializer.data)



class SuperUserLeaveView( APIView ):

    permission_classes = [CustomPermission]

    def get(self, request):
        leave_obj = models.LeaveModel.objects.all()
        serializer = serializers.UserSerializer(leave_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class LogoutView( APIView ):
     def post(self, request):
         user = request.user
         queryset = User.objects.get(email=user.email)
         if queryset is not None:
            logout(request)
            return Response({'message': 'User logged out succesfully'})
         

class ForgotPasswordEmailView( APIView ):

    def post(self, request):
        email = request.data.get('email')

        if not User.objects.filter(email=email).exists():
            return Response({"message": "No User exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.get(email=email)

        serializer = serializers.UserLoginSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ForgotPasswordView( APIView ):
     
     def patch(self, request):
         new_password = request.data.get('new_passowrd')
         Confrim_password = request.data.get('Confrim_passowrd')
         user = request.user

         user_obj = User.objects.get(id=user.id)

         serializer = serializers.UserSerializer(user_obj, many=True)
         serializer.update(
             password=new_password,
             isinstance=True
             )
         
         return Response({"message": "Password Update successfully"}, status=status.HTTP_201_CREATED)


